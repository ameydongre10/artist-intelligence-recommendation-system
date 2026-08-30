"""
Comprehensive Tests for Phase 4: Hirer Intelligence & Intent Extraction.
Verifies structured requirement extraction, classification into hard constraints,
preferences, deliverables, assumptions, unknowns, ambiguities, contradictions,
and follow-up update traceability.
"""

import pytest
from src.intelligence.hirer_intelligence import HirerIntelligencePipeline
from src.models.hirer import (
    HirerIntelligenceArtifact,
    HirerBrief,
    FollowUpUpdateRecord
)
from src.models.common import EpistemicState, ArtistCategory, ImportanceLevel
from src.utils.file_utils import read_json_file, read_jsonl_file


@pytest.fixture(scope="module")
def hirer_intelligence_artifact():
    """Fixture to run Hirer Intelligence pipeline and load validated artifact."""
    pipeline = HirerIntelligencePipeline()
    artifact = pipeline.process_all_briefs()
    raw_data = read_json_file("data/processed/hirer_intelligence.json")
    return artifact, raw_data


def test_exactly_four_briefs_processed(hirer_intelligence_artifact):
    """Verify all 4 hirer briefs are processed and present in the artifact."""
    artifact, raw_data = hirer_intelligence_artifact
    assert len(artifact.briefs) == 4
    assert len(raw_data["briefs"]) == 4

    brief_ids = [b.brief_id for b in artifact.briefs]
    assert "01_cafe_music_whatsapp" in brief_ids
    assert "02_skincare_photography_chat" in brief_ids
    assert "03_vertical_video_email" in brief_ids
    assert "04_leadership_event_photos" in brief_ids


def test_follow_up_update_processed_separately(hirer_intelligence_artifact):
    """Verify follow-up update is processed as a separate structured record."""
    artifact, raw_data = hirer_intelligence_artifact
    assert len(artifact.follow_up_updates) == 1
    assert len(raw_data["follow_up_updates"]) == 1

    fu = artifact.follow_up_updates[0]
    assert fu.update_id == "01_cafe_music_update"
    assert fu.related_brief_id == "01_cafe_music_whatsapp"
    assert len(fu.changes_detected) >= 3
    assert len(fu.new_hard_constraints) >= 2


def test_requirements_traceability_to_source_quotes(hirer_intelligence_artifact):
    """Verify every requirement, preference, and constraint includes source quotes."""
    artifact, _ = hirer_intelligence_artifact
    for brief in artifact.briefs:
        for req in brief.known_requirements:
            assert req.source_quote is not None
            assert len(req.source_quote) > 0
            assert req.epistemic_state == EpistemicState.CLAIM

        for constr in brief.hard_constraints:
            assert constr.source_quote is not None
            assert len(constr.source_quote) > 0

        for pref in brief.preferences:
            assert pref.source_quote is not None
            assert len(pref.source_quote) > 0


def test_epistemic_discipline_and_unknowns_handling(hirer_intelligence_artifact):
    """Verify unknowns and assumptions maintain explicit epistemic states."""
    artifact, _ = hirer_intelligence_artifact
    for brief in artifact.briefs:
        for ukn in brief.unknowns:
            assert ukn.epistemic_state == EpistemicState.UNKNOWN
            assert len(ukn.why_it_matters) > 0

        for asm in brief.assumptions:
            assert asm.epistemic_state == EpistemicState.ASSUMPTION
            assert len(asm.rationale) > 0
            assert len(asm.risk_impact) > 0


def test_ambiguity_vs_contradiction_separation(hirer_intelligence_artifact):
    """Verify ambiguities and contradictions are kept distinct."""
    artifact, _ = hirer_intelligence_artifact
    briefs_by_id = {b.brief_id: b for b in artifact.briefs}

    # Brief 04 has a clear contradiction (asking for headshots during tight conference schedule)
    lead_brief = briefs_by_id["04_leadership_event_photos"]
    assert len(lead_brief.contradictions) == 1
    assert "headshot" in lead_brief.contradictions[0].statement_a.lower()

    # Brief 01 has an ambiguity (vague PA equipment status)
    cafe_brief = briefs_by_id["01_cafe_music_whatsapp"]
    assert len(cafe_brief.ambiguities) == 1
    assert len(cafe_brief.ambiguities[0].possible_interpretations) >= 2


def test_category_alignment_for_briefs(hirer_intelligence_artifact):
    """Verify target category mapping for all 4 briefs."""
    artifact, _ = hirer_intelligence_artifact
    briefs_by_id = {b.brief_id: b for b in artifact.briefs}

    assert briefs_by_id["01_cafe_music_whatsapp"].target_category == ArtistCategory.MUSICIAN
    assert briefs_by_id["02_skincare_photography_chat"].target_category == ArtistCategory.PHOTOGRAPHER
    assert briefs_by_id["03_vertical_video_email"].target_category == ArtistCategory.VIDEO_EDITOR
    assert briefs_by_id["04_leadership_event_photos"].target_category == ArtistCategory.PHOTOGRAPHER


def test_artist_intelligence_jsonl_remains_unmodified():
    """Verify artist_intelligence.jsonl was not touched or modified during Phase 4."""
    records = read_jsonl_file("data/processed/artist_intelligence.jsonl")
    assert len(records) == 15
