"""Hirer Brief Intelligence Endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from src.api.data_service import DataService, get_data_service
from src.models.hirer import HirerBrief

router = APIRouter(tags=["Hirer Briefs"])


@router.get("/api/briefs", summary="List all 4 hirer briefs with context summaries")
@router.get("/api/hirer-briefs", summary="List all 4 hirer briefs with context summaries (alias)")
def list_hirer_briefs(data_service: DataService = Depends(get_data_service)) -> List[Dict[str, Any]]:
    """
    Returns high-level summary metadata for all 4 hirer briefs.
    """
    briefs = data_service.get_all_hirer_briefs()
    return [
        {
            "brief_id": b.brief_id,
            "hirer_name": b.hirer_name,
            "channel": b.channel,
            "target_category": b.target_category.value,
            "situation": b.context.situation,
            "timeline": b.context.target_date_or_timeline,
            "location": b.context.location_or_venue,
            "known_requirements_count": len(b.known_requirements),
            "hard_constraints_count": len(b.hard_constraints),
            "unknowns_count": len(b.unknowns),
            "contradictions_count": len(b.contradictions)
        }
        for b in briefs
    ]


@router.get("/api/briefs/{brief_id}", summary="Get structured hirer intelligence for a brief", response_model=HirerBrief)
@router.get("/api/hirer-briefs/{brief_id}", summary="Get structured hirer intelligence for a brief (alias)", response_model=HirerBrief)
def get_hirer_brief_detail(
    brief_id: str,
    data_service: DataService = Depends(get_data_service)
) -> HirerBrief:
    """
    Returns the complete structured intelligence for a single hirer brief,
    including context, explicit requirements, constraints, preferences, deliverables,
    assumptions, unknowns, ambiguities, and contradictions.
    """
    brief = data_service.get_hirer_brief_by_id(brief_id)
    if not brief:
        raise HTTPException(
            status_code=404,
            detail=f"Hirer brief '{brief_id}' was not found in processed records"
        )
    return brief
