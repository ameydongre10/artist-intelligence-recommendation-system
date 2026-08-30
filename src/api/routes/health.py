"""Health and System Status Endpoints."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from src.api.data_service import DataService, get_data_service

router = APIRouter(tags=["Health & System"])


@router.get("/api/health", summary="Health check endpoint")
def health_check() -> Dict[str, str]:
    """Returns application liveness and health status."""
    return {
        "status": "healthy",
        "service": "artist-intelligence-api",
        "version": "1.0.0"
    }


@router.get("/api/system/status", summary="Detailed system and artifact readiness status")
def system_status(data_service: DataService = Depends(get_data_service)) -> Dict[str, Any]:
    """Returns availability of all underlying processed artifacts and system readiness."""
    return data_service.get_system_status()
