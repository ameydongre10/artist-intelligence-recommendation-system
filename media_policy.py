"""
Media Processing Policy and Representative Evidence Selection Rules.
Governs how media files are inspected, selectively sampled, referenced, and handled for Phase 3.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.models.common import MediaType, ArtistCategory


class MediaSelectionRule(BaseModel):
    """Rule governing selective sampling of raw media assets."""
    max_samples_per_artist: int = Field(default=5, description="Maximum number of media assets deeply analyzed per artist")
    prioritize_formats: List[str] = Field(default_factory=list, description="Extensions prioritized for the category")
    selection_strategy: str = Field(description="Strategy for selecting representative media assets")


class MediaPolicy(BaseModel):
    """
    Standard media processing policy to prevent brute-force deep analysis across 941 MB of files.
    """
    photographer_policy: MediaSelectionRule = Field(
        default_factory=lambda: MediaSelectionRule(
            max_samples_per_artist=6,
            prioritize_formats=[".jpg", ".jpeg", ".png", ".webp"],
            selection_strategy="Sample distinct subject types (product vs event vs portrait vs architectural) based on filename or format."
        )
    )
    musician_policy: MediaSelectionRule = Field(
        default_factory=lambda: MediaSelectionRule(
            max_samples_per_artist=4,
            prioritize_formats=[".wav", ".mp3", ".mp4"],
            selection_strategy="Sample live gig takes (.wav/.mp4) over backing tracks; compare acoustic vs electronic instrumentation."
        )
    )
    video_editor_policy: MediaSelectionRule = Field(
        default_factory=lambda: MediaSelectionRule(
            max_samples_per_artist=5,
            prioritize_formats=[".mp4", ".mov"],
            selection_strategy="Prioritize food reels, live event cuts, and vertical short-form samples over generic landscape b-roll."
        )
    )


def select_representative_media_files(
    media_files: List[Dict[str, Any]],
    category: ArtistCategory,
    max_samples: int = 5
) -> List[Dict[str, Any]]:
    """
    Selects up to max_samples representative media files for an artist based on category heuristics,
    diversifying file types and prioritizing descriptive titles.
    """
    if len(media_files) <= max_samples:
        return media_files

    # Separate by type
    valid_files = [m for m in media_files if m.get("integrity_status") == "VALID"]
    
    # Priority sorting: files with descriptive names (containing 'food', 'reel', 'event', 'cafe', 'edit', 'demo') first
    def score_media(m: Dict[str, Any]) -> int:
        name = m.get("filename", "").lower()
        score = 0
        keywords = ["food", "reel", "event", "cafe", "demo", "take", "edit", "acoustic", "live", "product", "team"]
        for kw in keywords:
            if kw in name:
                score += 5
        # Prefer smaller/mid-size sample files over 90MB raw dumps when equal
        size = m.get("size_bytes", 0)
        if 0 < size < 30_000_000:
            score += 2
        return score

    sorted_files = sorted(valid_files, key=score_media, reverse=True)
    return sorted_files[:max_samples]


def format_evidence_reference(
    file_name: str,
    relative_path: str,
    media_type: MediaType,
    timestamp_or_frame: Optional[str] = None,
    observed_feature: Optional[str] = None
) -> Dict[str, Any]:
    """
    Standard formatter for evidence citations across images, video, and audio.
    """
    evidence_id = f"EV_{file_name.replace('.', '_').replace('-', '_')}"
    citation_parts = [f"Source: {file_name}"]
    if timestamp_or_frame:
        citation_parts.append(f"[{timestamp_or_frame}]")
    if observed_feature:
        citation_parts.append(f"— {observed_feature}")

    return {
        "evidence_id": evidence_id,
        "file_name": file_name,
        "relative_path": relative_path,
        "media_type": media_type.value,
        "timestamp_or_frame": timestamp_or_frame,
        "citation_text": " ".join(citation_parts)
    }
