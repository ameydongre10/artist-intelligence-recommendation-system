"""
Comprehensive Tests for Phase 5: Matching, Ranking & Decision Intelligence.
Verifies category isolation, deterministic scoring, Top 2 recommendations,
evidence citation validity, trade-off generation, max 2 refinement questions,
and follow-up re-ranking with before/after comparisons.
"""

import os
import pytest
from src.matching.engine import RecommendationEngine
from src.matching.scorer import calculate_match_score
from src.models.artifacts import (
    ArtistIntelligenceRecord,
    RecommendationsArtifact,
    UpdatedRecommendationArtifact
)
from src.models.hirer import HirerIntelligenceArtifact
from src.utils.file_utils import read_json_file, read_jsonl_file


@pytest.fixture(scope="module")
def recommendation_artifacts():
    """Fixture to execute recommendation engine and load validated artifacts."""
    engine = RecommendationEngine()
    recs_art, upd_art = engine.run()
    
    recs_raw = read_json_file("data/processed/recommendations.json")
    upd_raw = read_json_file("data/processed/updated_recommendation.json")
    
    return recs_art, upd_art, recs_raw, upd_raw


def test_exactly_four_brief_recommendations(recommendation_artifacts):
    """Verify exactly 4 brief recommendations exist."""
    recs_art, _, recs_raw, _ = recommendation_artifacts
    assert len(recs_art.recommendations) == 4
    assert len(recs_raw["recommendations"]) == 4

    brief_ids = [r.brief_id for r in recs_art.recommendations]
    assert "01_cafe_music_whatsapp" in brief_ids
    assert "02_skincare_photography_chat" in brief_ids
    assert "03_vertical_video_email" in brief_ids
    assert "04_leadership_event_photos" in brief_ids


def test_exactly_two_ranked_recommendations_per_brief(recommendation_artifacts):
    """Verify each brief has exactly Rank 1 and Rank 2 recommendations."""
    recs_art, _, _, _ = recommendation_artifacts
    for rec in recs_art.recommendations:
        assert len(rec.top_two) == 2
        assert rec.top_two[0].rank == 1
        assert rec.top_two[1].rank == 2
        assert rec.top_two[0].artist_id != rec.top_two[1].artist_id


def test_category_isolation_enforced(recommendation_artifacts):
    """Verify candidates are strictly matched within target category."""
    recs_art, _, _, _ = recommendation_artifacts
    for rec in recs_art.recommendations:
        if "music" in rec.brief_id:
            assert all(c.category.value == "musician" for c in rec.top_two)
        elif "skincare" in rec.brief_id or "leadership" in rec.brief_id:
            assert all(c.category.value == "photographer" for c in rec.top_two)
        elif "video" in rec.brief_id:
            assert all(c.category.value == "video_editor" for c in rec.top_two)


def test_supporting_evidence_citations_validity(recommendation_artifacts):
    """Verify every recommended artist has traceable, non-empty evidence citations."""
    recs_art, _, _, _ = recommendation_artifacts
    for rec in recs_art.recommendations:
        for cand in rec.top_two:
            assert len(cand.supporting_evidence) > 0
            for cit in cand.supporting_evidence:
                assert cit.evidence_id.startswith("EV_")
                assert cit.file_name is not None
                assert len(cit.observed_features) > 0


def test_refinement_questions_limit_and_impact(recommendation_artifacts):
    """Verify refinement questions are at most 2 and contain decision impact explanations."""
    recs_art, _, _, _ = recommendation_artifacts
    for rec in recs_art.recommendations:
        assert 0 <= len(rec.refinement_questions) <= 2
        for q in rec.refinement_questions:
            assert len(q.question_text) > 0
            assert len(q.why_it_matters) > 0
            assert len(q.potential_ranking_impact) > 0


def test_trade_offs_generated_for_each_brief(recommendation_artifacts):
    """Verify trade-offs exist comparing Rank 1 and Rank 2."""
    recs_art, _, _, _ = recommendation_artifacts
    for rec in recs_art.recommendations:
        assert len(rec.trade_off_analysis) >= 1
        for to in rec.trade_off_analysis:
            assert len(to.rank_1_status) > 0
            assert len(to.rank_2_status) > 0
            assert len(to.decision_implication) > 0


def test_follow_up_reranking_structure_and_explanation(recommendation_artifacts):
    """Verify follow-up update re-ranking preserves initial top 2 and explains movements."""
    _, upd_art, _, upd_raw = recommendation_artifacts
    rerank = upd_art.reranking

    assert rerank.brief_id == "01_cafe_music_whatsapp"
    assert rerank.follow_up_update_id == "01_cafe_music_update"
    assert len(rerank.initial_top_two) == 2
    assert len(rerank.updated_top_two) == 2
    assert len(rerank.rank_movements) == 2
    assert len(rerank.what_changed) > 0
    assert len(rerank.why_ranking_changed) > 0

    # Ensure M01 is Rank 1 in both
    assert rerank.updated_top_two[0].artist_id == "M01"
    assert rerank.updated_top_two[1].artist_id == "M03"


def test_unknown_information_is_not_penalized():
    """Verify an artist with UNKNOWN capabilities is not assigned a negative score penalty."""
    artists = [ArtistIntelligenceRecord.model_validate(r) for r in read_jsonl_file("data/processed/artist_intelligence.jsonl")]
    hirer_art = HirerIntelligenceArtifact.model_validate(read_json_file("data/processed/hirer_intelligence.json"))
    brief = hirer_art.briefs[0]

    # For Raghav Sen (M03), headline dynamism is UNKNOWN, but penalty_score should be 0.0
    m03 = next(a for a in artists if a.artist_id == "M03")
    score = calculate_match_score(m03, brief)
    assert score.penalty_score == 0.0
    assert score.total_score > 0.0


def test_engine_determinism():
    """Verify running recommendation engine multiple times produces identical results."""
    engine = RecommendationEngine()
    rec1, upd1 = engine.run()
    rec2, upd2 = engine.run()

    assert rec1.model_dump() == rec2.model_dump()
    assert upd1.model_dump() == upd2.model_dump()
