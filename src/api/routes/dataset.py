"""Dataset Summary Endpoints."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from src.api.data_service import DataService, get_data_service

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])


@router.get("/summary", summary="Dataset inventory and processed pipeline summary")
def get_dataset_summary(data_service: DataService = Depends(get_data_service)) -> Dict[str, Any]:
    """
    Returns comprehensive summary statistics of the raw dataset,
    including file counts, categories, discovered anomalies, and artifact availability.
    """
    return data_service.get_dataset_summary()
