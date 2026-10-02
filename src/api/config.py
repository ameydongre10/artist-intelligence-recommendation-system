"""
API Configuration Settings.
Loads configuration from environment variables with sensible production and local defaults.
"""

import os
from typing import List
from pydantic import BaseModel, Field


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _resolve_data_path(env_var: str, default_rel: str) -> str:
    path = os.getenv(env_var, default_rel)
    if not os.path.isabs(path):
        return os.path.normpath(os.path.join(REPO_ROOT, path))
    return path


class ApiSettings(BaseModel):
    """Configuration settings for the FastAPI application."""
    app_name: str = Field(default="Artist Intelligence & Recommendation System API")
    app_version: str = Field(default="1.0.0")
    app_env: str = Field(default=os.getenv("APP_ENV", "development"))
    debug: bool = Field(default=os.getenv("DEBUG", "false").lower() == "true")
    host: str = Field(default=os.getenv("HOST", "0.0.0.0"))
    port: int = Field(default=int(os.getenv("PORT", "8000")))
    
    # CORS Origins (supports comma-separated string from env)
    cors_origins: List[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                "https://ameydongre10.github.io,http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://localhost:8000,http://127.0.0.1:8000"
            ).split(",")
            if origin.strip()
        ]
    )

    # Processed Artifact Paths (Repository-relative and deployment safe)
    inventory_path: str = Field(default_factory=lambda: _resolve_data_path("INVENTORY_PATH", "data/processed/dataset_inventory.json"))
    artist_intelligence_path: str = Field(default_factory=lambda: _resolve_data_path("ARTIST_INTEL_PATH", "data/processed/artist_intelligence.jsonl"))
    media_log_path: str = Field(default_factory=lambda: _resolve_data_path("MEDIA_LOG_PATH", "data/processed/media_selection_log.json"))
    hirer_intelligence_path: str = Field(default_factory=lambda: _resolve_data_path("HIRER_INTEL_PATH", "data/processed/hirer_intelligence.json"))
    recommendations_path: str = Field(default_factory=lambda: _resolve_data_path("RECOMMENDATIONS_PATH", "data/processed/recommendations.json"))
    updated_recommendation_path: str = Field(default_factory=lambda: _resolve_data_path("UPDATED_RECOMMENDATION_PATH", "data/processed/updated_recommendation.json"))


def get_settings() -> ApiSettings:
    """Returns singleton-like settings instance."""
    return ApiSettings()
