"""
Comprehensive Tests for Phase 2: Core Project Foundation.
Tests domain schemas, epistemic state isolation, dataset loader, capability framework,
media selection policy, artifact contracts, and error handling.
"""

import pytest
from pydantic import ValidationError

from src.models.common import (
    EpistemicState,
    ArtistCategory,
    EvidenceStrength,
    ConfidenceLevel,
    ImportanceLevel,
    IdentifierStatus,
    MediaType
)
from src.models.evidence import (
    EvidenceCitation,
    DemonstratedCapability,
    ClaimedCapability
)
from src.models.artist import (
    ArtistIdentity,
    UnknownCapability,
    ProfileMetadata,
    ArtistRecord
)
from src.models.hirer import (
    RequirementItem,
    PreferenceItem,
    ConstraintItem,
    AssumptionItem,
    UnknownItem,
    ContradictionItem,
    HirerBrief
)
from src.models.recommendation import (
    RequirementMatch,
    TradeOffItem,
    RefinementQuestion,
    CandidateRecommendation,
    BriefRecommendation,
    RankMovement,
    ReRankingResult
)
from src.models.artifacts import (
    ArtistIntelligenceRecord,
    RecommendationsArtifact,
    UpdatedRecommendationArtifact
)
from src.ingestion.dataset_loader import DatasetLoader
from src.ingestion.profile_reader import read_profile_document
from src.ingestion.conversation_reader import read_conversation_file
from src.framework.capability_dimensions import (
    get_dimensions_for_category,
    PHOTOGRAPHER_DIMENSIONS,
    MUSICIAN_DIMENSIONS,
    VIDEO_EDITOR_DIMENSIONS
)
from src.processing.media_policy import (
    select_representative_media_files,
    format_evidence_reference
)
from src.utils.errors import (
    ArtistSystemError,
    FileNotFoundCustomError,
    InvalidSchemaError,
    InsufficientEvidenceError,
    IdentifierInconsistencyError
)
from src.utils.validation import validate_schema


def test_epistemic_state_isolation():
    """Verify that all four epistemic states are distinct and non-interchangeable."""
    assert EpistemicState.CLAIM != EpistemicState.DEMONSTRATED_EVIDENCE
    assert EpistemicState.DEMONSTRATED_EVIDENCE != EpistemicState.ASSUMPTION
    assert EpistemicState.ASSUMPTION != EpistemicState.UNKNOWN
    assert EpistemicState.UNKNOWN != EpistemicState.CLAIM

    states = {EpistemicState.CLAIM, EpistemicState.DEMONSTRATED_EVIDENCE, EpistemicState.ASSUMPTION, EpistemicState.UNKNOWN}
    assert len(states) == 4


def test_evidence_citation_and_demonstrated_capability_schema():
    """Verify that demonstrated capabilities require valid evidence citations."""
    citation = EvidenceCitation(
        evidence_id="EV_MA_cafe_demo",
        file_name="MA_cafe_demo_take1.wav",
        relative_path="artist_profiles/musicians/M01_Meera_Arjun/media/MA_cafe_demo_take1.wav",
        media_type=MediaType.AUDIO,
        timestamp_or_frame="0:00 - 1:30",
        observed_features=["Acoustic guitar live fingerpicking", "Dual vocal harmonies"],
        citation_text="Source: MA_cafe_demo_take1.wav [0:00-1:30] — Acoustic guitar live fingerpicking with dual harmonies"
    )
    assert citation.media_type == MediaType.AUDIO

    cap = DemonstratedCapability(
        capability_id="CAP_M01_ACOUSTIC",
        dimension="acoustic_live_performance",
        description="Demonstrated acoustic live performance with clean vocal harmonies in a cafe environment.",
        evidence_citations=[citation],
        evidence_strength=EvidenceStrength.STRONG,
        confidence=ConfidenceLevel.HIGH
    )
    assert cap.epistemic_state == EpistemicState.DEMONSTRATED_EVIDENCE
    assert len(cap.evidence_citations) == 1


def test_artist_identity_and_inconsistency_handling():
    """Verify artist identity model captures folder ID vs declared ID discrepancies."""
    # Consistent case
    p01 = ArtistIdentity(
        source_folder_name="P01_Aanya_Rao",
        source_folder_id="P01",
        profile_declared_id="P01",
        folder_declared_name="Aanya_Rao",
        profile_declared_name="Aanya Rao",
        identifier_status=IdentifierStatus.CONSISTENT
    )
    assert p01.identifier_status == IdentifierStatus.CONSISTENT

    # Inconsistent case (PO4_Drift declaring V05)
    po4 = ArtistIdentity(
        source_folder_name="PO4_Drift",
        source_folder_id="PO4",
        profile_declared_id="V05",
        folder_declared_name="Drift",
        profile_declared_name="Drift",
        identifier_status=IdentifierStatus.INCONSISTENT,
        discrepancy_notes="Folder uses letter 'O', profile declares 'V05 / Drift'"
    )
    assert po4.identifier_status == IdentifierStatus.INCONSISTENT
    assert po4.canonical_id is None  # Unresolved without evidence


def test_refinement_questions_limit_enforcement():
    """Verify that BriefRecommendation strictly enforces max 2 refinement questions."""
    q1 = RefinementQuestion(
        question_id="Q1",
        question_text="Will a portable PA be required or does venue provide sound?",
        why_it_matters="Resolves acoustic duo vs self-amplified act trade-off.",
        potential_ranking_impact="May favor solo act with minimal setup."
    )
    q2 = RefinementQuestion(
        question_id="Q2",
        question_text="What is the split between Hindi and English songs?",
        why_it_matters="Clarifies repertoire alignment.",
        potential_ranking_impact="Could elevate bilingual vocalists."
    )
    q3 = RefinementQuestion(
        question_id="Q3",
        question_text="Excessive question 3",
        why_it_matters="Not allowed",
        potential_ranking_impact="None"
    )

    rec1 = CandidateRecommendation(
        rank=1,
        artist_id="M01",
        artist_name="Meera & Arjun",
        category=ArtistCategory.MUSICIAN,
        fit_reason="Strong acoustic duo with cafe live demo recordings"
    )
    rec2 = CandidateRecommendation(
        rank=2,
        artist_id="M03",
        artist_name="Raghav Sen",
        category=ArtistCategory.MUSICIAN,
        fit_reason="Solo acoustic guitarist suitable for low volume background"
    )

    # Valid with 2 questions
    valid_brief_rec = BriefRecommendation(
        brief_id="01_cafe_music_whatsapp",
        hirer_name="Rhea",
        summary_of_need="Acoustic background live music for cafe",
        top_two=[rec1, rec2],
        refinement_questions=[q1, q2]
    )
    assert len(valid_brief_rec.refinement_questions) == 2

    # Invalid with 3 questions
    with pytest.raises(ValidationError):
        BriefRecommendation(
            brief_id="01_cafe_music_whatsapp",
            hirer_name="Rhea",
            summary_of_need="Acoustic background live music for cafe",
            top_two=[rec1, rec2],
            refinement_questions=[q1, q2, q3]
        )


def test_top_two_count_enforcement():
    """Verify that BriefRecommendation strictly requires exactly 2 ranked artists."""
    rec1 = CandidateRecommendation(
        rank=1,
        artist_id="M01",
        artist_name="Meera & Arjun",
        category=ArtistCategory.MUSICIAN,
        fit_reason="Fit reason"
    )
    # Only 1 artist should fail
    with pytest.raises(ValidationError):
        BriefRecommendation(
            brief_id="01_cafe_music_whatsapp",
            hirer_name="Rhea",
            summary_of_need="Need",
            top_two=[rec1]
        )


def test_dataset_loader_safe_operations():
    """Verify that DatasetLoader retrieves all 15 artists, 4 briefs, and 1 follow-up."""
    loader = DatasetLoader()
    inv = loader.load_inventory()
    assert inv is not None

    meta = loader.get_metadata()
    assert meta["total_artists_discovered"] == 15
    assert meta["total_hirer_conversations"] == 4
    assert meta["total_follow_up_updates"] == 1

    # Artists by category
    photographers = loader.get_all_artists(ArtistCategory.PHOTOGRAPHER)
    musicians = loader.get_all_artists(ArtistCategory.MUSICIAN)
    editors = loader.get_all_artists(ArtistCategory.VIDEO_EDITOR)
    assert len(photographers) == 5
    assert len(musicians) == 5
    assert len(editors) == 5

    # Retrieve specific artists by various identifiers
    m01 = loader.get_artist_by_identifier("M01")
    assert m01 is not None
    assert m01["source_folder_name"] == "M01_Meera_Arjun"

    po4 = loader.get_artist_by_identifier("PO4_Drift")
    assert po4 is not None
    assert po4["identifier_status"] == "INCONSISTENT"

    vo4 = loader.get_artist_by_identifier("VO4")
    assert vo4 is not None
    assert vo4["media_summary"]["media_subfolder"] == "Work"

    # Hirer briefs retrieval
    cafe_brief = loader.get_hirer_conversation_by_id("01_cafe_music_whatsapp")
    assert cafe_brief is not None
    assert "live music" in cafe_brief["raw_content"]

    # Follow up retrieval
    follow_up = loader.get_follow_up_by_id("01_cafe_music_update")
    assert follow_up is not None
    assert "launch night" in follow_up["raw_content"]


def test_profile_reader_and_conversation_reader():
    """Verify profile_reader and conversation_reader on actual extracted raw files."""
    loader = DatasetLoader()
    m01_info = loader.get_artist_by_identifier("M01")
    docx_rel = m01_info["profile_document"]["relative_path"]
    docx_full = f"data/raw/{docx_rel}"

    raw_text, meta = read_profile_document(docx_full)
    assert len(raw_text) > 0
    assert meta.location == "Delhi NCR, India"

    conv_info = loader.get_hirer_conversation_by_id("01_cafe_music_whatsapp")
    conv_full = f"data/raw/{conv_info['relative_path']}"
    conv_data = read_conversation_file(conv_full)
    assert conv_data["line_count"] > 0
    assert "Rhea" in conv_data["raw_text"]


def test_category_capability_framework():
    """Verify capability dimension definitions for all 3 categories."""
    photo_dims = get_dimensions_for_category(ArtistCategory.PHOTOGRAPHER)
    music_dims = get_dimensions_for_category(ArtistCategory.MUSICIAN)
    editor_dims = get_dimensions_for_category(ArtistCategory.VIDEO_EDITOR)

    assert "product_commercial_photography" in photo_dims
    assert "candid_event_coverage" in photo_dims
    assert "acoustic_live_performance" in music_dims
    assert "ambient_background_suitability" in music_dims
    assert "vertical_short_form_editing" in editor_dims
    assert "narrative_curation_from_raw_clips" in editor_dims

    for dim_id, dim_def in photo_dims.items():
        assert dim_def.category == ArtistCategory.PHOTOGRAPHER
        assert len(dim_def.observable_evidence_signals) > 0


def test_media_selection_policy():
    """Verify representative media sampling logic."""
    sample_media = [
        {"filename": "raw_shot_01.mp4", "size_bytes": 10_000_000, "integrity_status": "VALID"},
        {"filename": "NK_food_reel_cut.mp4", "size_bytes": 5_000_000, "integrity_status": "VALID"},
        {"filename": "event_recap_edit.mp4", "size_bytes": 8_000_000, "integrity_status": "VALID"},
        {"filename": "broll_clip.mov", "size_bytes": 12_000_000, "integrity_status": "VALID"},
        {"filename": "ambient_cafe_take.mp4", "size_bytes": 4_000_000, "integrity_status": "VALID"},
        {"filename": "huge_dump_file.mp4", "size_bytes": 95_000_000, "integrity_status": "VALID"}
    ]

    selected = select_representative_media_files(sample_media, ArtistCategory.VIDEO_EDITOR, max_samples=3)
    assert len(selected) == 3
    selected_names = [s["filename"] for s in selected]
    # 'food', 'reel', 'event', 'edit', 'cafe' have priority
    assert "NK_food_reel_cut.mp4" in selected_names
    assert "event_recap_edit.mp4" in selected_names


def test_artifact_contracts_validation():
    """Verify schemas for the 3 mandatory assignment output files."""
    # 1. Artist Intelligence line record
    artist_line = ArtistIntelligenceRecord(
        artist_id="M01",
        source_folder_name="M01_Meera_Arjun",
        category=ArtistCategory.MUSICIAN,
        declared_name="Meera & Arjun",
        identifier_status=IdentifierStatus.CONSISTENT,
        profile_claims=[{"claim": "Acoustic duo", "dimension": "acoustic_live_performance"}],
        category_dimensions={"acoustic_live_performance": "STRONG", "ambient_background_suitability": "HIGH"},
        demonstrated_capabilities=[{"dimension": "acoustic_live_performance", "evidence": "MA_cafe_demo_take1.wav"}],
        unknowns=[{"dimension": "studio_multitrack_production", "reason": "No multitrack DAW sessions provided"}],
        confidence=ConfidenceLevel.HIGH
    )
    assert artist_line.artist_id == "M01"

    # 2. Recommendations Artifact
    rec1 = CandidateRecommendation(
        rank=1,
        artist_id="M01",
        artist_name="Meera & Arjun",
        category=ArtistCategory.MUSICIAN,
        fit_reason="Strong acoustic live demo in cafe environment"
    )
    rec2 = CandidateRecommendation(
        rank=2,
        artist_id="M03",
        artist_name="Raghav Sen",
        category=ArtistCategory.MUSICIAN,
        fit_reason="Solo acoustic folk repertoire"
    )
    brief_rec = BriefRecommendation(
        brief_id="01_cafe_music_whatsapp",
        hirer_name="Rhea",
        summary_of_need="Acoustic background music",
        top_two=[rec1, rec2],
        refinement_questions=[
            RefinementQuestion(
                question_id="Q1",
                question_text="Will PA system be available?",
                why_it_matters="Affects setup needs.",
                potential_ranking_impact="Favors self-amplified duo."
            )
        ]
    )
    rec_artifact = RecommendationsArtifact(
        metadata={"generator": "Artist Intelligence Engine v1.0"},
        recommendations=[brief_rec]
    )
    assert len(rec_artifact.recommendations) == 1

    # 3. Updated Recommendation Artifact
    rerank_result = ReRankingResult(
        brief_id="01_cafe_music_whatsapp",
        follow_up_update_id="01_cafe_music_update",
        follow_up_summary="Management made it launch night headline set with ₹15k budget",
        initial_top_two=[rec1, rec2],
        updated_top_two=[rec1, rec2],
        rank_movements=[
            RankMovement(
                artist_id="M01",
                artist_name="Meera & Arjun",
                previous_rank=1,
                updated_rank=1,
                movement="STABLE",
                reason="Duo format possesses headline dynamism required for launch night"
            )
        ],
        what_changed="Shifted from 3-hr ambient background to 45-min headline set, budget increased to 15k",
        why_ranking_changed="M01 retained top rank due to demonstrated upbeat rehearsal medley"
    )
    updated_artifact = UpdatedRecommendationArtifact(
        metadata={"generator": "Artist Intelligence Engine v1.0"},
        reranking=rerank_result
    )
    assert updated_artifact.reranking.brief_id == "01_cafe_music_whatsapp"


def test_custom_error_formatting():
    """Verify that custom errors format into structured dictionaries."""
    err = InsufficientEvidenceError("P03", "product_commercial_photography")
    d = err.to_dict()
    assert d["success"] is False
    assert d["error"]["code"] == "INSUFFICIENT_EVIDENCE"
    assert "P03" in d["error"]["details"]["artist_id"]
