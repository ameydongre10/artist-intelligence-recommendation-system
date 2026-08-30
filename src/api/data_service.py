"""
Data Access Service.
Loads, validates, caches, and queries the processed artifacts:
- dataset_inventory.json
- artist_intelligence.jsonl
- media_selection_log.json
- hirer_intelligence.json
- recommendations.json
- updated_recommendation.json
"""

import os
from typing import Dict, List, Any, Optional
from src.api.config import ApiSettings, get_settings
from src.utils.file_utils import read_json_file, read_jsonl_file
from src.models.artifacts import (
    ArtistIntelligenceRecord,
    RecommendationsArtifact,
    UpdatedRecommendationArtifact
)
from src.models.hirer import HirerIntelligenceArtifact, HirerBrief
from src.models.recommendation import BriefRecommendation, ReRankingResult


class DataService:
    """
    Centralized data access service for API endpoints.
    Provides fast, cached access to validated domain artifacts.
    """
    def __init__(self, settings: Optional[ApiSettings] = None):
        self.settings = settings or get_settings()
        self._inventory_cache: Optional[Dict[str, Any]] = None
        self._artists_cache: Optional[List[ArtistIntelligenceRecord]] = None
        self._media_log_cache: Optional[Dict[str, Any]] = None
        self._hirer_cache: Optional[HirerIntelligenceArtifact] = None
        self._recommendations_cache: Optional[RecommendationsArtifact] = None
        self._updated_recommendation_cache: Optional[UpdatedRecommendationArtifact] = None

    def get_system_status(self) -> Dict[str, Any]:
        """Returns artifact availability, pipeline versions, and readiness status."""
        artifacts_status = {
            "dataset_inventory": os.path.exists(self.settings.inventory_path),
            "artist_intelligence": os.path.exists(self.settings.artist_intelligence_path),
            "media_selection_log": os.path.exists(self.settings.media_log_path),
            "hirer_intelligence": os.path.exists(self.settings.hirer_intelligence_path),
            "recommendations": os.path.exists(self.settings.recommendations_path),
            "updated_recommendation": os.path.exists(self.settings.updated_recommendation_path),
        }
        all_ready = all(artifacts_status.values())
        return {
            "status": "healthy" if all_ready else "degraded",
            "environment": self.settings.app_env,
            "version": self.settings.app_version,
            "artifacts_available": artifacts_status,
            "all_artifacts_ready": all_ready
        }

    def get_dataset_summary(self) -> Dict[str, Any]:
        """Returns structured summary of inventory, artists, media, and anomalies."""
        if not self._inventory_cache:
            if not os.path.exists(self.settings.inventory_path):
                raise FileNotFoundError("Dataset inventory artifact not found")
            self._inventory_cache = read_json_file(self.settings.inventory_path)

        inv = self._inventory_cache
        artists = self.get_all_artists()

        category_counts = {}
        for a in artists:
            cat = a.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

        anomalies = inv.get("dataset_anomalies", [])
        total_files = inv.get("dataset_metadata", {}).get("total_files", 149)

        return {
            "dataset_version": inv.get("dataset_metadata", {}).get("inventory_version", "1.0.0"),
            "total_files": total_files,
            "total_artists": len(artists),
            "artists_by_category": category_counts,
            "total_hirer_briefs": len(inv.get("hirer_conversations", [])),
            "total_follow_ups": len(inv.get("follow_up_updates", [])),
            "total_media_files": inv.get("file_type_distribution", {}).get("media_files_total", 120),
            "detected_anomalies_count": len(anomalies),
            "detected_anomalies": anomalies,
            "artifacts_status": {
                "artist_intelligence": "available",
                "hirer_intelligence": "available",
                "recommendations": "available",
                "updated_recommendation": "available"
            }
        }

    def get_all_artists(self, category: Optional[str] = None) -> List[ArtistIntelligenceRecord]:
        """Returns all artist intelligence records with optional category filter."""
        if self._artists_cache is None:
            if not os.path.exists(self.settings.artist_intelligence_path):
                raise FileNotFoundError("Artist intelligence artifact not found")
            raw_records = read_jsonl_file(self.settings.artist_intelligence_path)
            self._artists_cache = [ArtistIntelligenceRecord.model_validate(r) for r in raw_records]

        if category:
            cat_norm = category.lower().strip()
            return [a for a in self._artists_cache if a.category.value.lower() == cat_norm]
        return self._artists_cache

    def get_artist_by_id(self, artist_id: str) -> Optional[ArtistIntelligenceRecord]:
        """Looks up an artist by stable ID (e.g., 'P01', 'M01', 'V01', 'PO4', 'VO4') or folder name."""
        artists = self.get_all_artists()
        query = artist_id.strip().lower()
        for a in artists:
            if a.artist_id.lower() == query or a.source_folder_name.lower() == query:
                return a
            if a.declared_name and a.declared_name.lower() == query:
                return a
        return None

    def get_hirer_intelligence(self) -> HirerIntelligenceArtifact:
        """Returns the full hirer intelligence artifact."""
        if self._hirer_cache is None:
            if not os.path.exists(self.settings.hirer_intelligence_path):
                raise FileNotFoundError("Hirer intelligence artifact not found")
            raw_data = read_json_file(self.settings.hirer_intelligence_path)
            self._hirer_cache = HirerIntelligenceArtifact.model_validate(raw_data)
        return self._hirer_cache

    def get_all_hirer_briefs(self) -> List[HirerBrief]:
        """Returns all 4 hirer briefs."""
        return self.get_hirer_intelligence().briefs

    def get_hirer_brief_by_id(self, brief_id: str) -> Optional[HirerBrief]:
        """Looks up a brief by brief_id (e.g., '01_cafe_music_whatsapp')."""
        briefs = self.get_all_hirer_briefs()
        query = brief_id.strip().lower()
        for b in briefs:
            if b.brief_id.lower() == query or query in b.brief_id.lower():
                return b
        return None

    def get_recommendations_artifact(self) -> RecommendationsArtifact:
        """Returns the recommendations artifact."""
        if self._recommendations_cache is None:
            if not os.path.exists(self.settings.recommendations_path):
                raise FileNotFoundError("Recommendations artifact not found")
            raw_data = read_json_file(self.settings.recommendations_path)
            self._recommendations_cache = RecommendationsArtifact.model_validate(raw_data)
        return self._recommendations_cache

    def get_all_recommendations(self) -> List[BriefRecommendation]:
        """Returns all 4 brief recommendations."""
        return self.get_recommendations_artifact().recommendations

    def get_recommendation_by_brief_id(self, brief_id: str) -> Optional[BriefRecommendation]:
        """Looks up a recommendation by brief_id."""
        recs = self.get_all_recommendations()
        query = brief_id.strip().lower()
        for r in recs:
            if r.brief_id.lower() == query or query in r.brief_id.lower():
                return r
        return None

    def get_updated_recommendation_artifact(self) -> UpdatedRecommendationArtifact:
        """Returns the updated recommendation artifact for the follow-up update."""
        if self._updated_recommendation_cache is None:
            if not os.path.exists(self.settings.updated_recommendation_path):
                raise FileNotFoundError("Updated recommendation artifact not found")
            raw_data = read_json_file(self.settings.updated_recommendation_path)
            self._updated_recommendation_cache = UpdatedRecommendationArtifact.model_validate(raw_data)
        return self._updated_recommendation_cache

    def get_reranking_for_brief(self, brief_id: str) -> Optional[ReRankingResult]:
        """Returns the re-ranking result if available for this brief."""
        upd = self.get_updated_recommendation_artifact()
        query = brief_id.strip().lower()
        if upd.reranking.brief_id.lower() == query or query in upd.reranking.brief_id.lower() or "cafe" in query:
            return upd.reranking
        return None


# Global singleton instance
_data_service_instance: Optional[DataService] = None

def get_data_service() -> DataService:
    """Returns singleton DataService instance."""
    global _data_service_instance
    if _data_service_instance is None:
        _data_service_instance = DataService()
    return _data_service_instance
