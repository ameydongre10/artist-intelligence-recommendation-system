"""
Unit and Integration Tests for Dataset Inventory (Phase 1).
Validates dataset discovery, artist grouping, docx extraction, media integrity,
identifier inconsistencies, and inventory reproducibility.
"""

import os
import json
import pytest
from pathlib import Path
from scripts.inventory_dataset import scan_dataset, get_docx_text, parse_profile_text, inspect_media_file


@pytest.fixture(scope="module")
def raw_dir():
    """Returns the path to the extracted raw dataset."""
    path = Path("data/raw/Data set")
    assert path.exists(), f"Raw dataset directory not found at {path}"
    return str(path)


@pytest.fixture(scope="module")
def inventory_data(raw_dir):
    """Generates inventory dictionary for test assertions."""
    return scan_dataset(raw_dir)


def test_raw_dataset_structure_exists(raw_dir):
    """Verify that expected top-level dataset directories exist."""
    base = Path(raw_dir)
    assert (base / "artist_profiles").is_dir()
    assert (base / "hirer_conversations").is_dir()
    assert (base / "follow_up_update").is_dir()
    assert (base / "artist_profiles" / "photographers").is_dir()
    assert (base / "artist_profiles" / "musicians").is_dir()
    assert (base / "artist_profiles" / "video_editors").is_dir()


def test_total_file_count_and_reproducibility(raw_dir, inventory_data):
    """Verify total file count is 149 and scanning is deterministic."""
    assert inventory_data["dataset_metadata"]["total_files_discovered"] == 149
    
    # Second run to test exact determinism
    second_run = scan_dataset(raw_dir)
    assert inventory_data["dataset_metadata"]["total_files_discovered"] == second_run["dataset_metadata"]["total_files_discovered"]
    assert inventory_data["dataset_metadata"]["total_size_bytes"] == second_run["dataset_metadata"]["total_size_bytes"]
    assert inventory_data["file_type_distribution"] == second_run["file_type_distribution"]


def test_hirer_conversations_and_follow_up(inventory_data):
    """Verify 4 hirer conversations and 1 follow-up update."""
    assert len(inventory_data["hirer_conversations"]) == 4
    brief_ids = {b["brief_id"] for b in inventory_data["hirer_conversations"]}
    expected_briefs = {
        "01_cafe_music_whatsapp",
        "02_skincare_photography_chat",
        "03_vertical_video_email",
        "04_leadership_event_photos"
    }
    assert brief_ids == expected_briefs

    assert len(inventory_data["follow_up_updates"]) == 1
    assert inventory_data["follow_up_updates"][0]["update_id"] == "01_cafe_music_update"


def test_artist_counts_and_categories(inventory_data):
    """Verify exactly 15 artists across the 3 categories."""
    assert inventory_data["dataset_metadata"]["total_artists_discovered"] == 15
    photographers = inventory_data["artist_profiles"]["photographers"]
    musicians = inventory_data["artist_profiles"]["musicians"]
    video_editors = inventory_data["artist_profiles"]["video_editors"]

    assert len(photographers) == 5
    assert len(musicians) == 5
    assert len(video_editors) == 5


def test_all_artists_have_readable_profile_docx(inventory_data):
    """Verify that all 15 artists have a readable profile docx."""
    for cat in ["photographers", "musicians", "video_editors"]:
        for artist in inventory_data["artist_profiles"][cat]:
            pdoc = artist["profile_document"]
            assert pdoc is not None, f"Artist {artist['source_folder_name']} has no profile document"
            assert pdoc["integrity_status"] == "OK"
            assert pdoc["char_count"] > 0
            assert len(pdoc["raw_text"]) > 0


def test_identifier_inconsistencies_detected(inventory_data):
    """Verify that dataset inconsistencies are explicitly captured with INCONSISTENT status."""
    artists_by_folder = {}
    for cat in ["photographers", "musicians", "video_editors"]:
        for a in inventory_data["artist_profiles"][cat]:
            artists_by_folder[a["source_folder_name"]] = a

    # 1. PO4_Drift: Letter 'O' in folder ID, docx declares V05
    po4 = artists_by_folder["PO4_Drift"]
    assert po4["identifier_status"] == "INCONSISTENT"
    assert po4["profile_declared_id"] == "V05"
    assert any("letter 'O'" in msg for msg in po4["artist_anomalies"])

    # 2. PO5_Frames: Letter 'O' in folder ID, docx declares P04
    po5 = artists_by_folder["PO5_Frames"]
    assert po5["identifier_status"] == "INCONSISTENT"
    assert po5["profile_declared_id"] == "P04"

    # 3. V03_Rahul_Gupta: Name mismatch (Tara D'Souza declared in profile)
    v03 = artists_by_folder["V03_Rahul_Gupta"]
    assert v03["profile_declared_name"] == "Tara D'Souza"
    assert any("Tara D'Souza" in msg for msg in v03["artist_anomalies"])

    # 4. VO4_Shivam_media: Letter 'O' in folder ID, Work/ subfolder
    vo4 = artists_by_folder["VO4_Shivam_media"]
    assert vo4["identifier_status"] == "INCONSISTENT"
    assert vo4["media_summary"]["media_subfolder"] == "Work"

    # 5. VO5_Roshan: Letter 'O' in folder ID, docx declares V03
    vo5 = artists_by_folder["VO5_Roshan"]
    assert vo5["identifier_status"] == "INCONSISTENT"
    assert vo5["profile_declared_id"] == "V03"

    # 6. V02_Rehman_Ali: Docx has no ID header
    v02 = artists_by_folder["V02_Rehman_Ali"]
    assert v02["profile_declared_id"] is None
    assert any("no artist ID/name header" in msg for msg in v02["artist_anomalies"])


def test_media_files_integrity(inventory_data):
    """Verify that all media files across all artists have valid integrity and no corrupt/empty files."""
    total_media_count = 0
    for cat in ["photographers", "musicians", "video_editors"]:
        for artist in inventory_data["artist_profiles"][cat]:
            for mf in artist["media_summary"]["media_files"]:
                total_media_count += 1
                assert mf["integrity_status"] == "VALID", f"Media file {mf['relative_path']} failed: {mf['integrity_status']}"
                assert mf["size_bytes"] > 0

    assert total_media_count == 120  # 149 total - 15 docx - 5 txt - 9 .DS_Store = 120 media files


def test_generated_json_artifact_validity():
    """Verify data/processed/dataset_inventory.json exists and is valid JSON."""
    json_path = Path("data/processed/dataset_inventory.json")
    assert json_path.exists(), "dataset_inventory.json does not exist"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "dataset_metadata" in data
    assert "hirer_conversations" in data
    assert "follow_up_updates" in data
    assert "artist_profiles" in data
    assert "file_type_distribution" in data
    assert "system_files" in data
    assert "dataset_anomalies" in data
    assert "integrity_summary" in data
    assert data["dataset_metadata"]["total_artists_discovered"] == 15
