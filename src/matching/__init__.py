"""Matching and Recommendation Package."""
from src.matching.scorer import calculate_match_score, ScoreBreakdown
from src.matching.tradeoffs import generate_trade_offs_for_brief
from src.matching.ranking import rank_artists_for_brief
from src.matching.reranking import process_follow_up_reranking
from src.matching.engine import RecommendationEngine

__all__ = [
    "calculate_match_score",
    "ScoreBreakdown",
    "generate_trade_offs_for_brief",
    "rank_artists_for_brief",
    "process_follow_up_reranking",
    "RecommendationEngine"
]
