"""
Remediation and Verification Tests for AIRS.
Proves:
1. Documented scoring formula exactly matches implementation.
2. UNKNOWN receives zero positive or negative penalty.
3. Artist IDs alone do NOT control scoring (capability and evidence driven).
4. Recommendation fit reasons and trade-offs are dynamically derived from scoring data.
5. Re-ranking genuinely runs generic scoring/ranking on updated brief parameters.
6. Changing follow-up parameters shifts scores and rankings dynamically.
"""

import pytest
from src.models.common import (
    ArtistCategory,
    EvidenceStrength,
    ConfidenceLevel,
    ImportanceLevel,
    EpistemicState,
    IdentifierStatus,
    MediaType
)
from src.models.artifacts import ArtistIntelligenceRecord
from src.models.hirer import (
    HirerBrief,
    ContextInfo,
    RequirementItem,
    ConstraintItem,
    PreferenceItem,
    FollowUpUpdateRecord
)
from src.models.recommendation import CandidateRecommendation, BriefRecommendation
from src.matching.scorer import calculate_match_score, ScoreBreakdown
from src.matching.ranking import rank_artists_for_brief, _synthesize_fit_reason
from src.matching.tradeoffs import generate_trade_offs_for_brief
from src.matching.reranking import process_follow_up_reranking, _apply_follow_up_to_brief


def _make_mock_artist(
    artist_id: str,
    name: str,
    category: ArtistCategory,
    demonstrated_dims: list,
    claimed_dims: list = None,
    unknown_dims: list = None,
    conf: ConfidenceLevel = ConfidenceLevel.HIGH
) -> ArtistIntelligenceRecord:
    claimed_dims = claimed_dims or []
    unknown_dims = unknown_dims or []
    
    demo_caps = [
        {
            "capability_id": f"CAP_{d.upper()}",
            "dimension": d,
            "description": f"Demonstrated {d}",
            "evidence_citations": [
                {
                    "evidence_id": f"EV_{artist_id}_{d}",
                    "file_name": f"{d}.wav",
                    "relative_path": f"media/{d}.wav",
                    "media_type": "audio",
                    "timestamp_or_frame": "0:00-1:00",
                    "observed_features": [f"Feature {d}"],
                    "citation_text": f"Verified asset for {d}"
                }
            ],
            "evidence_strength": "STRONG",
            "confidence": "HIGH",
            "epistemic_state": "DEMONSTRATED_EVIDENCE"
        }
        for d in demonstrated_dims
    ]
    
    claims = [
        {
            "claim_id": f"CLM_{c.upper()}",
            "dimension": c,
            "claimed_attribute": f"Claims {c}",
            "description": f"Self-reported {c}",
            "confidence": "LOW",
            "epistemic_state": "CLAIM"
        }
        for c in claimed_dims
    ]
    
    unknowns = [
        {
            "unknown_id": f"UKN_{u.upper()}",
            "dimension": u,
            "reason": f"No evidence for {u}",
            "is_blocker": False,
            "epistemic_state": "UNKNOWN"
        }
        for u in unknown_dims
    ]
    
    cat_dims = {}
    for d in demonstrated_dims:
        cat_dims[d] = {"status": "DEMONSTRATED_EVIDENCE", "strength": "STRONG", "confidence": "HIGH"}
    for c in claimed_dims:
        cat_dims[c] = {"status": "CLAIM", "strength": "UNVERIFIED_CLAIM", "confidence": "LOW"}
    for u in unknown_dims:
        cat_dims[u] = {"status": "UNKNOWN", "strength": "INSUFFICIENT", "confidence": "UNKNOWN"}

    return ArtistIntelligenceRecord(
        artist_id=artist_id,
        source_folder_name=f"{artist_id}_{name}",
        category=category,
        declared_name=name,
        identifier_status=IdentifierStatus.CONSISTENT,
        profile_claims=claims,
        category_dimensions=cat_dims,
        demonstrated_capabilities=demo_caps,
        unknowns=unknowns,
        confidence=conf,
        discrepancies_and_anomalies=[]
    )


def _make_mock_brief(
    brief_id: str,
    category: ArtistCategory,
    required_dims: list,
    importance_map: dict = None
) -> HirerBrief:
    importance_map = importance_map or {}
    reqs = [
        RequirementItem(
            requirement_id=f"REQ_{d.upper()}",
            dimension=d,
            description=f"Must have {d}",
            importance=importance_map.get(d, ImportanceLevel.HIGH),
            source_quote=f"Need {d}"
        )
        for d in required_dims
    ]
    
    return HirerBrief(
        brief_id=brief_id,
        hirer_name="Test Hirer",
        channel="whatsapp",
        source_file="test.txt",
        target_category=category,
        raw_text="Test conversation",
        context=ContextInfo(
            situation="Test gig",
            location_or_venue="Delhi",
            target_date_or_timeline="Next Friday",
            audience_or_scale="80 guests"
        ),
        known_requirements=reqs,
        preferences=[],
        hard_constraints=[],
        deliverables=[],
        assumptions=[],
        unknowns=[],
        ambiguities=[],
        contradictions=[],
        decision_critical_factors=[]
    )


def test_scoring_formula_exact_mathematical_breakdown():
    """Verify the exact additive formula: Req Fit + Evidence Strength + Constraint Fit - Penalty."""
    artist = _make_mock_artist(
        artist_id="CUSTOM_01",
        name="Artist Alpha",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=["acoustic_live_performance", "vocal_capability_and_repertoire"],
        claimed_dims=[],
        unknown_dims=["ambient_background_suitability"]
    )
    brief = _make_mock_brief(
        brief_id="brief_test",
        category=ArtistCategory.MUSICIAN,
        required_dims=["acoustic_live_performance", "vocal_capability_and_repertoire"]
    )
    
    score = calculate_match_score(artist, brief)
    # Total reqs = 2. max_req_pts = 25.0 per req.
    # Importance is HIGH (1.0). Strength is STRONG (1.0).
    # Req Fit = 25.0 * 1.0 * 1.0 + 25.0 * 1.0 * 1.0 = 50.0
    assert score.requirement_fit_score == 50.0
    # Evidence bonus: 2 STRONG demonstrated = 6.0 + 6.0 = 12.0
    assert score.evidence_strength_score == 12.0
    # Constraint compatibility baseline = 20.0
    assert score.constraint_compatibility_score == 20.0
    # Penalty = 0.0
    assert score.penalty_score == 0.0
    # Total = 50 + 12 + 20 - 0 = 82.0
    assert score.total_score == 82.0


def test_unknown_information_is_strictly_neutral():
    """Verify UNKNOWN requirements contribute 0 points and deduct 0 points (no penalty)."""
    artist_with_unknowns = _make_mock_artist(
        artist_id="CUSTOM_UNK",
        name="Artist Unk",
        category=ArtistCategory.PHOTOGRAPHER,
        demonstrated_dims=["candid_event_coverage"],
        unknown_dims=["portraiture_and_headshots", "turnaround_and_digital_delivery"]
    )
    brief = _make_mock_brief(
        brief_id="brief_photo",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage", "portraiture_and_headshots"]
    )
    
    score = calculate_match_score(artist_with_unknowns, brief)
    assert score.penalty_score == 0.0
    assert "portraiture_and_headshots" in score.unmatched_unknowns


def test_changing_artist_id_alone_does_not_change_scoring():
    """Verify that two artists with different IDs but identical capabilities score identically."""
    artist_a = _make_mock_artist(
        artist_id="AAA_99",
        name="Artist A",
        category=ArtistCategory.VIDEO_EDITOR,
        demonstrated_dims=["vertical_short_form_editing", "food_and_hospitality_content"]
    )
    artist_b = _make_mock_artist(
        artist_id="ZZZ_00",
        name="Artist Z",
        category=ArtistCategory.VIDEO_EDITOR,
        demonstrated_dims=["vertical_short_form_editing", "food_and_hospitality_content"]
    )
    brief = _make_mock_brief(
        brief_id="brief_vid",
        category=ArtistCategory.VIDEO_EDITOR,
        required_dims=["vertical_short_form_editing", "food_and_hospitality_content"]
    )
    
    score_a = calculate_match_score(artist_a, brief)
    score_b = calculate_match_score(artist_b, brief)
    assert score_a.total_score == score_b.total_score
    assert score_a.requirement_fit_score == score_b.requirement_fit_score
    assert score_a.evidence_strength_score == score_b.evidence_strength_score


def test_scoring_is_purely_capability_and_evidence_driven():
    """Verify demonstrated evidence scores higher than unverified claims, which score higher than unknown."""
    artist_demo = _make_mock_artist(
        artist_id="DEMO_ARTIST",
        name="Demo Artist",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=["acoustic_live_performance"]
    )
    artist_claim = _make_mock_artist(
        artist_id="CLAIM_ARTIST",
        name="Claim Artist",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=[],
        claimed_dims=["acoustic_live_performance"]
    )
    artist_unk = _make_mock_artist(
        artist_id="UNK_ARTIST",
        name="Unk Artist",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=[],
        unknown_dims=["acoustic_live_performance"]
    )
    brief = _make_mock_brief(
        brief_id="brief_mus",
        category=ArtistCategory.MUSICIAN,
        required_dims=["acoustic_live_performance"]
    )
    
    score_demo = calculate_match_score(artist_demo, brief)
    score_claim = calculate_match_score(artist_claim, brief)
    score_unk = calculate_match_score(artist_unk, brief)
    
    assert score_demo.total_score > score_claim.total_score > score_unk.total_score
    assert score_demo.evidence_strength_score > score_claim.evidence_strength_score
    assert score_claim.evidence_strength_score > score_unk.evidence_strength_score


def test_trade_offs_change_when_capability_differences_change():
    """Verify trade-off analysis generates differences based on actual dimension coverage."""
    artist_1 = _make_mock_artist(
        artist_id="R1_ARTIST",
        name="Rank 1 Artist",
        category=ArtistCategory.PHOTOGRAPHER,
        demonstrated_dims=["candid_event_coverage"],
        unknown_dims=["group_and_team_framing"]
    )
    artist_2 = _make_mock_artist(
        artist_id="R2_ARTIST",
        name="Rank 2 Artist",
        category=ArtistCategory.PHOTOGRAPHER,
        demonstrated_dims=["group_and_team_framing"],
        unknown_dims=["candid_event_coverage"]
    )
    brief = _make_mock_brief(
        brief_id="brief_photo_tradeoff",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage", "group_and_team_framing"]
    )
    
    s1 = calculate_match_score(artist_1, brief)
    s2 = calculate_match_score(artist_2, brief)
    trade_offs = generate_trade_offs_for_brief(brief, s1, s2)
    
    assert len(trade_offs) >= 2
    dims = {t.dimension for t in trade_offs}
    assert "candid_event_coverage" in dims
    assert "group_and_team_framing" in dims


def test_reranking_score_shifts_with_follow_up_parameters():
    """Verify changing follow-up parameters dynamically re-scores candidates and shifts margins."""
    artist_m01 = _make_mock_artist(
        artist_id="M01_TEST",
        name="Meera & Arjun",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=["acoustic_live_performance", "headline_stage_dynamism", "ambient_background_suitability"]
    )
    artist_m03 = _make_mock_artist(
        artist_id="M03_TEST",
        name="Raghav Sen",
        category=ArtistCategory.MUSICIAN,
        demonstrated_dims=["acoustic_live_performance", "ambient_background_suitability"],
        unknown_dims=["headline_stage_dynamism"]
    )
    
    initial_brief = _make_mock_brief(
        brief_id="brief_cafe",
        category=ArtistCategory.MUSICIAN,
        required_dims=["ambient_background_suitability", "acoustic_live_performance"]
    )
    
    follow_up = FollowUpUpdateRecord(
        update_id="test_update",
        related_brief_id="brief_cafe",
        source_file="test_update.txt",
        update_summary="Scope changed to 45-min headline showcase",
        raw_text="need headline set",
        changes_detected=[
            {
                "parameter": "event_energy_and_headline",
                "initial_value": "ambient background",
                "updated_value": "headline showcase set for 80 guests",
                "source_quote": "need a proper 45 min headline set"
            }
        ],
        new_hard_constraints=[],
        modified_preferences=[],
        remaining_unknowns=[]
    )
    
    init_rec = rank_artists_for_brief(initial_brief, [artist_m01, artist_m03])
    
    rerank_result = process_follow_up_reranking(
        initial_recommendation=init_rec,
        follow_up_record=follow_up,
        all_artists=[artist_m01, artist_m03],
        initial_brief=initial_brief
    )
    
    assert rerank_result.brief_id == "brief_cafe"
    assert len(rerank_result.updated_top_two) == 2
    assert rerank_result.updated_top_two[0].artist_id == "M01_TEST"
    assert rerank_result.updated_top_two[1].artist_id == "M03_TEST"
    assert "headline_stage_dynamism" in rerank_result.why_ranking_changed.lower()


def test_changing_hirer_requirement_weight_changes_candidate_scores():
    """TEST 1: Change a hirer requirement weight. Verify candidate scores change accordingly."""
    artist = _make_mock_artist(
        artist_id="WEIGHT_TEST",
        name="Weight Test Artist",
        category=ArtistCategory.PHOTOGRAPHER,
        demonstrated_dims=["candid_event_coverage"]
    )
    brief_standard = _make_mock_brief(
        brief_id="brief_std",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage"],
        importance_map={"candid_event_coverage": ImportanceLevel.HIGH}
    )
    brief_critical = _make_mock_brief(
        brief_id="brief_crit",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage"],
        importance_map={"candid_event_coverage": ImportanceLevel.CRITICAL}
    )
    
    score_std = calculate_match_score(artist, brief_standard)
    score_crit = calculate_match_score(artist, brief_critical)
    # Critical multiplier is 1.2 vs Standard 1.0 (capped at max 50 pts)
    # With 1 requirement of 50 pts, std gets 50*1.0 = 50.0, crit gets min(50*1.2, 50) = 50.0
    # With 2 requirements (25 pts each), std gets 25*1.0 = 25.0, crit gets 25*1.2 = 30.0
    brief_std_2 = _make_mock_brief(
        brief_id="brief_std_2",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage", "portraiture_and_headshots"],
        importance_map={"candid_event_coverage": ImportanceLevel.HIGH, "portraiture_and_headshots": ImportanceLevel.HIGH}
    )
    brief_crit_2 = _make_mock_brief(
        brief_id="brief_crit_2",
        category=ArtistCategory.PHOTOGRAPHER,
        required_dims=["candid_event_coverage", "portraiture_and_headshots"],
        importance_map={"candid_event_coverage": ImportanceLevel.CRITICAL, "portraiture_and_headshots": ImportanceLevel.HIGH}
    )
    score_std_2 = calculate_match_score(artist, brief_std_2)
    score_crit_2 = calculate_match_score(artist, brief_crit_2)
    assert score_crit_2.requirement_fit_score > score_std_2.requirement_fit_score
    assert score_crit_2.requirement_fit_score == 30.0  # 25.0 * 1.2 = 30.0
    assert score_std_2.requirement_fit_score == 25.0   # 25.0 * 1.0 = 25.0


def test_claim_evidence_cannot_be_elevated_to_demonstrated():
    """TEST 5: Ensure self-reported CLAIM evidence is capped at 40% and receives claim bonus, not demonstrated bonus."""
    artist_claim = _make_mock_artist(
        artist_id="CLAIM_CAP_TEST",
        name="Claim Capped Artist",
        category=ArtistCategory.VIDEO_EDITOR,
        demonstrated_dims=[],
        claimed_dims=["vertical_short_form_editing"]
    )
    brief = _make_mock_brief(
        brief_id="brief_claim_test",
        category=ArtistCategory.VIDEO_EDITOR,
        required_dims=["vertical_short_form_editing"]
    )
    score = calculate_match_score(artist_claim, brief)
    # Requirement Fit: 50.0 * 1.0 * 0.4 = 20.0 pts (strictly capped at 40%)
    assert score.requirement_fit_score == 20.0
    # Evidence Strength: CLAIM bonus is 1.0 pt (not 6.0 pt STRONG demonstrated bonus)
    assert score.evidence_strength_score == 1.0


def test_all_top_two_recommendations_produced_from_generic_ranking():
    """TEST 6: Ensure all Top 2 recommendations are produced from the generic ranking mechanism."""
    artists = [
        _make_mock_artist("A1", "Candidate 1", ArtistCategory.MUSICIAN, ["acoustic_live_performance"]),
        _make_mock_artist("A2", "Candidate 2", ArtistCategory.MUSICIAN, ["acoustic_live_performance", "vocal_capability_and_repertoire"]),
        _make_mock_artist("A3", "Candidate 3", ArtistCategory.MUSICIAN, ["ambient_background_suitability"])
    ]
    brief = _make_mock_brief("brief_gen", ArtistCategory.MUSICIAN, ["acoustic_live_performance", "vocal_capability_and_repertoire"])
    
    rec = rank_artists_for_brief(brief, artists)
    assert len(rec.top_two) == 2
    # Candidate A2 has both demonstrated -> Rank 1
    assert rec.top_two[0].artist_id == "A2"
    assert rec.top_two[0].rank == 1
    # Candidate A1 has 1 demonstrated -> Rank 2
    assert rec.top_two[1].artist_id == "A1"
    assert rec.top_two[1].rank == 2

