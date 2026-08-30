"""Recommendation and Follow-Up Re-Ranking Endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from src.api.data_service import DataService, get_data_service
from src.models.recommendation import BriefRecommendation, ReRankingResult

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("", summary="List recommendation summaries for all briefs")
def list_recommendations(data_service: DataService = Depends(get_data_service)) -> List[Dict[str, Any]]:
    """
    Returns high-level summaries of recommendations across all 4 hirer briefs,
    including Top 2 candidate IDs, names, and confidence levels.
    """
    recs = data_service.get_all_recommendations()
    return [
        {
            "brief_id": r.brief_id,
            "hirer_name": r.hirer_name,
            "summary_of_need": r.summary_of_need,
            "top_two": [
                {
                    "rank": c.rank,
                    "artist_id": c.artist_id,
                    "artist_name": c.artist_name,
                    "category": c.category.value,
                    "confidence": c.confidence.value,
                    "evidence_citations_count": len(c.supporting_evidence)
                }
                for c in r.top_two
            ],
            "refinement_questions_count": len(r.refinement_questions)
        }
        for r in recs
    ]


@router.get("/{brief_id}", summary="Get full decision intelligence and Top 2 recommendations for a brief", response_model=BriefRecommendation)
def get_recommendation_detail(
    brief_id: str,
    data_service: DataService = Depends(get_data_service)
) -> BriefRecommendation:
    """
    Returns the complete decision intelligence for a brief, including:
    - Top 2 ranked recommendations with fit reasons and evidence citations
    - Matched capability requirements with evidence chains
    - Comparative trade-off analysis between Rank 1 and Rank 2
    - Explicit operational assumptions and key uncertainties
    - At most 2 high-impact refinement questions with decision impact explanations
    """
    rec = data_service.get_recommendation_by_brief_id(brief_id)
    if not rec:
        raise HTTPException(
            status_code=404,
            detail=f"Recommendation for brief '{brief_id}' was not found"
        )
    return rec


@router.get("/{brief_id}/updated", summary="Get transparent follow-up re-ranking result for a brief", response_model=ReRankingResult)
def get_updated_recommendation_reranking(
    brief_id: str,
    data_service: DataService = Depends(get_data_service)
) -> ReRankingResult:
    """
    Returns the transparent follow-up re-ranking result for a brief (e.g. '01_cafe_music_whatsapp').
    Shows initial Top 2, updated Top 2, rank movements, parameter deltas, and why the ranking changed or held stable.
    """
    rerank = data_service.get_reranking_for_brief(brief_id)
    if not rerank:
        raise HTTPException(
            status_code=404,
            detail=f"No follow-up re-ranking update found for brief '{brief_id}'"
        )
    return rerank
