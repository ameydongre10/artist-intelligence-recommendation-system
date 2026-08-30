"""
Evidence and Capability Schemas.
Enforces that demonstrated capabilities cite specific media sources, timestamps, or image identifiers.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.models.common import EpistemicState, EvidenceStrength, ConfidenceLevel, MediaType


class EvidenceCitation(BaseModel):
    """
    Exact reference to a piece of evidence extracted from raw media or profile.
    Must cite the source file, image ID, timestamp/frame interval, or track segment.
    """
    evidence_id: str = Field(description="Unique identifier for this piece of evidence")
    file_name: str = Field(description="Name of the source file")
    relative_path: str = Field(description="Relative path within the dataset")
    media_type: MediaType = Field(description="Type of media source")
    timestamp_or_frame: Optional[str] = Field(default=None, description="Timestamp interval or frame number where capability is observed")
    observed_features: List[str] = Field(default_factory=list, description="Specific observable signals extracted from the media")
    citation_text: str = Field(description="Human-readable citation summarizing the observed evidence")


class DemonstratedCapability(BaseModel):
    """
    A capability supported by directly observable media evidence.
    """
    capability_id: str = Field(description="Unique identifier for the capability")
    dimension: str = Field(description="Category-specific capability dimension (e.g., 'candid_event_coverage', 'acoustic_live_performance')")
    description: str = Field(description="Description of what the artist demonstrated")
    evidence_citations: List[EvidenceCitation] = Field(default_factory=list, description="Direct supporting evidence references")
    evidence_strength: EvidenceStrength = Field(default=EvidenceStrength.MODERATE, description="Strength of supporting evidence")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM, description="Confidence in this capability assessment")
    epistemic_state: EpistemicState = Field(default=EpistemicState.DEMONSTRATED_EVIDENCE, description="Must always be DEMONSTRATED_EVIDENCE")
    notes: Optional[str] = Field(default=None, description="Any specific observations or limitations")


class ClaimedCapability(BaseModel):
    """
    A capability claimed by the artist in profile text but not yet verified as demonstrated.
    """
    claim_id: str = Field(description="Unique identifier for the claim")
    dimension: str = Field(description="Category-specific capability dimension")
    description: str = Field(description="Description of the self-reported claim")
    source_text: str = Field(description="Exact excerpt or summary from profile.docx where claim appears")
    is_demonstrated: bool = Field(default=False, description="Whether this claim is corroborated by media evidence")
    epistemic_state: EpistemicState = Field(default=EpistemicState.CLAIM, description="Must always be CLAIM")
