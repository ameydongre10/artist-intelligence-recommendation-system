"""
Artist Domain Schemas.
Models artist identity, profile metadata, claims, demonstrated capabilities, unknowns, and anomalies.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.models.common import (
    EpistemicState,
    ArtistCategory,
    ConfidenceLevel,
    IdentifierStatus
)
from src.models.evidence import ClaimedCapability, DemonstratedCapability


class ArtistIdentity(BaseModel):
    """
    Structured representation of artist identity, preserving folder vs profile discrepancies.
    """
    source_folder_name: str = Field(description="Full source folder name (e.g., 'PO4_Drift', 'P01_Aanya_Rao')")
    source_folder_id: str = Field(description="Identifier derived from the folder prefix (e.g., 'PO4', 'P01')")
    profile_declared_id: Optional[str] = Field(default=None, description="Identifier declared inside the profile.docx header (e.g., 'V05', 'P01')")
    canonical_id: Optional[str] = Field(default=None, description="Resolved canonical identifier (remains None if unresolved)")
    folder_declared_name: str = Field(description="Artist name extracted from the folder name")
    profile_declared_name: Optional[str] = Field(default=None, description="Artist name extracted from docx text")
    identifier_status: IdentifierStatus = Field(default=IdentifierStatus.CONSISTENT, description="CONSISTENT if folder matches declared ID, else INCONSISTENT")
    discrepancy_notes: Optional[str] = Field(default=None, description="Explanation of any ID or name mismatch")


class UnknownCapability(BaseModel):
    """
    Represents an unverified capability dimension where evidence is missing or insufficient.
    Strict rule: UNKNOWN does NOT mean negative capability.
    """
    unknown_id: str = Field(description="Unique identifier for the unknown state")
    dimension: str = Field(description="Capability dimension that cannot be determined")
    reason: str = Field(description="Explanation of why evidence is insufficient (e.g., 'No vertical format clips supplied')")
    is_blocker: bool = Field(default=False, description="Whether this unknown prevents fulfilling critical hirer requirements")
    epistemic_state: EpistemicState = Field(default=EpistemicState.UNKNOWN, description="Must always be UNKNOWN")


class ProfileMetadata(BaseModel):
    """Structured fields parsed from docx profile."""
    raw_bio: Optional[str] = Field(default=None, description="Raw bio text from profile")
    location: Optional[str] = Field(default=None, description="Declared location (e.g., 'Delhi / NCR')")
    work_preference: Optional[str] = Field(default=None, description="Declared preference (e.g., 'Travel available', 'Remote')")
    declared_portfolio_claims: List[str] = Field(default_factory=list, description="List of portfolio titles/files declared in profile text")


class ArtistRecord(BaseModel):
    """
    Full intelligence record for an individual artist.
    """
    identity: ArtistIdentity = Field(description="Artist identity and identifier status")
    category: ArtistCategory = Field(description="Artist category: photographer, musician, or video_editor")
    profile_metadata: ProfileMetadata = Field(default_factory=ProfileMetadata, description="Parsed profile text metadata")
    claims: List[ClaimedCapability] = Field(default_factory=list, description="Self-reported claims from profile")
    demonstrated_capabilities: List[DemonstratedCapability] = Field(default_factory=list, description="Capabilities supported by observable media evidence")
    unknown_capabilities: List[UnknownCapability] = Field(default_factory=list, description="Dimensions where evidence is missing or inconclusive")
    overall_confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM, description="Overall confidence in artist capability profile")
    anomalies: List[str] = Field(default_factory=list, description="Specific dataset anomalies observed for this artist")
