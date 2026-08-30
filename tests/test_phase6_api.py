"""
Comprehensive Tests for Phase 6: FastAPI Backend & Data Access.
Tests all endpoints, category filtering, detailed records, error handling,
OpenAPI schema, and follow-up re-ranking exposure using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify root greeting and documentation links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["documentation"] == "/docs"
    assert data["health_check"] == "/api/health"


def test_health_endpoint():
    """Verify /api/health returns healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "artist-intelligence-api"


def test_system_status_endpoint():
    """Verify /api/system/status confirms all processed artifacts are ready."""
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["all_artifacts_ready"] is True
    assert data["artifacts_available"]["artist_intelligence"] is True
    assert data["artifacts_available"]["hirer_intelligence"] is True
    assert data["artifacts_available"]["recommendations"] is True
    assert data["artifacts_available"]["updated_recommendation"] is True


def test_dataset_summary_endpoint():
    """Verify /api/dataset/summary returns factual inventory statistics."""
    response = client.get("/api/dataset/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_artists"] == 15
    assert data["total_files"] == 149
    assert data["total_hirer_briefs"] == 4
    assert data["total_follow_ups"] == 1
    assert data["artists_by_category"]["photographer"] == 5
    assert data["artists_by_category"]["musician"] == 5
    assert data["artists_by_category"]["video_editor"] == 5
    assert data["detected_anomalies_count"] == 7


def test_list_artists_endpoint():
    """Verify /api/artists lists all 15 artists."""
    response = client.get("/api/artists")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 15


def test_list_artists_with_category_filter():
    """Verify /api/artists?category=... correctly filters artist list."""
    res_photo = client.get("/api/artists?category=photographer")
    assert res_photo.status_code == 200
    assert len(res_photo.json()) == 5
    assert all(a["category"] == "photographer" for a in res_photo.json())

    res_music = client.get("/api/artists?category=musician")
    assert res_music.status_code == 200
    assert len(res_music.json()) == 5
    assert all(a["category"] == "musician" for a in res_music.json())

    res_video = client.get("/api/artists?category=video_editor")
    assert res_video.status_code == 200
    assert len(res_video.json()) == 5
    assert all(a["category"] == "video_editor" for a in res_video.json())


def test_get_artist_detail_success():
    """Verify /api/artists/{artist_id} returns full intelligence record."""
    response = client.get("/api/artists/P01")
    assert response.status_code == 200
    data = response.json()
    assert data["artist_id"] == "P01"
    assert data["category"] == "photographer"
    assert len(data["demonstrated_capabilities"]) > 0
    assert len(data["profile_claims"]) > 0

    # Check anomalous artist lookup (PO4)
    res_po4 = client.get("/api/artists/PO4")
    assert res_po4.status_code == 200
    assert res_po4.json()["artist_id"] == "PO4"


def test_get_artist_detail_not_found():
    """Verify /api/artists/{invalid_id} returns structured 404."""
    response = client.get("/api/artists/UNKNOWN_ARTIST_999")
    assert response.status_code == 404
    data = response.json()
    assert data["status_code"] == 404
    assert "not found" in data["detail"].lower()


def test_list_hirer_briefs():
    """Verify /api/hirer-briefs and /api/briefs returns all 4 briefs."""
    response = client.get("/api/hirer-briefs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    brief_ids = [b["brief_id"] for b in data]
    assert "01_cafe_music_whatsapp" in brief_ids
    assert "02_skincare_photography_chat" in brief_ids
    assert "03_vertical_video_email" in brief_ids
    assert "04_leadership_event_photos" in brief_ids

    # Verify /api/briefs alias
    res_briefs = client.get("/api/briefs")
    assert res_briefs.status_code == 200
    assert len(res_briefs.json()) == 4


def test_get_hirer_brief_detail_success():
    """Verify /api/hirer-briefs/{brief_id} and /api/briefs/{brief_id} return complete structured brief."""
    response = client.get("/api/hirer-briefs/01_cafe_music_whatsapp")
    assert response.status_code == 200
    data = response.json()
    assert data["brief_id"] == "01_cafe_music_whatsapp"
    assert data["hirer_name"] == "Rhea"
    assert len(data["known_requirements"]) > 0
    assert len(data["hard_constraints"]) > 0
    assert len(data["unknowns"]) > 0

    # Verify /api/briefs/{brief_id} alias
    res_alias = client.get("/api/briefs/01_cafe_music_whatsapp")
    assert res_alias.status_code == 200
    assert res_alias.json()["brief_id"] == "01_cafe_music_whatsapp"


def test_get_hirer_brief_not_found():
    """Verify /api/hirer-briefs/{invalid_id} and /api/briefs/{invalid_id} return structured 404."""
    response = client.get("/api/hirer-briefs/invalid_brief_xyz")
    assert response.status_code == 404
    data = response.json()
    assert data["status_code"] == 404

    res_alias = client.get("/api/briefs/invalid_brief_xyz")
    assert res_alias.status_code == 404
    assert res_alias.json()["status_code"] == 404


def test_list_recommendations():
    """Verify /api/recommendations returns 4 recommendation summaries."""
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    for r in data:
        assert len(r["top_two"]) == 2


def test_get_recommendation_detail_success():
    """Verify /api/recommendations/{brief_id} returns full decision intelligence."""
    response = client.get("/api/recommendations/01_cafe_music_whatsapp")
    assert response.status_code == 200
    data = response.json()
    assert data["brief_id"] == "01_cafe_music_whatsapp"
    assert len(data["top_two"]) == 2
    assert data["top_two"][0]["rank"] == 1
    assert data["top_two"][1]["rank"] == 2
    assert len(data["top_two"][0]["supporting_evidence"]) > 0
    assert len(data["trade_off_analysis"]) >= 1
    assert 0 <= len(data["refinement_questions"]) <= 2


def test_get_recommendation_detail_not_found():
    """Verify /api/recommendations/{invalid_id} returns structured 404."""
    response = client.get("/api/recommendations/non_existent_brief")
    assert response.status_code == 404
    data = response.json()
    assert data["status_code"] == 404


def test_get_updated_recommendation_reranking_success():
    """Verify /api/recommendations/{brief_id}/updated returns follow-up re-ranking."""
    response = client.get("/api/recommendations/01_cafe_music_whatsapp/updated")
    assert response.status_code == 200
    data = response.json()
    assert data["brief_id"] == "01_cafe_music_whatsapp"
    assert data["follow_up_update_id"] == "01_cafe_music_update"
    assert len(data["initial_top_two"]) == 2
    assert len(data["updated_top_two"]) == 2
    assert len(data["rank_movements"]) == 2
    assert len(data["what_changed"]) > 0
    assert len(data["why_ranking_changed"]) > 0


def test_openapi_schema_available():
    """Verify OpenAPI schema is generated and accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "/api/health" in data["paths"]
    assert "/api/artists" in data["paths"]
    assert "/api/hirer-briefs" in data["paths"]
    assert "/api/recommendations" in data["paths"]
