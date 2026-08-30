"""
Recommendation and Re-Ranking Domain Schemas.
Models requirement-to-capability matching, Top 2 recommendations, trade-offs,
max 2 refinement questions, and transparent before/after re-ranking.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from src.models.common import (
    ArtistCategory,
    ConfidenceLevel
)
from src.models.evidence import EvidenceCitation


class RequirementMatch(BaseModel):
    """Traceable connection between a hirer requirement and demonstrated artist evidence."""
    requirement_id: str = Field(description="Hirer requirement ID")
    dimension: str = Field(description="Capability dimension being matched")
    artist_capability_id: Optional[str] = Field(default=None, description="Matched artist capability ID if found")
    match_status: str = Field(description="Match rating: 'STRONG_MATCH', 'MODERATE_MATCH', 'PARTIAL_MATCH', 'UNKNOWN_FIT', 'MISMATCH'")
    fit_explanation: str = Field(description="Specific explanation connecting demonstrated evidence to the requirement")
    supporting_evidence: List[EvidenceCitation] = Field(default_factory=list, description="Citations supporting this match")


class TradeOffItem(BaseModel):
    """Explicit trade-off comparison between top candidates."""
    dimension: str = Field(description="Capability or operational dimension (e.g., 'repertoire_energy', 'budget_margin')")
    rank_1_status: str = Field(description="How Rank 1 performs on this dimension")
    rank_2_status: str = Field(description="How Rank 2 performs on this dimension")
    decision_implication: str = Field(description="Why the evaluator might pick Rank 2 over Rank 1 depending on priorities")


class RefinementQuestion(BaseModel):
    """
    High-impact follow-up question.
    Must explain why it matters and how answers alter the ranking.
    """
    question_id: str = Field(description="Unique ID (e.g., 'Q1', 'Q2')")
    question_text: str = Field(description="The question prompt for the hirer")
    why_it_matters: str = Field(description="The uncertainty or contradiction this question resolves")
    potential_ranking_impact: str = Field(description="Concrete explanation of how answers could change Rank 1 vs Rank 2")


class CandidateRecommendation(BaseModel):
    """An individual ranked artist recommendation."""
    rank: int = Field(description="Position in ranking (1, 2, etc.)")
    artist_id: str = Field(description="Artist identifier")
    artist_name: str = Field(description="Artist declared or folder name")
    category: ArtistCategory = Field(description="Artist category")
    fit_reason: str = Field(description="Concise synthesis of why this artist fits the brief")
    matched_requirements: List[RequirementMatch] = Field(default_factory=list, description="Requirement-by-requirement match breakdown")
    supporting_evidence: List[EvidenceCitation] = Field(default_factory=list, description="Key media evidence supporting this recommendation")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM, description="Confidence in this recommendation")
    trade_offs: List[str] = Field(default_factory=list, description="Explicit trade-offs or weaknesses compared to alternatives")
    uncertainty_and_limitations: List[str] = Field(default_factory=list, description="Gaps in evidence or unresolved brief items")


class BriefRecommendation(BaseModel):
    """
    Complete recommendation response for an initial hirer brief.
    Enforces maximum of 2 refinement questions.
    """
    brief_id: str = Field(description="Hirer brief ID")
    hirer_name: str = Field(description="Hirer name")
    summary_of_need: str = Field(description="Synthesized statement of core hiring requirement")
    top_two: List[CandidateRecommendation] = Field(description="Exactly two ranked candidate recommendations")
    trade_off_analysis: List[TradeOffItem] = Field(default_factory=list, description="Direct comparative trade-offs between Rank 1 and Rank 2")
    assumptions_made: List[str] = Field(default_factory=list, description="List of operational assumptions underpinning the recommendation")
    key_uncertainties: List[str] = Field(default_factory=list, description="Missing variables that could alter the decision")
    refinement_questions: List[RefinementQuestion] = Field(
        default_factory=list,
        description="At most two high-impact refinement questions"
    )

    @field_validator("refinement_questions")
    @classmethod
    def validate_max_two_questions(cls, v: List[RefinementQuestion]) -> List[RefinementQuestion]:
        if len(v) > 2:
            raise ValueError(f"Maximum 2 refinement questions allowed by assignment rules, got {len(v)}")
        return v

    @field_validator("top_two")
    @classmethod
    def validate_top_two_count(cls, v: List[CandidateRecommendation]) -> List[CandidateRecommendation]:
        if len(v) != 2:
            raise ValueError(f"Top 2 recommendation must contain exactly 2 ranked artists, got {len(v)}")
        return v


class RankMovement(BaseModel):
    """Tracks movement of an artist between initial and updated rankings."""
    artist_id: str = Field(description="Artist ID")
    artist_name: str = Field(description="Artist Name")
    previous_rank: Optional[int] = Field(default=None, description="Previous rank or None if unranked in Top 2")
    updated_rank: int = Field(description="New rank in revised ranking")
    movement: str = Field(description="'UP', 'DOWN', 'STABLE', or 'NEW_ENTRY'")
    reason: str = Field(description="Reason for movement triggered by new follow-up information")


class ReRankingResult(BaseModel):
    """
    Transparent before/after re-ranking result following a follow-up update.
    Preserves initial ranking snapshot and details all deltas.
    """
    brief_id: str = Field(description="Brief ID")
    follow_up_update_id: str = Field(description="Follow-up update identifier (e.g., '01_cafe_music_update')")
    follow_up_summary: str = Field(description="Summary of new requirements/constraints provided in update")
    initial_top_two: List[CandidateRecommendation] = Field(description="Preserved initial Top 2 ranking snapshot")
    updated_top_two: List[CandidateRecommendation] = Field(description="Revised Top 2 ranking after follow-up")
    rank_movements: List[RankMovement] = Field(default_factory=list, description="Detailed movement per candidate")
    what_changed: str = Field(description="Summary of what changed in requirements and priorities")
    why_ranking_changed: str = Field(description="Detailed explanation of why specific artists moved up, down, or stayed stable")
