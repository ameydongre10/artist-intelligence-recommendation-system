"""
Comprehensive Tests for Phase 3: Artist Intelligence Pipeline.
Verifies processing of all 15 artists, JSONL schema validation, claim vs evidence separation,
evidence citations, unknown handling, anomaly preservation, and media selection logging.
"""

import os
import pytest
from src.intelligence.artist_intelligence import ArtistIntelligencePipeline
from src.models.artifacts import ArtistIntelligenceRecord
from src.models.common import EpistemicState, ArtistCategory, IdentifierStatus
from src.utils.file_utils import read_jsonl_file, read_json_file


@pytest.fixture(scope="module")
def processed_pipeline_data():
    """Fixture ensuring pipeline runs and returns generated records and logs."""
    pipeline = ArtistIntelligencePipeline()
    records = pipeline.process_all_artists()
    raw_jsonl = read_jsonl_file("data/processed/artist_intelligence.jsonl")
    media_log = read_json_file("data/processed/media_selection_log.json")
    return records, raw_jsonl, media_log


def test_exactly_fifteen_artists_processed(processed_pipeline_data):
    """Verify that exactly 15 artist records are generated in the JSONL artifact."""
    records, raw_jsonl, media_log = processed_pipeline_data
    assert len(records) == 15
    assert len(raw_jsonl) == 15
    assert media_log["total_artists_processed"] == 15


def test_all_jsonl_records_validate_against_schema(processed_pipeline_data):
    """Verify that every single JSON line parses cleanly into ArtistIntelligenceRecord."""
    _, raw_jsonl, _ = processed_pipeline_data
    for idx, raw_rec in enumerate(raw_jsonl):
        rec_obj = ArtistIntelligenceRecord.model_validate(raw_rec)
        assert rec_obj.artist_id is not None
        assert rec_obj.source_folder_name is not None
        assert rec_obj.category in [ArtistCategory.PHOTOGRAPHER, ArtistCategory.MUSICIAN, ArtistCategory.VIDEO_EDITOR]
        assert len(rec_obj.category_dimensions) > 0


def test_no_duplicate_artist_ids(processed_pipeline_data):
    """Verify no duplicate artist identifiers exist in the generated output."""
    records, _, _ = processed_pipeline_data
    folder_names = [r.source_folder_name for r in records]
    assert len(folder_names) == len(set(folder_names)) == 15


def test_claim_vs_demonstrated_evidence_separation(processed_pipeline_data):
    """Verify that profile claims and demonstrated capabilities remain strictly separated."""
    records, _, _ = processed_pipeline_data
    for r in records:
        # Every claim must have EpistemicState.CLAIM
        for clm in r.profile_claims:
            assert clm["epistemic_state"] == EpistemicState.CLAIM.value
            assert clm["is_demonstrated"] is False  # Claims are not conflated with evidence

        # Every demonstrated capability must have EpistemicState.DEMONSTRATED_EVIDENCE
        for dem in r.demonstrated_capabilities:
            assert dem["epistemic_state"] == EpistemicState.DEMONSTRATED_EVIDENCE.value
            assert len(dem["evidence_citations"]) >= 1  # Must have supporting citations


def test_evidence_citations_traceability(processed_pipeline_data):
    """Verify every demonstrated capability has traceable evidence citations citing valid files."""
    records, _, _ = processed_pipeline_data
    for r in records:
        for dem in r.demonstrated_capabilities:
            for cit in dem["evidence_citations"]:
                assert cit["file_name"] is not None
                assert cit["relative_path"] is not None
                assert len(cit["citation_text"]) > 0


def test_unknowns_do_not_equal_negative_capability(processed_pipeline_data):
    """Verify unknown dimensions are explicitly represented with reasons rather than negative scores."""
    records, _, _ = processed_pipeline_data
    for r in records:
        for ukn in r.unknowns:
            assert ukn["epistemic_state"] == EpistemicState.UNKNOWN.value
            assert len(ukn["reason"]) > 0
            assert ukn["is_blocker"] is False


def test_anomalies_preserved_accurately(processed_pipeline_data):
    """Verify dataset anomalies are preserved without arbitrary overrides."""
    records, _, _ = processed_pipeline_data
    records_by_folder = {r.source_folder_name: r for r in records}

    # PO4_Drift (folder has 'O', profile declared 'V05 / Drift')
    po4 = records_by_folder["PO4_Drift"]
    assert po4.identifier_status == IdentifierStatus.INCONSISTENT
    assert any("V05" in a or "mismatch" in a.lower() or "inconsistent" in a.lower() for a in po4.discrepancies_and_anomalies)

    # PO5_Frames (folder has 'O', profile declared 'P04 / Frames')
    po5 = records_by_folder["PO5_Frames"]
    assert po5.identifier_status == IdentifierStatus.INCONSISTENT

    # VO4_Shivam_media (nested Work/ subfolder)
    vo4 = records_by_folder["VO4_Shivam_media"]
    assert vo4.identifier_status == IdentifierStatus.INCONSISTENT
    assert any("Work" in a for a in vo4.discrepancies_and_anomalies)

    # VO5_Roshan (profile declared V03 / Roshan)
    vo5 = records_by_folder["VO5_Roshan"]
    assert vo5.identifier_status == IdentifierStatus.INCONSISTENT


def test_media_selection_log_integrity(processed_pipeline_data):
    """Verify media selection log tracks selected files and reasons for all 15 artists."""
    _, _, media_log = processed_pipeline_data
    assert media_log["total_artists_processed"] == 15
    assert len(media_log["artist_logs"]) == 15

    for artist_log in media_log["artist_logs"]:
        assert artist_log["artist_id"] is not None
        assert artist_log["total_media_available"] > 0
        assert artist_log["selected_samples_count"] > 0
        assert len(artist_log["selected_files"]) == artist_log["selected_samples_count"]
        assert len(artist_log["selection_rationale"]) > 0


def test_pipeline_determinism():
    """Verify running the pipeline multiple times produces identical output."""
    pipeline = ArtistIntelligencePipeline()
    run1 = [rec.model_dump() for rec in pipeline.process_all_artists()]
    run2 = [rec.model_dump() for rec in pipeline.process_all_artists()]
    assert run1 == run2
