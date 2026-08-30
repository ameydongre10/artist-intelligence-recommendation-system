"""Artist Intelligence Endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from src.api.data_service import DataService, get_data_service
from src.models.artifacts import ArtistIntelligenceRecord

router = APIRouter(prefix="/api/artists", tags=["Artists"])


@router.get("", summary="List all artists with optional category filtering")
def list_artists(
    category: Optional[str] = Query(None, description="Filter by category: 'photographer', 'musician', 'video_editor'"),
    data_service: DataService = Depends(get_data_service)
) -> List[Dict[str, Any]]:
    """
    Returns lightweight summary cards for all artists in the dataset.
    Preserves raw folder names and declared docx identities transparently.
    """
    artists = data_service.get_all_artists(category=category)
    return [
        {
            "artist_id": a.artist_id,
            "source_folder_name": a.source_folder_name,
            "category": a.category.value,
            "declared_name": a.declared_name,
            "identifier_status": a.identifier_status.value,
            "confidence": a.confidence.value,
            "demonstrated_capabilities_count": len(a.demonstrated_capabilities),
            "profile_claims_count": len(a.profile_claims),
            "unknowns_count": len(a.unknowns),
            "discrepancies_and_anomalies": a.discrepancies_and_anomalies
        }
        for a in artists
    ]


@router.get("/{artist_id}", summary="Get detailed artist intelligence profile by ID", response_model=ArtistIntelligenceRecord)
def get_artist_detail(
    artist_id: str,
    data_service: DataService = Depends(get_data_service)
) -> ArtistIntelligenceRecord:
    """
    Returns the complete, evidence-backed intelligence profile for a single artist.
    Includes profile claims, demonstrated capabilities with evidence citations,
    category dimensions, unknowns, and anomalies.
    """
    artist = data_service.get_artist_by_id(artist_id)
    if not artist:
        raise HTTPException(
            status_code=404,
            detail=f"Artist with ID or name '{artist_id}' was not found in processed dataset"
        )
    return artist
