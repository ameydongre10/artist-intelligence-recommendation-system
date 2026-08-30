"""
Profile Claim Extractor.
Extracts self-reported claims from artist profile.docx text.
Strict epistemic rule: A claim is purely self-reported (EpistemicState.CLAIM) and NOT demonstrated evidence.
"""

from typing import List, Dict, Any, Optional
import re
from src.models.common import EpistemicState, ArtistCategory
from src.models.evidence import ClaimedCapability
from src.models.artist import ProfileMetadata
from src.framework.capability_dimensions import get_dimensions_for_category


def extract_profile_claims(
    artist_id: str,
    category: ArtistCategory,
    profile_metadata: ProfileMetadata,
    raw_text: str
) -> List[ClaimedCapability]:
    """
    Extracts structured ClaimedCapability objects from parsed profile metadata and raw text.
    """
    claims: List[ClaimedCapability] = []
    claim_idx = 1

    # 1. Claims from Bio
    bio = profile_metadata.raw_bio or ""
    if bio:
        # Extract sentences or key phrases
        bio_clean = bio.strip()
        claims.append(
            ClaimedCapability(
                claim_id=f"CLM_{artist_id}_{claim_idx}",
                dimension="general_profile_bio",
                description=f"Self-reported profile summary: {bio_clean}",
                source_text=bio_clean[:200],
                is_demonstrated=False,
                epistemic_state=EpistemicState.CLAIM
            )
        )
        claim_idx += 1

    # 2. Category-specific capability claims mapped from bio and declared portfolio
    dim_defs = get_dimensions_for_category(category)
    bio_lower = bio.lower()

    # Match bio mentions to capability dimensions
    for dim_id, dim_def in dim_defs.items():
        matched_keywords = []
        # Look for keywords related to the dimension
        if dim_id == "product_commercial_photography":
            if any(w in bio_lower for w in ["product", "commercial", "food", "fashion"]):
                matched_keywords.append("product/commercial focus")
        elif dim_id == "candid_event_coverage":
            if any(w in bio_lower for w in ["event", "café", "workshop", "team day", "community"]):
                matched_keywords.append("event/community coverage")
        elif dim_id == "portraiture_and_headshots":
            if any(w in bio_lower for w in ["portrait", "headshot", "fashion"]):
                matched_keywords.append("portraiture focus")
        elif dim_id == "group_and_team_framing":
            if any(w in bio_lower for w in ["team day", "workshop", "event"]):
                matched_keywords.append("team/group context")
        elif dim_id == "acoustic_live_performance":
            if any(w in bio_lower for w in ["acoustic", "guitar", "live", "duo", "band"]):
                matched_keywords.append("acoustic live performance")
        elif dim_id == "vocal_capability_and_repertoire":
            if any(w in bio_lower for w in ["vocal", "singer", "act", "duo", "band"]):
                matched_keywords.append("vocal capability")
        elif dim_id == "ambient_background_suitability":
            if any(w in bio_lower for w in ["acoustic", "duo", "solo", "chill", "electronic"]):
                matched_keywords.append("ambient/live context")
        elif dim_id == "vertical_short_form_editing":
            if any(w in bio_lower for w in ["social", "short-form", "reel", "creator"]):
                matched_keywords.append("short-form/social video")
        elif dim_id == "food_and_hospitality_content":
            if any(w in bio_lower for w in ["food", "hospitality", "travel", "café"]):
                matched_keywords.append("food/hospitality focus")
        elif dim_id == "narrative_curation_from_raw_clips":
            if any(w in bio_lower for w in ["interview", "explainer", "company", "film", "recap"]):
                matched_keywords.append("narrative editing")

        if matched_keywords:
            claims.append(
                ClaimedCapability(
                    claim_id=f"CLM_{artist_id}_{claim_idx}",
                    dimension=dim_id,
                    description=f"Artist self-describes experience in {dim_def.display_name} ({', '.join(matched_keywords)})",
                    source_text=f"Bio mention: {bio_clean[:150]}",
                    is_demonstrated=False,
                    epistemic_state=EpistemicState.CLAIM
                )
            )
            claim_idx += 1

    # 3. Claims from declared portfolio items
    for port_claim in profile_metadata.declared_portfolio_claims:
        clean_claim = port_claim.strip()
        if clean_claim:
            claims.append(
                ClaimedCapability(
                    claim_id=f"CLM_{artist_id}_{claim_idx}",
                    dimension="declared_portfolio_project",
                    description=f"Self-declared portfolio project: '{clean_claim}'",
                    source_text=f"Portfolio item: {clean_claim}",
                    is_demonstrated=False,
                    epistemic_state=EpistemicState.CLAIM
                )
            )
            claim_idx += 1

    # 4. Claim from work preference / location
    if profile_metadata.work_preference:
        claims.append(
            ClaimedCapability(
                claim_id=f"CLM_{artist_id}_{claim_idx}",
                dimension="work_preference_claim",
                description=f"Declared work preference: {profile_metadata.work_preference}",
                source_text=f"Work preference: {profile_metadata.work_preference}",
                is_demonstrated=False,
                epistemic_state=EpistemicState.CLAIM
            )
        )
        claim_idx += 1

    return claims
