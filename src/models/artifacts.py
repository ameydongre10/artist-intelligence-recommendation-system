"""
Artifact Contracts for Mandatory Assignment Deliverables:
1. artist_intelligence.jsonl (One record per artist)
2. recommendations.json (Initial top two per brief, trade-offs, max 2 questions)
3. updated_recommendation.json (Revised ranking after supplied follow-up update)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.models.common import ArtistCategory, ConfidenceLevel, IdentifierStatus
from src.models.artist import ArtistRecord
from src.models.recommendation import BriefRecommendation, ReRankingResult


class ArtistIntelligenceRecord(BaseModel):
    """
    Contract for each line in 'artist_intelligence.jsonl'.
    Strictly aligns with the assignment requirement:
    'One record per artist: capability assessment, category-specific dimensions, evidence, unknowns and confidence'
    """
    artist_id: str = Field(description="Stable artist identifier (e.g., 'P01', 'M01', 'V01', 'PO4', 'VO4')")
    source_folder_name: str = Field(description="Original source folder name")
    category: ArtistCategory = Field(description="Category: photographer, musician, or video_editor")
    declared_name: Optional[str] = Field(default=None, description="Artist name as declared in profile docx")
    identifier_status: IdentifierStatus = Field(description="Identifier integrity status: CONSISTENT or INCONSISTENT")
    profile_claims: List[Dict[str, Any]] = Field(description="Self-reported claims from docx profile")
    category_dimensions: Dict[str, Any] = Field(description="Evaluated category-specific capability dimensions")
    demonstrated_capabilities: List[Dict[str, Any]] = Field(description="Observable demonstrated capabilities with evidence citations")
    unknowns: List[Dict[str, Any]] = Field(description="Unknown capability dimensions with reasons")
    confidence: ConfidenceLevel = Field(description="Overall confidence in artist capability profile")
    discrepancies_and_anomalies: List[str] = Field(default_factory=list, description="Any detected dataset or identifier anomalies")


class RecommendationsArtifact(BaseModel):
    """
    Contract for 'recommendations.json'.
    Strictly aligns with the assignment requirement:
    'Initial top two per brief, reasons, trade-offs, assumptions, uncertainty, then up to two refinement questions and expected impact'
    """
    metadata: Dict[str, Any] = Field(description="Artifact generation metadata")
    recommendations: List[BriefRecommendation] = Field(description="List of recommendations for all 4 hirer briefs")


class UpdatedRecommendationArtifact(BaseModel):
    """
    Contract for 'updated_recommendation.json'.
    Strictly aligns with the assignment requirement:
    'Revised ranking after the supplied follow-up, including what changed and why'
    """
    metadata: Dict[str, Any] = Field(description="Artifact generation metadata")
    reranking: ReRankingResult = Field(description="Re-ranking result for the follow-up update")
