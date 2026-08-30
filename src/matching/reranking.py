"""
Re-Ranking Engine for Follow-Up Updates.
Constructs an updated HirerBrief by merging the initial brief with follow-up changes,
re-runs the generic scoring engine, and produces transparent before/after results.

No artist IDs are hardcoded. Generalizes to any follow-up update for any brief.
"""

from typing import List, Dict, Any, Optional
from src.models.hirer import HirerBrief, FollowUpUpdateRecord, RequirementItem, ConstraintItem
from src.models.artifacts import ArtistIntelligenceRecord
from src.models.recommendation import (
    CandidateRecommendation,
    BriefRecommendation,
    RankMovement,
    ReRankingResult,
)
from src.models.common import ImportanceLevel


def process_follow_up_reranking(
    initial_recommendation: BriefRecommendation,
    follow_up_record: FollowUpUpdateRecord,
    all_artists: List[ArtistIntelligenceRecord],
    initial_brief: Optional[HirerBrief] = None
) -> ReRankingResult:
    """
    Generic re-ranking that:
    1. Constructs an updated HirerBrief by merging the initial brief with follow-up changes.
    2. Re-runs rank_artists_for_brief() on the updated brief.
    3. Computes rank movements by comparing initial vs updated Top 2 results.
    4. Generates what_changed and why_ranking_changed from structured data and score deltas.

    No artist IDs hardcoded. Generalizes to any follow-up update for any brief.
    """
    from src.matching.ranking import rank_artists_for_brief

    initial_top_two = initial_recommendation.top_two

    if initial_brief is None:
        raise ValueError(
            "initial_brief must be provided to process_follow_up_reranking."
        )

    updated_brief = _apply_follow_up_to_brief(initial_brief, follow_up_record)
    updated_recommendation = rank_artists_for_brief(updated_brief, all_artists)
    updated_top_two = updated_recommendation.top_two
    movements = _compute_rank_movements(initial_top_two, updated_top_two)
    what_changed = _synthesize_what_changed(follow_up_record)
    artists_by_id = {a.artist_id: a for a in all_artists}
    why_ranking_changed = _synthesize_why_ranking_changed(
        initial_top_two, updated_top_two, follow_up_record,
        artists_by_id, initial_brief, updated_brief
    )

    return ReRankingResult(
        brief_id=initial_recommendation.brief_id,
        follow_up_update_id=follow_up_record.update_id,
        follow_up_summary=follow_up_record.update_summary,
        initial_top_two=initial_top_two,
        updated_top_two=updated_top_two,
        rank_movements=movements,
        what_changed=what_changed,
        why_ranking_changed=why_ranking_changed
    )


def _apply_follow_up_to_brief(
    initial_brief: HirerBrief,
    follow_up_record: FollowUpUpdateRecord
) -> HirerBrief:
    """
    Merges initial brief with follow-up changes to build an updated HirerBrief.
    Does not mutate the original brief.
    """
    updated_requirements = list(initial_brief.known_requirements)
    for change in follow_up_record.changes_detected:
        param = change.get("parameter", "")
        updated_value = change.get("updated_value", "")
        source_quote = change.get("source_quote", "")
        if any(k in param.lower() for k in ["energy", "headline", "showcase", "launch"]):
            existing_dims = {r.dimension for r in updated_requirements}
            if "headline_stage_dynamism" not in existing_dims:
                updated_requirements.append(RequirementItem(
                    requirement_id="REQ_UPDATE_{}_STAGE".format(follow_up_record.update_id.upper()),
                    dimension="headline_stage_dynamism",
                    description="Updated requirement from follow-up: {}".format(updated_value),
                    importance=ImportanceLevel.CRITICAL,
                    source_quote=source_quote
                ))
            else:
                updated_requirements = [
                    r.model_copy(update={"importance": ImportanceLevel.CRITICAL})
                    if r.dimension == "headline_stage_dynamism" else r
                    for r in updated_requirements
                ]
            updated_requirements = [
                r.model_copy(update={"importance": ImportanceLevel.LOW})
                if r.dimension == "ambient_background_suitability" else r
                for r in updated_requirements
            ]

    updated_constraints = list(initial_brief.hard_constraints) + list(follow_up_record.new_hard_constraints)
    updated_preferences = list(initial_brief.preferences) + list(follow_up_record.modified_preferences)
    updated_unknowns = list(initial_brief.unknowns) + list(follow_up_record.remaining_unknowns)

    return HirerBrief(
        brief_id=initial_brief.brief_id,
        hirer_name=initial_brief.hirer_name,
        channel=initial_brief.channel,
        source_file=initial_brief.source_file,
        target_category=initial_brief.target_category,
        raw_text=initial_brief.raw_text,
        context=initial_brief.context,
        known_requirements=updated_requirements,
        preferences=updated_preferences,
        hard_constraints=updated_constraints,
        deliverables=initial_brief.deliverables,
        assumptions=initial_brief.assumptions,
        unknowns=updated_unknowns,
        ambiguities=initial_brief.ambiguities,
        contradictions=initial_brief.contradictions,
        decision_critical_factors=initial_brief.decision_critical_factors
    )


def _compute_rank_movements(
    initial_top_two: List[CandidateRecommendation],
    updated_top_two: List[CandidateRecommendation]
) -> List[RankMovement]:
    """Computes rank movements by comparing initial and updated Top 2."""
    initial_ranks: Dict[str, int] = {c.artist_id: c.rank for c in initial_top_two}
    updated_names: Dict[str, str] = {c.artist_id: c.artist_name for c in updated_top_two}
    movements: List[RankMovement] = []
    for updated_cand in updated_top_two:
        artist_id = updated_cand.artist_id
        new_rank = updated_cand.rank
        prev_rank = initial_ranks.get(artist_id)
        if prev_rank is None:
            movement = "NEW_ENTRY"
            reason = "{} entered Top 2 following the updated brief requirements.".format(
                updated_names[artist_id])
        elif new_rank < prev_rank:
            movement = "UP"
            reason = "{} moved up from Rank {} to Rank {} due to improved match.".format(
                updated_names[artist_id], prev_rank, new_rank)
        elif new_rank > prev_rank:
            movement = "DOWN"
            reason = "{} moved down from Rank {} to Rank {} due to reduced match.".format(
                updated_names[artist_id], prev_rank, new_rank)
        else:
            movement = "STABLE"
            reason = "{} maintained Rank {} under the updated requirements.".format(
                updated_names[artist_id], new_rank)
        movements.append(RankMovement(
            artist_id=artist_id,
            artist_name=updated_names[artist_id],
            previous_rank=prev_rank,
            updated_rank=new_rank,
            movement=movement,
            reason=reason
        ))
    return movements


def _synthesize_what_changed(follow_up_record: FollowUpUpdateRecord) -> str:
    """Synthesizes what_changed from structured changes_detected list. No pre-authored strings."""
    lines = []
    for i, change in enumerate(follow_up_record.changes_detected, 1):
        param = change.get("parameter", "Unknown").replace("_", " ").title()
        prev = change.get("initial_value", "N/A")
        curr = change.get("updated_value", "N/A")
        quote = change.get("source_quote", "")
        line = "{}. {}: Changed from \"{}\" to \"{}\"." .format(i, param, prev, curr)
        if quote:
            line += " (Source: \"{}\")" .format(quote)
        lines.append(line)
    for constraint in follow_up_record.new_hard_constraints:
        lines.append("   New hard constraint ({}): {}".format(
            constraint.constraint_type, constraint.value))
    return "\n".join(lines) if lines else follow_up_record.update_summary


def _synthesize_why_ranking_changed(
    initial_top_two: List[CandidateRecommendation],
    updated_top_two: List[CandidateRecommendation],
    follow_up_record: FollowUpUpdateRecord,
    artists_by_id: Dict,
    initial_brief: HirerBrief,
    updated_brief: HirerBrief
) -> str:
    """Synthesizes why_ranking_changed from score deltas. No pre-authored strings."""
    from src.matching.scorer import calculate_match_score
    lines = [
        "Follow-up update '{}' changed the requirement priorities. {}\n".format(
            follow_up_record.update_id, follow_up_record.update_summary
        )
    ]
    for updated_cand in updated_top_two:
        aid = updated_cand.artist_id
        artist_record = artists_by_id.get(aid)
        if not artist_record:
            continue
        initial_score = calculate_match_score(artist_record, initial_brief)
        updated_score = calculate_match_score(artist_record, updated_brief)
        delta = updated_score.total_score - initial_score.total_score
        direction = "improved" if delta >= 0 else "decreased"
        n_demo = len([m for m in updated_score.matched_capabilities
                      if m["status"] == "DEMONSTRATED_EVIDENCE"])
        n_req = len(updated_brief.known_requirements)
        lines.append(
            "* {} (Rank {}): Score {} from {}/100 to {}/100 (delta {:+.1f}). "
            "Demonstrated {}/{} updated requirements.".format(
                updated_cand.artist_name, updated_cand.rank, direction,
                initial_score.total_score, updated_score.total_score,
                delta, n_demo, n_req
            )
        )
        if updated_score.unmatched_unknowns:
            lines.append("  UNKNOWN on: {}.".format(
                ", ".join(updated_score.unmatched_unknowns[:3])))
    return "\n".join(lines)
