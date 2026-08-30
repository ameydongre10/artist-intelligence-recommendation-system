"""
Ranking and Top 2 Recommendation Generator.
Filters artists by category, computes transparent match scores, selects exactly Top 2 candidates,
constructs evidence-backed fit reasons and trade-offs, and generates at most 2 refinement questions.
"""

from typing import List, Dict, Any, Tuple
from src.models.common import ArtistCategory, ConfidenceLevel
from src.models.evidence import EvidenceCitation
from src.models.hirer import HirerBrief
from src.models.artifacts import ArtistIntelligenceRecord
from src.models.recommendation import (
    RequirementMatch,
    CandidateRecommendation,
    BriefRecommendation,
    RefinementQuestion,
    TradeOffItem
)
from src.matching.scorer import calculate_match_score, ScoreBreakdown
from src.matching.tradeoffs import generate_trade_offs_for_brief


def rank_artists_for_brief(
    brief: HirerBrief,
    all_artists: List[ArtistIntelligenceRecord]
) -> BriefRecommendation:
    """
    Evaluates candidate pool in target category, computes scores, selects Top 2,
    and returns a validated BriefRecommendation.
    """
    # 1. Category Filtering
    category_candidates = [
        a for a in all_artists if a.category == brief.target_category
    ]

    # 2. Score Candidates
    candidate_scores: List[Tuple[ArtistIntelligenceRecord, ScoreBreakdown]] = []
    for artist in category_candidates:
        score_breakdown = calculate_match_score(artist, brief)
        candidate_scores.append((artist, score_breakdown))

    # 3. Deterministic Sorting: Primary by total_score desc, Secondary by evidence_strength_score desc
    sorted_candidates = sorted(
        candidate_scores,
        key=lambda x: (x[1].total_score, x[1].evidence_strength_score),
        reverse=True
    )

    # 4. Extract Top 2 Candidates
    rank_1_artist, rank_1_score = sorted_candidates[0]
    rank_2_artist, rank_2_score = sorted_candidates[1]

    # 5. Build Candidate Recommendations
    rec_1 = _build_candidate_recommendation(1, rank_1_artist, rank_1_score, brief)
    rec_2 = _build_candidate_recommendation(2, rank_2_artist, rank_2_score, brief)

    # 6. Generate Trade-Offs
    trade_offs = generate_trade_offs_for_brief(brief, rank_1_score, rank_2_score)

    # 7. Generate Refinement Questions (Max 2)
    refinement_questions = _generate_refinement_questions_for_brief(brief)

    # 8. Construct Brief Recommendation
    summary_of_need = f"{brief.context.situation} requiring {brief.target_category.value} for {brief.context.target_date_or_timeline}."

    return BriefRecommendation(
        brief_id=brief.brief_id,
        hirer_name=brief.hirer_name,
        summary_of_need=summary_of_need,
        top_two=[rec_1, rec_2],
        trade_off_analysis=trade_offs,
        assumptions_made=[asm.description for asm in brief.assumptions],
        key_uncertainties=[ukn.description for ukn in brief.unknowns],
        refinement_questions=refinement_questions
    )


def _build_candidate_recommendation(
    rank: int,
    artist: ArtistIntelligenceRecord,
    score: ScoreBreakdown,
    brief: HirerBrief
) -> CandidateRecommendation:
    """Builds a structured CandidateRecommendation with evidence citations and fit reasons."""
    
    # Collect evidence citations from demonstrated capabilities
    citations: List[EvidenceCitation] = []
    matched_reqs: List[RequirementMatch] = []

    demo_caps = {dc["dimension"]: dc for dc in artist.demonstrated_capabilities}

    for req in brief.known_requirements:
        dim = req.dimension
        if dim in demo_caps:
            cap = demo_caps[dim]
            cits = [EvidenceCitation.model_validate(c) for c in cap.get("evidence_citations", [])]
            citations.extend(cits)
            
            matched_reqs.append(
                RequirementMatch(
                    requirement_id=req.requirement_id,
                    dimension=dim,
                    artist_capability_id=cap.get("capability_id"),
                    match_status="STRONG_MATCH" if cap.get("evidence_strength") == "STRONG" else "MODERATE_MATCH",
                    fit_explanation=f"Demonstrated: {cap.get('description')}",
                    supporting_evidence=cits
                )
            )
        else:
            matched_reqs.append(
                RequirementMatch(
                    requirement_id=req.requirement_id,
                    dimension=dim,
                    artist_capability_id=None,
                    match_status="UNKNOWN_FIT",
                    fit_explanation=f"No direct portfolio evidence provided for '{dim}' (treated neutrally as UNKNOWN)",
                    supporting_evidence=[]
                )
            )

    # Deduplicate citations by evidence_id
    seen_ids = set()
    unique_citations = []
    for c in citations:
        if c.evidence_id not in seen_ids:
            seen_ids.add(c.evidence_id)
            unique_citations.append(c)

    # Contextual fit reason synthesis
    fit_reason = _synthesize_fit_reason(rank, artist, score, brief)

    # Specific trade-offs & limitations
    trade_offs_list = _extract_trade_offs_list(rank, artist, brief)
    uncertainties_list = [u["reason"] for u in artist.unknowns]

    return CandidateRecommendation(
        rank=rank,
        artist_id=artist.artist_id,
        artist_name=artist.declared_name or artist.source_folder_name,
        category=artist.category,
        fit_reason=fit_reason,
        matched_requirements=matched_reqs,
        supporting_evidence=unique_citations[:4],  # Top 4 most relevant citations
        confidence=score.confidence,
        trade_offs=trade_offs_list,
        uncertainty_and_limitations=uncertainties_list
    )


def _synthesize_fit_reason(
    rank: int,
    artist: ArtistIntelligenceRecord,
    score: ScoreBreakdown,
    brief: HirerBrief
) -> str:
    """
    Generates an evidence-backed fit reason from the computed score breakdown.
    Generalized: works for any artist/brief combination without hardcoded IDs.
    """
    artist_name = artist.declared_name or artist.source_folder_name
    demonstrated_dims = [
        m["dimension"].replace("_", " ")
        for m in score.matched_capabilities
        if m["status"] == "DEMONSTRATED_EVIDENCE"
    ]
    claimed_dims = [
        m["dimension"].replace("_", " ")
        for m in score.matched_capabilities
        if m["status"] == "CLAIM"
    ]
    unknown_dims = [u.replace("_", " ") for u in score.unmatched_unknowns[:2]]

    fit_summary = ""
    if demonstrated_dims:
        fit_summary = f"Demonstrated capability in: {', '.join(demonstrated_dims[:3])}."
    if claimed_dims:
        fit_summary += f" Claimed (unverified): {', '.join(claimed_dims[:2])}."
    if unknown_dims:
        fit_summary += f" UNKNOWN evidence on: {', '.join(unknown_dims)}."

    return (
        f"{artist_name} ranks #{rank} — {fit_summary} "
        f"(Score: {score.total_score}/100, Confidence: {score.confidence.value}). "
        f"{score.explanation}"
    )


def _extract_trade_offs_list(
    rank: int,
    artist: ArtistIntelligenceRecord,
    brief: HirerBrief
) -> List[str]:
    """
    Generates candidate-specific trade-offs from the artist's unknown dimensions relative to
    the brief requirements. Generalized: works for any artist/brief combination.
    """
    trade_offs: List[str] = []

    # Trade-off 1: missing evidence on brief requirements
    brief_dims = {req.dimension for req in brief.known_requirements}
    demo_dims = {dc["dimension"] for dc in artist.demonstrated_capabilities}
    unknown_dims_for_brief = brief_dims - demo_dims
    for dim in list(unknown_dims_for_brief)[:2]:
        readable = dim.replace("_", " ").title()
        trade_offs.append(f"UNKNOWN evidence on '{readable}' required by this brief.")

    # Trade-off 2: anomalies or identifier discrepancies
    if artist.discrepancies_and_anomalies:
        anomaly = artist.discrepancies_and_anomalies[0]
        trade_offs.append(f"Dataset anomaly noted: {anomaly[:120]}")

    # Trade-off 3: low-confidence rating
    if artist.confidence.value == "LOW":
        trade_offs.append(f"Overall portfolio confidence: {artist.confidence.value} — limited media samples available.")

    return trade_offs if trade_offs else [f"Evidence confidence: {artist.confidence.value}"]



def _generate_refinement_questions_for_brief(brief: HirerBrief) -> List[RefinementQuestion]:
    """
    Generates at most 2 high-impact refinement questions from the brief's structured
    unknowns and ambiguities. Generalized: works for any brief without hardcoded IDs.
    Priority is given to decision-critical unknowns (is_decision_critical=True), then
    non-critical unknowns, then ambiguities.
    """
    questions: List[RefinementQuestion] = []

    # Priority 1: Decision-critical unknowns
    decision_critical = [u for u in brief.unknowns if u.is_decision_critical]
    # Priority 2: Non-critical unknowns
    non_critical = [u for u in brief.unknowns if not u.is_decision_critical]
    # Priority 3: Ambiguities
    ambiguities = getattr(brief, "ambiguities", [])

    candidates = decision_critical + non_critical
    for ukn in candidates:
        if len(questions) >= 2:
            break
        questions.append(RefinementQuestion(
            question_id=f"Q{len(questions) + 1}",
            question_text=f"Regarding '{ukn.description}': {ukn.why_it_matters} Can this be clarified before artist selection?",
            why_it_matters=ukn.why_it_matters,
            potential_ranking_impact=(
                f"Resolves {ukn.unknown_id} — this unknown is "
                f"{'decision-critical' if ukn.is_decision_critical else 'relevant'} "
                f"and could alter candidate ranking or eliminate a candidate if resolved."
            )
        ))

    # Fill remaining slot from ambiguities if fewer than 2 questions
    for amb in ambiguities:
        if len(questions) >= 2:
            break
        questions.append(RefinementQuestion(
            question_id=f"Q{len(questions) + 1}",
            question_text=f"Clarification needed: '{amb.statement}' — which interpretation applies? {' / '.join(amb.possible_interpretations[:2])}",
            why_it_matters=amb.decision_risk,
            potential_ranking_impact=(
                f"Resolves {amb.ambiguity_id} — misinterpretation risk: {amb.decision_risk[:100]}"
            )
        ))

    return questions[:2]
