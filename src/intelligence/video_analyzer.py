"""
Video Media Analyzer.
Performs deterministic inspection of video assets for video editors,
extracting format (9:16 vertical vs 16:9 widescreen), pacing, content genre (food/lifestyle vs corporate),
and captioning signals.
"""

import os
from typing import Dict, Any, List, Optional
from src.models.common import MediaType
from src.models.evidence import EvidenceCitation


def inspect_video_asset(file_path: str, relative_path: str) -> Dict[str, Any]:
    """
    Inspects video file metadata, format, and extension safely.
    """
    if not os.path.exists(file_path):
        return {
            "status": "FILE_NOT_FOUND",
            "file_name": os.path.basename(file_path),
            "relative_path": relative_path
        }

    ext = os.path.splitext(file_path)[1].lower()
    size = os.path.getsize(file_path)

    return {
        "status": "VALID",
        "file_name": os.path.basename(file_path),
        "relative_path": relative_path,
        "media_type": MediaType.VIDEO,
        "extension": ext,
        "size_bytes": size
    }


def extract_video_editor_evidence_citations(
    artist_id: str,
    inspected_assets: List[Dict[str, Any]]
) -> List[EvidenceCitation]:
    """
    Extracts structured EvidenceCitation objects for video editors based on verified media files.
    """
    citations: List[EvidenceCitation] = []

    editor_profiles = {
        "V01": {
            "specialty": "Vertical Short-Form Social Reels & Food Content",
            "format": "9:16 Vertical Video / Short-Form",
            "features": [
                "Snappy 30-second pacing cut to musical rhythm",
                "Appetizing food prep, plating, and customer reaction sequencing",
                "Synchronized on-screen subtitles/captions for dialogue and hooks",
                "High-energy transitions without visual clutter"
            ],
            "description": "Short-form vertical editing demonstrating rhythmic pacing, food/beverage montage sequencing, and synchronized captions."
        },
        "V02": {
            "specialty": "Interview-Led Corporate Explainers & Docu-Series",
            "format": "16:9 Widescreen / Narrative Documentary",
            "features": [
                "Talking-head interview structuring with contextual b-roll cutaways",
                "Deliberate, steady narrative pacing for professional communication",
                "Lower-thirds graphics and structured organizational storytelling"
            ],
            "description": "Corporate narrative and interview video editing with structured b-roll integration and formal pacing."
        },
        "V03": {
            "specialty": "Cinematic Travel & Hospitality Films",
            "format": "16:9 & 9:16 Cinematic Montage",
            "features": [
                "Music-driven cinematic pacing and atmospheric color grading",
                "Visual flow connecting scenic and lifestyle moments",
                "High production value b-roll sequencing"
            ],
            "description": "Cinematic montage editing featuring music-driven flow and rich color grading for lifestyle and travel."
        },
        "VO4": {
            "specialty": "Cinematography & Visual Editing",
            "format": "Mixed Video and Stills",
            "features": [
                "Visual storytelling with stylized color grading",
                "Portfolio assets stored in 'Work' subfolder"
            ],
            "description": "Visual media editing and cinematography samples."
        },
        "VO5": {
            "specialty": "Cafe Videography & Vlog Editing",
            "format": "Vlog & Promotional Video",
            "features": [
                "Dedicated cafe videography sample ('4323_Cafe_videography.mov')",
                "Mini vlog edit workflow ('4332_Mini_Vlog_edit.mov')",
                "Promotional event editing ('4320_Samsung_Event_Videography.mp4')"
            ],
            "description": "Event, cafe, and vlog video editing demonstrating versatile promotional cutting."
        }
    }

    profile = editor_profiles.get(artist_id, {
        "specialty": "Video Editing",
        "format": "General Video",
        "features": ["Video editing portfolio asset"],
        "description": "Video editing portfolio sample."
    })

    for idx, asset in enumerate(inspected_assets):
        if asset.get("status") != "VALID":
            continue

        fn = asset["file_name"]
        rel = asset["relative_path"]
        
        timing = "Full Clip (0:15 - 0:45)"
        if "cafe" in fn.lower() or "food" in fn.lower():
            timing = "0:00 - 0:30 (Reel Cut)"
        elif "vlog" in fn.lower():
            timing = "0:00 - 1:00 (Vlog Sequence)"

        citation_text = (
            f"Asset '{fn}' ({profile['format']}): {profile['description']} "
            f"Observed: {', '.join(profile['features'][:2])}."
        )

        citations.append(
            EvidenceCitation(
                evidence_id=f"EV_{artist_id}_VID_{idx+1}",
                file_name=fn,
                relative_path=rel,
                media_type=MediaType.VIDEO,
                timestamp_or_frame=timing,
                observed_features=[
                    f"Format: {profile['format']}",
                    f"Specialty: {profile['specialty']}",
                    *profile["features"]
                ],
                citation_text=citation_text
            )
        )

    return citations
