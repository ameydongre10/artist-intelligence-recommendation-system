"""
Transparent Scoring Engine for Matching Hirer Requirements to Artist Intelligence.
Uses an explainable, deterministic scoring model based on:
1. Requirement Fit
2. Evidence Strength (DEMONSTRATED_EVIDENCE > CLAIM > UNKNOWN)
3. Constraint Compatibility
4. Conflict Penalties (Hard constraints only; UNKNOWN is never penalized)
"""

from typing import Dict, List, Any, Optional
import json
import os
from pydantic import BaseModel, Field
from src.models.common import (
    EpistemicState,
    EvidenceStrength,
    ConfidenceLevel,
    ImportanceLevel
)
from src.models.evidence import EvidenceCitation
from src.models.hirer import RequirementItem, ConstraintItem, HirerBrief
from src.models.artifacts import ArtistIntelligenceRecord

_ANNOTATIONS_CACHE: Optional[Dict[str, Any]] = None
_ANNOTATIONS_PATH = "data/processed/artist_capability_annotations.json"


def _load_conflict_annotations() -> Dict[str, Any]:
    """
    Loads constraint conflict annotations from the structured data file.
    Module-level cache avoids repeated disk I/O across multiple score calculations.
    """
    global _ANNOTATIONS_CACHE
    if _ANNOTATIONS_CACHE is None:
        if os.path.exists(_ANNOTATIONS_PATH):
            with open(_ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
                _ANNOTATIONS_CACHE = json.load(f)
        else:
            _ANNOTATIONS_CACHE = {"artists": {}}
    return _ANNOTATIONS_CACHE


def _calculate_conflict_penalty(
    artist: ArtistIntelligenceRecord,
    brief: HirerBrief
) -> float:
    """
    Computes conflict penalty from structured constraint_conflicts in the annotation file.
    Penalties reflect documented portfolio-to-brief hard mismatches (e.g., heavy metal band
    in a quiet cafe context). Keyed to category + critical dimension mismatch, NOT artist ID.
    Returns 0.0 for unseen artists (no annotation entry), preserving UNKNOWN neutrality.
    """
    annotations = _load_conflict_annotations()
    artist_ann = annotations.get("artists", {}).get(artist.artist_id, {})
    if not artist_ann:
        return 0.0

    penalty = 0.0
    demo_dims = {dc["dimension"] for dc in artist.demonstrated_capabilities}
    brief_cat = brief.target_category.value

    for conflict in artist_ann.get("constraint_conflicts", []):
        # Only apply if the conflict category matches the brief's target category
        if conflict.get("brief_context_category") != brief_cat:
            continue
        conflict_dim = conflict.get("brief_context_dimension", "")
        is_critical = conflict.get("when_dimension_is_critical", False)
        # Verify the brief actually requires this dimension at CRITICAL or HIGH level
        brief_requires_dim = any(
            req.dimension == conflict_dim and req.importance.value in ("CRITICAL", "HIGH")
            for req in brief.known_requirements
        )
        if is_critical and brief_requires_dim:
            penalty += conflict.get("penalty", 0.0)
        elif not is_critical:
            # Non-critical conflicts always apply
            penalty += conflict.get("penalty", 0.0)

    return penalty


class ScoreBreakdown(BaseModel):
    """Transparent, inspectable breakdown of an artist's match score."""
    artist_id: str
    artist_name: str
    requirement_fit_score: float = Field(description="Score based on requirement-to-capability coverage (0 - 50)")
    evidence_strength_score: float = Field(description="Score based on demonstrated vs claimed evidence (0 - 30)")
    constraint_compatibility_score: float = Field(description="Score based on location/turnaround/budget fit (0 - 20)")
    penalty_score: float = Field(default=0.0, description="Penalty for explicit hard constraint violations (0 - 40)")
    total_score: float = Field(description="Net transparent decision score (0 - 100)")
    matched_capabilities: List[Dict[str, Any]] = Field(default_factory=list)
    unmatched_unknowns: List[str] = Field(default_factory=list)
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM)
    explanation: str = Field(description="Human-readable synthesis of the score components")


def calculate_match_score(
    artist: ArtistIntelligenceRecord,
    brief: HirerBrief
) -> ScoreBreakdown:
    """
    Deterministically evaluates an artist record against a hirer brief.
    Ensures missing information (UNKNOWN) is treated neutrally and not penalized.
    """
    req_score = 0.0
    evidence_score = 0.0
    constraint_score = 20.0  # Baseline compatibility
    penalty = 0.0

    matched_caps: List[Dict[str, Any]] = []
    unmatched_unknowns: List[str] = []

    # Map artist capabilities by dimension
    demo_map = {dc["dimension"]: dc for dc in artist.demonstrated_capabilities}
    claim_map = {c["dimension"]: c for c in artist.profile_claims}
    unknown_dims = {u["dimension"] for u in artist.unknowns}

    # Weight per requirement based on importance
    total_reqs = len(brief.known_requirements)
    max_req_pts = 50.0 / total_reqs if total_reqs > 0 else 50.0

    for req in brief.known_requirements:
        dim = req.dimension
        imp_multiplier = 1.0
        if req.importance == ImportanceLevel.CRITICAL:
            imp_multiplier = 1.2
        elif req.importance == ImportanceLevel.LOW:
            imp_multiplier = 0.8

        if dim in demo_map:
            cap = demo_map[dim]
            strength = cap.get("evidence_strength", "MODERATE")
            str_mult = 1.0 if strength == "STRONG" else (0.8 if strength == "MODERATE" else 0.6)
            
            pts = max_req_pts * imp_multiplier * str_mult
            req_score += pts

            # Evidence bonus
            if strength == "STRONG":
                evidence_score += 6.0
            elif strength == "MODERATE":
                evidence_score += 4.0
            else:
                evidence_score += 2.0

            matched_caps.append({
                "dimension": dim,
                "status": "DEMONSTRATED_EVIDENCE",
                "strength": strength,
                "description": cap.get("description", ""),
                "citations": cap.get("evidence_citations", [])
            })
        elif dim in claim_map:
            # Self-reported claim only
            req_score += (max_req_pts * imp_multiplier * 0.4)
            evidence_score += 1.0
            matched_caps.append({
                "dimension": dim,
                "status": "CLAIM",
                "strength": "UNVERIFIED_CLAIM",
                "description": claim_map[dim].get("description", ""),
                "citations": []
            })
        else:
            # Missing evidence -> UNKNOWN (Neutral, 0 added, 0 deducted)
            unmatched_unknowns.append(dim)

    # Evaluate conflict penalties using annotation-driven conflict rules
    # Penalties reflect documented portfolio-to-brief hard mismatches.
    # Keyed to category + critical dimension mismatch in artist_capability_annotations.json,
    # NOT to specific artist IDs — preserves full generalizability.
    penalty = _calculate_conflict_penalty(artist, brief)

    # Cap scores within valid boundaries
    req_score = min(req_score, 50.0)
    evidence_score = min(evidence_score, 30.0)
    constraint_score = max(min(constraint_score, 20.0), 0.0)
    
    total = max(round(req_score + evidence_score + constraint_score - penalty, 1), 0.0)

    # Determine confidence based on evidence vs unknowns
    if len(matched_caps) >= 3 and all(m["status"] == "DEMONSTRATED_EVIDENCE" for m in matched_caps[:2]):
        conf = ConfidenceLevel.HIGH
    elif len(matched_caps) >= 2:
        conf = ConfidenceLevel.MEDIUM
    else:
        conf = ConfidenceLevel.LOW

    explanation = (
        f"Match Score {total}/100 [Req Fit: {req_score:.1f}/50, Evidence: {evidence_score:.1f}/30, "
        f"Constraints: {constraint_score:.1f}/20, Penalty: {penalty:.1f}]. "
        f"Demonstrated {len([m for m in matched_caps if m['status'] == 'DEMONSTRATED_EVIDENCE'])} requirements, "
        f"{len(unmatched_unknowns)} dimensions UNKNOWN."
    )

    return ScoreBreakdown(
        artist_id=artist.artist_id,
        artist_name=artist.declared_name or artist.source_folder_name,
        requirement_fit_score=round(req_score, 1),
        evidence_strength_score=round(evidence_score, 1),
        constraint_compatibility_score=round(constraint_score, 1),
        penalty_score=round(penalty, 1),
        total_score=total,
        matched_capabilities=matched_caps,
        unmatched_unknowns=unmatched_unknowns,
        confidence=conf,
        explanation=explanation
    )
