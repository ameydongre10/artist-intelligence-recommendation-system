"""
Hirer Intent and Requirement Domain Schemas.
Models requirements, preferences, constraints, context, deliverables, assumptions,
unknowns, ambiguities, contradictions, decision-critical factors, and follow-up updates.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.models.common import (
    EpistemicState,
    ArtistCategory,
    ImportanceLevel
)


class RequirementItem(BaseModel):
    """An explicit capability requirement extracted from the hirer brief."""
    requirement_id: str = Field(description="Unique ID for this requirement")
    dimension: str = Field(description="Category capability dimension (e.g., 'acoustic_live_performance', 'clean_product_shots')")
    description: str = Field(description="Clear formulation of what the hirer explicitly asked for")
    importance: ImportanceLevel = Field(default=ImportanceLevel.HIGH, description="Importance level for ranking")
    source_quote: Optional[str] = Field(default=None, description="Exact phrase or excerpt from conversation")
    epistemic_state: EpistemicState = Field(default=EpistemicState.CLAIM, description="Must always be EpistemicState.CLAIM for hirer statements")


class PreferenceItem(BaseModel):
    """A soft preference or desired style that is not a strict dealbreaker."""
    preference_id: str = Field(description="Unique ID for the preference")
    description: str = Field(description="Description of the preference")
    is_flexible: bool = Field(default=True, description="Whether this preference can be traded off")
    source_quote: Optional[str] = Field(default=None, description="Source quote from conversation")


class ConstraintItem(BaseModel):
    """An operational, financial, or spatial constraint (e.g., budget ceiling, turnaround time, gear size)."""
    constraint_id: str = Field(description="Unique ID for the constraint")
    constraint_type: str = Field(description="Type of constraint: 'budget', 'location', 'turnaround', 'equipment', 'stage_size', 'format'")
    value: str = Field(description="Explicit value or bounds (e.g., '₹7,000 - ₹9,000 max', '2 days for selects')")
    is_hard_constraint: bool = Field(default=True, description="Whether violation disqualifies or severely penalizes candidate")
    source_quote: Optional[str] = Field(default=None, description="Source quote from conversation")


class ContextInfo(BaseModel):
    """Contextual parameters of the hiring situation."""
    situation: str = Field(description="Core situation (e.g., 'Cafe evening background music', 'Skincare launch')")
    target_date_or_timeline: str = Field(description="Scheduled date or deadline (e.g., 'Next Friday 7-10 PM', '4 September 10am-3pm')")
    location_or_venue: str = Field(description="Location or venue details")
    audience_or_scale: Optional[str] = Field(default=None, description="Audience size or event scale (e.g., '120 people', '80 guests')")


class DeliverableItem(BaseModel):
    """Concrete asset expected by the hirer."""
    deliverable_id: str = Field(description="Unique ID for this deliverable")
    description: str = Field(description="Deliverable specification (e.g., '12 final retouched images in square and vertical crops')")
    turnaround_expectation: str = Field(description="Expected turnaround time (e.g., '2 days for selects', 'Same evening for LinkedIn')")
    is_mandatory: bool = Field(default=True, description="Whether this deliverable is strictly required or optional")
    source_quote: Optional[str] = Field(default=None, description="Exact phrase from conversation")


class AssumptionItem(BaseModel):
    """
    An operational inference required to make progress from a sparse brief.
    Must never be silently merged into confirmed requirements.
    """
    assumption_id: str = Field(description="Unique ID for the assumption")
    description: str = Field(description="What is assumed")
    rationale: str = Field(description="Reasoning behind why this assumption is plausible")
    risk_impact: str = Field(description="What happens if this assumption is wrong")
    epistemic_state: EpistemicState = Field(default=EpistemicState.ASSUMPTION, description="Must always be EpistemicState.ASSUMPTION")


class UnknownItem(BaseModel):
    """
    An important missing variable from the hirer conversation.
    """
    unknown_id: str = Field(description="Unique ID for the unknown")
    description: str = Field(description="What variable is unknown (e.g., 'PA system availability', 'Leadership headshots confirmation')")
    why_it_matters: str = Field(description="Why resolving this unknown could alter artist selection")
    is_decision_critical: bool = Field(default=False, description="Whether this unknown directly blocks definitive selection")
    epistemic_state: EpistemicState = Field(default=EpistemicState.UNKNOWN, description="Must always be EpistemicState.UNKNOWN")


class AmbiguityItem(BaseModel):
    """An unclear statement with multiple interpretations that is not a direct contradiction."""
    ambiguity_id: str = Field(description="Unique ID for the ambiguity")
    statement: str = Field(description="Unclear statement from conversation")
    possible_interpretations: List[str] = Field(description="Possible meanings")
    decision_risk: str = Field(description="Risk of misinterpreting the hirer's intent")
    source_quote: str = Field(description="Exact quote from conversation")


class ContradictionItem(BaseModel):
    """A direct conflict or tension between two statements in the brief."""
    contradiction_id: str = Field(description="Unique ID for the contradiction")
    statement_a: str = Field(description="First statement (e.g., 'wants leadership headshots')")
    statement_b: str = Field(description="Second statement (e.g., 'no separate time/setup allocated during 10am-3pm schedule')")
    impact_on_decision: str = Field(description="How this contradiction affects artist scoping and trade-offs")


class DecisionCriticalFactor(BaseModel):
    """A core factor that dictates artist selection and ranking."""
    factor_id: str = Field(description="Unique ID")
    dimension: str = Field(description="Relevant capability dimension")
    factor_summary: str = Field(description="Summary of why this factor governs recommendation choices")
    importance: ImportanceLevel = Field(default=ImportanceLevel.HIGH, description="Importance level")


class HirerBrief(BaseModel):
    """
    Complete structured representation of an analyzed hirer brief.
    """
    brief_id: str = Field(description="Identifier corresponding to the conversation file (e.g., '01_cafe_music_whatsapp')")
    hirer_name: str = Field(description="Name or handle of hirer (e.g., 'Rhea', 'Nidhi', 'Manu K.', 'Shalini')")
    channel: str = Field(description="Channel type: 'whatsapp', 'chat', 'email', 'phone_notes'")
    source_file: str = Field(description="Relative path of the source conversation file")
    target_category: ArtistCategory = Field(description="Target artist category required by this brief")
    raw_text: str = Field(description="Full text of the original conversation")
    context: ContextInfo = Field(description="Contextual background of the brief")
    known_requirements: List[RequirementItem] = Field(default_factory=list, description="Explicit known capability demands")
    preferences: List[PreferenceItem] = Field(default_factory=list, description="Soft preferences")
    hard_constraints: List[ConstraintItem] = Field(default_factory=list, description="Explicit operational constraints (budget, dates, format)")
    deliverables: List[DeliverableItem] = Field(default_factory=list, description="Concrete expected outputs")
    assumptions: List[AssumptionItem] = Field(default_factory=list, description="Explicitly tracked operational assumptions")
    unknowns: List[UnknownItem] = Field(default_factory=list, description="Explicitly tracked missing variables")
    ambiguities: List[AmbiguityItem] = Field(default_factory=list, description="Detected ambiguous statements")
    contradictions: List[ContradictionItem] = Field(default_factory=list, description="Detected tensions or conflicting asks")
    decision_critical_factors: List[DecisionCriticalFactor] = Field(default_factory=list, description="Core factors governing candidate evaluation")


class FollowUpUpdateRecord(BaseModel):
    """
    Structured record of the follow-up conversation update.
    """
    update_id: str = Field(description="Identifier for the update file (e.g., '01_cafe_music_update')")
    related_brief_id: str = Field(description="Corresponding initial brief ID ('01_cafe_music_whatsapp')")
    source_file: str = Field(description="Source file path")
    update_summary: str = Field(description="Summary of the scope and parameter changes")
    raw_text: str = Field(description="Raw text of the follow-up message")
    changes_detected: List[Dict[str, Any]] = Field(description="List of detected changes with before/after comparisons")
    new_hard_constraints: List[ConstraintItem] = Field(default_factory=list, description="New constraints introduced (e.g., 45-min headline set, ₹15k budget)")
    modified_preferences: List[PreferenceItem] = Field(default_factory=list, description="Updated preferences (performance/moment feeling)")
    remaining_unknowns: List[UnknownItem] = Field(default_factory=list, description="Remaining unresolved variables (e.g., speaker/PA status)")


class HirerIntelligenceArtifact(BaseModel):
    """
    Schema for 'data/processed/hirer_intelligence.json'.
    """
    metadata: Dict[str, Any] = Field(description="Metadata about generation")
    briefs: List[HirerBrief] = Field(description="Structured intelligence for all 4 hirer briefs")
    follow_up_updates: List[FollowUpUpdateRecord] = Field(description="Structured records of follow-up updates")
