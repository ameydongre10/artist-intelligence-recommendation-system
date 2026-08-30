"""
Common Enums and Value Objects for the Domain Model.
Enforces strict epistemic state separation: CLAIM vs DEMONSTRATED_EVIDENCE vs ASSUMPTION vs UNKNOWN.
"""

from enum import Enum


class EpistemicState(str, Enum):
    """
    Epistemic classification for every piece of information in the system.
    Strict non-negotiable rule: CLAIM != DEMONSTRATED_EVIDENCE != ASSUMPTION != UNKNOWN.
    """
    CLAIM = "CLAIM"
    DEMONSTRATED_EVIDENCE = "DEMONSTRATED_EVIDENCE"
    ASSUMPTION = "ASSUMPTION"
    UNKNOWN = "UNKNOWN"


class ArtistCategory(str, Enum):
    """Artist categories present in the dataset."""
    PHOTOGRAPHER = "photographer"
    MUSICIAN = "musician"
    VIDEO_EDITOR = "video_editor"


class EvidenceStrength(str, Enum):
    """Qualitative strength of demonstrated evidence."""
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    LIMITED = "LIMITED"
    INSUFFICIENT = "INSUFFICIENT"


class ConfidenceLevel(str, Enum):
    """Confidence level assigned to assessments or inferences."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class ImportanceLevel(str, Enum):
    """Requirement priority for hirer matching."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class IdentifierStatus(str, Enum):
    """Integrity status for artist folder ID vs docx declared ID."""
    CONSISTENT = "CONSISTENT"
    INCONSISTENT = "INCONSISTENT"


class MediaType(str, Enum):
    """Type of media asset."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    TEXT = "text"
    SYSTEM = "system"
