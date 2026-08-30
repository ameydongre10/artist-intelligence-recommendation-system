"""API routes package."""
from src.api.routes.health import router as health_router
from src.api.routes.dataset import router as dataset_router
from src.api.routes.artists import router as artists_router
from src.api.routes.hirers import router as hirers_router
from src.api.routes.recommendations import router as recommendations_router

__all__ = [
    "health_router",
    "dataset_router",
    "artists_router",
    "hirers_router",
    "recommendations_router"
]
