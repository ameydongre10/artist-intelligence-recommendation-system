"""
Category Capability Framework.
Defines category-specific capability dimensions for Photographers, Musicians, and Video Editors
based strictly on the assignment briefs and observable dataset evidence.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from src.models.common import ArtistCategory


class CapabilityDimensionDefinition(BaseModel):
    """Definition and evidence criteria for an observable capability dimension."""
    dimension_id: str = Field(description="Unique dimension code (e.g., 'candid_event_coverage')")
    display_name: str = Field(description="Human-readable title")
    category: ArtistCategory = Field(description="Target artist category")
    description: str = Field(description="What this capability dimension represents")
    observable_evidence_signals: List[str] = Field(description="Observable signals in submitted media that corroborate this capability")
    counter_evidence_or_limitations: List[str] = Field(description="Indicators of limitations, gaps, or insufficient evidence")


# Category-Specific Capability Dimensions
PHOTOGRAPHER_DIMENSIONS: Dict[str, CapabilityDimensionDefinition] = {
    "product_commercial_photography": CapabilityDimensionDefinition(
        dimension_id="product_commercial_photography",
        display_name="Product & Commercial Photography",
        category=ArtistCategory.PHOTOGRAPHER,
        description="Capability to shoot commercial products (bottles, jars, packaging) with clean, premium aesthetics and controlled reflections/lighting.",
        observable_evidence_signals=[
            "Isolated or contextual product framing (bottles, cosmetics, glassware)",
            "Controlled specular highlights and reflections on glass/plastic",
            "Clean depth of field isolating product textures and labels"
        ],
        counter_evidence_or_limitations=[
            "Only event/travel shots available without product samples",
            "Harsh clinical lighting or poor texture focus"
        ]
    ),
    "candid_event_coverage": CapabilityDimensionDefinition(
        dimension_id="candid_event_coverage",
        display_name="Candid & Dynamic Event Coverage",
        category=ArtistCategory.PHOTOGRAPHER,
        description="Capability to capture unposed, expressive moments during team offsites, literature events, workshops, and gatherings without stiff conference poses.",
        observable_evidence_signals=[
            "Natural unposed facial expressions and interactions among participants",
            "Indoor event lighting handling and movement capture",
            "Storytelling compositions across varied room angles and interactions"
        ],
        counter_evidence_or_limitations=[
            "Only static posed studio portraits",
            "Blurry motion capture or intrusive flash artifacts"
        ]
    ),
    "portraiture_and_headshots": CapabilityDimensionDefinition(
        dimension_id="portraiture_and_headshots",
        display_name="Portraiture & Leadership Headshots",
        category=ArtistCategory.PHOTOGRAPHER,
        description="Capability to frame professional individual or leadership portraits with flattering lighting and clean background separation.",
        observable_evidence_signals=[
            "Sharp eye focus and balanced facial lighting",
            "Flattering angles and confident executive expression",
            "Clean background separation and professional depth of field"
        ],
        counter_evidence_or_limitations=[
            "No individual portraits in media",
            "Distracting cluttered backgrounds"
        ]
    ),
    "group_and_team_framing": CapabilityDimensionDefinition(
        dimension_id="group_and_team_framing",
        display_name="Full-Team & Group Photo Coordination",
        category=ArtistCategory.PHOTOGRAPHER,
        description="Capability to coordinate and frame large groups (100+ people or team cohorts) with uniform sharpness and balanced exposure.",
        observable_evidence_signals=[
            "Wide-angle group compositions with edge-to-edge sharpness",
            "Even exposure across all subjects in multi-row groups",
            "Structured alignment avoiding blocked faces"
        ],
        counter_evidence_or_limitations=[
            "Only single-subject close-ups available",
            "Edge distortion on group perimeters"
        ]
    ),
    "turnaround_and_digital_delivery": CapabilityDimensionDefinition(
        dimension_id="turnaround_and_digital_delivery",
        display_name="Turnaround & Social/Digital Readiness",
        category=ArtistCategory.PHOTOGRAPHER,
        description="Capability to deliver rapid selects or social-ready crops (same-evening LinkedIn delivery or 2-day selects).",
        observable_evidence_signals=[
            "Demonstrated vertical and square aspect crop compositions",
            "Consistent color grading suited for digital web/social display"
        ],
        counter_evidence_or_limitations=[
            "Turnaround speed cannot be directly proven from static images alone (flagged as UNKNOWN / operational assumption)"
        ]
    )
}


MUSICIAN_DIMENSIONS: Dict[str, CapabilityDimensionDefinition] = {
    "acoustic_live_performance": CapabilityDimensionDefinition(
        dimension_id="acoustic_live_performance",
        display_name="Acoustic Live Performance",
        category=ArtistCategory.MUSICIAN,
        description="Demonstrated capability to perform live acoustic music (acoustic guitar, organic percussion, warm live arrangements).",
        observable_evidence_signals=[
            "Clean live acoustic guitar fingerpicking or strumming audio",
            "Video recordings of un-synthesized live cafe or rehearsal takes",
            "Natural room resonance and uncompressed organic timbre"
        ],
        counter_evidence_or_limitations=[
            "Purely synthesized electronic tracks without live acoustic instruments",
            "Over-produced studio backing tracks without live take evidence"
        ]
    ),
    "vocal_capability_and_repertoire": CapabilityDimensionDefinition(
        dimension_id="vocal_capability_and_repertoire",
        display_name="Vocal Capability & Repertoire Breadth",
        category=ArtistCategory.MUSICIAN,
        description="Vocal ability across English/Hindi acoustic ballads, pop covers, and duo harmonies.",
        observable_evidence_signals=[
            "Clear pitch control and vocal dynamic range in audio/video takes",
            "Multi-part vocal harmonies (duo format) or emotive solo delivery",
            "Demonstrated lyric versatility across Hindi/English songs"
        ],
        counter_evidence_or_limitations=[
            "Instrumental-only tracks without vocal evidence",
            "Excessive pitch correction masking live vocal stability"
        ]
    ),
    "ambient_background_suitability": CapabilityDimensionDefinition(
        dimension_id="ambient_background_suitability",
        display_name="Ambient Background & Cafe Atmosphere",
        category=ArtistCategory.MUSICIAN,
        description="Capability to maintain an unobtrusive, mellow musical backdrop allowing patrons to converse freely.",
        observable_evidence_signals=[
            "Mellow tempo and gentle dynamic control (downtempo/folk/chill acoustic)",
            "Cafe gig video recordings showing conversational patrons and gentle volume",
            "Absence of jarring heavy percussion or aggressive distortion"
        ],
        counter_evidence_or_limitations=[
            "Heavy rock/metal riffs or club EDM volume",
            "Acoustic acts lacking dynamic restraint"
        ]
    ),
    "headline_stage_dynamism": CapabilityDimensionDefinition(
        dimension_id="headline_stage_dynamism",
        display_name="Headline Set & Launch Stage Dynamism",
        category=ArtistCategory.MUSICIAN,
        description="Capability to deliver an engaging, high-energy 45-minute showcase performance that commands crowd attention during a launch event.",
        observable_evidence_signals=[
            "Upbeat medley live videos with energetic audience engagement",
            "Strong rhythmic propulsion and commanding vocal presence",
            "Fuller ensemble sound (duo/band) generating dynamic performance moments"
        ],
        counter_evidence_or_limitations=[
            "Only slow, somber solo ballads unsuitable for an upbeat launch moment",
            "Lack of stage presence or crowd-facing energy in video clips"
        ]
    ),
    "setup_portability_and_format": CapabilityDimensionDefinition(
        dimension_id="setup_portability_and_format",
        display_name="Setup Portability & Stage Footprint",
        category=ArtistCategory.MUSICIAN,
        description="Appropriateness of physical footprint for small cafe corners without a dedicated stage or complex PA system.",
        observable_evidence_signals=[
            "Solo or duo acoustic format with minimal instrument footprint",
            "Direct plug-and-play capability without full drum kits or large amp stacks"
        ],
        counter_evidence_or_limitations=[
            "Large multi-piece band requiring extensive stage space, multi-mic setups, and heavy PA gear"
        ]
    )
}


VIDEO_EDITOR_DIMENSIONS: Dict[str, CapabilityDimensionDefinition] = {
    "vertical_short_form_editing": CapabilityDimensionDefinition(
        dimension_id="vertical_short_form_editing",
        display_name="Vertical 9:16 Short-Form Editing",
        category=ArtistCategory.VIDEO_EDITOR,
        description="Demonstrated capability in formatting, framing, and pacing reels/shorts specifically for 9:16 mobile platforms.",
        observable_evidence_signals=[
            "Native 9:16 vertical video framing with centered subjects",
            "Snappy social hook within the first 3 seconds",
            "Optimized visual hierarchy for mobile UI overlays"
        ],
        counter_evidence_or_limitations=[
            "Only 16:9 widescreen corporate landscape videos without vertical crop experience"
        ]
    ),
    "narrative_curation_from_raw_clips": CapabilityDimensionDefinition(
        dimension_id="narrative_curation_from_raw_clips",
        display_name="Narrative Curation & Storytelling from Raw Footage",
        category=ArtistCategory.VIDEO_EDITOR,
        description="Capability to sort through dozens of raw phone clips (kitchen prep, dishes, crowd, reactions) and assemble a coherent, engaging story arc.",
        observable_evidence_signals=[
            "Well-sequenced montage balancing establishing shots, detail b-roll, and human reactions",
            "Logical progression (problem/prep -> execution -> reaction/satisfaction)",
            "Selective trimming removing shaky/redundant raw phone footage"
        ],
        counter_evidence_or_limitations=[
            "Generic chronological cut dumping every clip in order",
            "Disjointed cuts lacking narrative momentum"
        ]
    ),
    "pacing_and_energy_control": CapabilityDimensionDefinition(
        dimension_id="pacing_and_energy_control",
        display_name="Pacing & Rhythmic Energy Control",
        category=ArtistCategory.VIDEO_EDITOR,
        description="Clean, energetic pacing cut to musical rhythm without chaotic, disorienting transitions.",
        observable_evidence_signals=[
            "Cuts landing precisely on musical beats or percussion accents",
            "Dynamic speed ramps and smooth transitions maintaining energy",
            "Clean graphic/motion cuts that enhance rather than distract"
        ],
        counter_evidence_or_limitations=[
            "Sluggish unedited pauses or overly disruptive transition packs"
        ]
    ),
    "speech_captioning_and_subtitles": CapabilityDimensionDefinition(
        dimension_id="speech_captioning_and_subtitles",
        display_name="Speech Captioning & Subtitling",
        category=ArtistCategory.VIDEO_EDITOR,
        description="Integration of styled, kinetic, or clear on-screen subtitles for customer reactions and dialogue.",
        observable_evidence_signals=[
            "Accurate, synchronized on-screen animated or static captions",
            "Legible high-contrast typography styled for social reels"
        ],
        counter_evidence_or_limitations=[
            "No subtitles on videos with spoken dialogue",
            "Unreadable typography overlapping platform UI elements"
        ]
    ),
    "food_and_hospitality_content": CapabilityDimensionDefinition(
        dimension_id="food_and_hospitality_content",
        display_name="Food & Hospitality Content Editing",
        category=ArtistCategory.VIDEO_EDITOR,
        description="Specialized visual grading and montage pacing for culinary, cafe, and pop-up food experiences.",
        observable_evidence_signals=[
            "Appetizing color saturation and warm food lighting enhancement",
            "Macro cuts of plating, sizzling dishes, and texture details",
            "Vibrant cafe atmosphere and customer delight capture"
        ],
        counter_evidence_or_limitations=[
            "Only tech corporate explainers or tech software screencasts in media"
        ]
    )
}


def get_dimensions_for_category(category: ArtistCategory) -> Dict[str, CapabilityDimensionDefinition]:
    """Retrieve capability dimension definitions for a specific category."""
    if category == ArtistCategory.PHOTOGRAPHER:
        return PHOTOGRAPHER_DIMENSIONS
    elif category == ArtistCategory.MUSICIAN:
        return MUSICIAN_DIMENSIONS
    elif category == ArtistCategory.VIDEO_EDITOR:
        return VIDEO_EDITOR_DIMENSIONS
    return {}
