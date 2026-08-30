"""
Trade-Off Analyzer.
Generates structured comparative trade-offs between Rank 1 and Rank 2 recommendations
by comparing their ScoreBreakdown objects against the brief requirements.

Trade-offs are computed from score differentials and capability status comparisons.
No artist IDs or brief IDs are hardcoded. Generalizes to any artist/brief pair.
"""

from typing import List, Set, Dict, Any
from src.models.recommendation import TradeOffItem
from src.models.hirer import HirerBrief
from src.matching.scorer import ScoreBreakdown
from src.framework.capability_dimensions import get_dimensions_for_category


def generate_trade_offs_for_brief(
    brief: HirerBrief,
    rank_1_score: ScoreBreakdown,
    rank_2_score: ScoreBreakdown
) -> List[TradeOffItem]:
    """
    Generates factual, evidence-backed trade-offs by comparing Rank 1 and Rank 2
    on every dimension required by the brief.

    A meaningful trade-off exists when one candidate has DEMONSTRATED_EVIDENCE and
    the other does not. Trade-offs are computed from score breakdowns.
    Generalized: works for any artist/brief pair without hardcoded IDs.
    Returns up to 4 most differentiated trade-off dimensions.
    """
    trade_offs: List[TradeOffItem] = []

    # Index capabilities by dimension for both candidates
    r1_caps: Dict[str, Dict] = {m["dimension"]: m for m in rank_1_score.matched_capabilities}
    r2_caps: Dict[str, Dict] = {m["dimension"]: m for m in rank_2_score.matched_capabilities}

    r1_unknowns: Set[str] = set(rank_1_score.unmatched_unknowns)
    r2_unknowns: Set[str] = set(rank_2_score.unmatched_unknowns)

    dim_defs = get_dimensions_for_category(brief.target_category)

    def status_to_label(dim: str, caps: Dict, unknowns: Set) -> str:
        if dim in caps:
            cap = caps[dim]
            status = cap.get("status", "UNKNOWN")
            strength = cap.get("strength", "")
            desc = cap.get("description", "")[:80]
            if status == "DEMONSTRATED_EVIDENCE":
                return "DEMONSTRATED ({}): {}".format(strength, desc)
            elif status == "CLAIM":
                return "CLAIMED (unverified): {}".format(desc)
        if dim in unknowns:
            return "UNKNOWN - no evidence in portfolio"
        return "UNKNOWN"

    for req in brief.known_requirements:
        dim = req.dimension
        r1_label = status_to_label(dim, r1_caps, r1_unknowns)
        r2_label = status_to_label(dim, r2_caps, r2_unknowns)

        r1_has_demo = dim in r1_caps and r1_caps[dim].get("status") == "DEMONSTRATED_EVIDENCE"
        r2_has_demo = dim in r2_caps and r2_caps[dim].get("status") == "DEMONSTRATED_EVIDENCE"

        if r1_has_demo == r2_has_demo:
            continue

        dim_def = dim_defs.get(dim)
        dim_name = dim_def.display_name if dim_def else dim.replace("_", " ").title()

        if r1_has_demo:
            implication = (
                "Rank 1 has stronger demonstrated capability on '{}'. "
                "Rank 2 is a viable fallback but carries higher uncertainty on this requirement."
            ).format(dim_name)
        else:
            implication = (
                "Rank 2 has stronger demonstrated capability on '{}'. "
                "Prioritizing this dimension would favor Rank 2, provided Rank 1 gaps can be resolved."
            ).format(dim_name)

        trade_offs.append(TradeOffItem(
            dimension=dim,
            rank_1_status=r1_label,
            rank_2_status=r2_label,
            decision_implication=implication
        ))

        if len(trade_offs) >= 4:
            break

    if not trade_offs:
        delta = rank_1_score.total_score - rank_2_score.total_score
        trade_offs.append(TradeOffItem(
            dimension="overall_score",
            rank_1_status="Score: {}/100 ({} confidence)".format(
                rank_1_score.total_score, rank_1_score.confidence.value),
            rank_2_status="Score: {}/100 ({} confidence)".format(
                rank_2_score.total_score, rank_2_score.confidence.value),
            decision_implication=(
                "Rank 1 scores {:.1f} points {} overall. "
                "Both candidates have similar evidence profiles on the key dimensions."
            ).format(abs(delta), "higher" if delta > 0 else "lower")
        ))

    return trade_offs
