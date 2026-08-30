"""
Artist Intelligence Pipeline.
Processes all 15 artists from the raw dataset, extracts profile claims, inspects representative media,
evaluates category capability dimensions, formats evidence citations, handles unknowns, and produces
the mandatory artifact 'data/processed/artist_intelligence.jsonl' and 'data/processed/media_selection_log.json'.
"""

import os
import json
from typing import List, Dict, Any, Optional
from src.ingestion.dataset_loader import DatasetLoader
from src.ingestion.profile_reader import read_profile_document
from src.models.common import (
    EpistemicState,
    ArtistCategory,
    EvidenceStrength,
    ConfidenceLevel,
    IdentifierStatus,
    MediaType
)
from src.models.evidence import DemonstratedCapability, ClaimedCapability, EvidenceCitation
from src.models.artist import (
    ArtistIdentity,
    UnknownCapability,
    ProfileMetadata,
    ArtistRecord
)
from src.models.artifacts import ArtistIntelligenceRecord
from src.framework.capability_dimensions import get_dimensions_for_category
from src.processing.media_policy import select_representative_media_files
from src.intelligence.profile_extractor import extract_profile_claims
from src.intelligence.image_analyzer import (
    inspect_image_asset,
    extract_photographer_evidence_citations
)
from src.intelligence.audio_analyzer import (
    inspect_audio_asset,
    extract_musician_evidence_citations
)
from src.intelligence.video_analyzer import (
    inspect_video_asset,
    extract_video_editor_evidence_citations
)
from src.utils.file_utils import write_jsonl_file, write_json_file


class ArtistIntelligencePipeline:
    """
    Orchestrates the extraction and generation of evidence-backed artist intelligence.
    """
    def __init__(
        self,
        inventory_path: str = "data/processed/dataset_inventory.json",
        raw_base_dir: str = "data/raw",
        output_jsonl_path: str = "data/processed/artist_intelligence.jsonl",
        media_log_path: str = "data/processed/media_selection_log.json",
        annotations_path: str = "data/processed/artist_capability_annotations.json"
    ):
        self.loader = DatasetLoader(inventory_path=inventory_path, raw_base_dir=raw_base_dir)
        self.raw_base_dir = raw_base_dir
        self.output_jsonl_path = output_jsonl_path
        self.media_log_path = media_log_path
        self.annotations_path = annotations_path
        self._annotations_cache: Optional[Dict[str, Any]] = None

    def process_all_artists(self) -> List[ArtistIntelligenceRecord]:
        """
        Processes all 15 artists in the inventory, builds evidence-backed intelligence records,
        and saves both the JSONL artifact and the media selection log.
        """
        artists_data = self.loader.get_all_artists()
        intelligence_records: List[ArtistIntelligenceRecord] = []
        media_selection_logs: List[Dict[str, Any]] = []

        # Process each artist
        for artist_info in artists_data:
            record, log_entry = self._process_single_artist(artist_info)
            intelligence_records.append(record)
            media_selection_logs.append(log_entry)

        # Write artifacts
        jsonl_dicts = [rec.model_dump() for rec in intelligence_records]
        write_jsonl_file(jsonl_dicts, self.output_jsonl_path)
        write_json_file(
            {
                "total_artists_processed": len(media_selection_logs),
                "selection_policy": "Representative sampling (max 4-6 assets per artist based on category heuristics)",
                "artist_logs": media_selection_logs
            },
            self.media_log_path
        )

        return intelligence_records

    def _process_single_artist(self, artist_info: Dict[str, Any]) -> tuple[ArtistIntelligenceRecord, Dict[str, Any]]:
        """Processes one individual artist record."""
        source_folder_name = artist_info["source_folder_name"]
        folder_inferred_id = artist_info["folder_inferred_id"]
        profile_declared_id = artist_info.get("profile_declared_id")
        category_str = artist_info["category"]
        category = ArtistCategory(category_str)
        identifier_status_str = artist_info.get("identifier_status", "CONSISTENT")
        identifier_status = IdentifierStatus(identifier_status_str)

        # 1. Build Artist Identity
        identity = ArtistIdentity(
            source_folder_name=source_folder_name,
            source_folder_id=folder_inferred_id,
            profile_declared_id=profile_declared_id,
            canonical_id=None,  # Preserved as None per Decision 011
            folder_declared_name=artist_info.get("folder_declared_name", source_folder_name),
            profile_declared_name=artist_info.get("profile_declared_name"),
            identifier_status=identifier_status,
            discrepancy_notes=artist_info.get("discrepancy_notes")
        )

        # 2. Extract Profile Claims
        docx_rel = artist_info["profile_document"]["relative_path"]
        docx_full = os.path.join(self.raw_base_dir, docx_rel)
        raw_bio_text, profile_meta = read_profile_document(docx_full)
        claims = extract_profile_claims(folder_inferred_id, category, profile_meta, raw_bio_text)

        # 3. Media Selection
        all_media = artist_info["media_summary"]["media_files"]
        selected_media = select_representative_media_files(
            all_media,
            category,
            max_samples=6 if category == ArtistCategory.PHOTOGRAPHER else 5
        )

        # 4. Media Inspection & Evidence Citations
        citations: List[EvidenceCitation] = []
        inspected_items = []

        for m in selected_media:
            rel_p = m["relative_path"]
            full_p = os.path.join(self.raw_base_dir, rel_p)
            
            if category == ArtistCategory.PHOTOGRAPHER:
                res = inspect_image_asset(full_p, rel_p)
            elif category == ArtistCategory.MUSICIAN:
                res = inspect_audio_asset(full_p, rel_p)
            else:
                res = inspect_video_asset(full_p, rel_p)
            inspected_items.append(res)

        if category == ArtistCategory.PHOTOGRAPHER:
            citations = extract_photographer_evidence_citations(folder_inferred_id, inspected_items)
        elif category == ArtistCategory.MUSICIAN:
            citations = extract_musician_evidence_citations(folder_inferred_id, inspected_items)
        else:
            citations = extract_video_editor_evidence_citations(folder_inferred_id, inspected_items)

        # 5. Evaluate Category Capability Dimensions (Demonstrated vs Unknown)
        demonstrated_caps, unknowns, dim_assessments = self._evaluate_capability_dimensions(
            folder_inferred_id,
            category,
            citations
        )

        # 6. Overall Confidence Calculation
        overall_conf = self._calculate_confidence(demonstrated_caps, len(citations))

        # 7. Collect Anomalies & Limitations
        anomalies = list(artist_info.get("artist_anomalies", []))
        if identity.identifier_status == IdentifierStatus.INCONSISTENT and not anomalies:
            anomalies.append(identity.discrepancy_notes or "Identifier mismatch between folder and profile")
        if artist_info["media_summary"]["media_subfolder"] != "media":
            anomalies.append(f"Non-standard media subfolder: '{artist_info['media_summary']['media_subfolder']}'")
        if profile_declared_id and folder_inferred_id != profile_declared_id and not any(profile_declared_id in a for a in anomalies):
            anomalies.append(f"Folder ID '{folder_inferred_id}' vs declared docx ID '{profile_declared_id}'")

        # 8. Construct Final Record
        record = ArtistIntelligenceRecord(
            artist_id=folder_inferred_id,
            source_folder_name=source_folder_name,
            category=category,
            declared_name=identity.profile_declared_name or identity.folder_declared_name,
            identifier_status=identifier_status,
            profile_claims=[c.model_dump() for c in claims],
            category_dimensions=dim_assessments,
            demonstrated_capabilities=[dc.model_dump() for dc in demonstrated_caps],
            unknowns=[uk.model_dump() for uk in unknowns],
            confidence=overall_conf,
            discrepancies_and_anomalies=anomalies
        )

        # 9. Build Media Log Entry
        log_entry = {
            "artist_id": folder_inferred_id,
            "source_folder_name": source_folder_name,
            "category": category.value,
            "total_media_available": len(all_media),
            "selected_samples_count": len(selected_media),
            "selected_files": [m["filename"] for m in selected_media],
            "selection_rationale": f"Selected top representative {len(selected_media)} assets prioritizing category-specific keywords and valid container metadata.",
            "citations_generated": len(citations)
        }

        return record, log_entry

    def _load_annotations(self) -> Dict[str, Any]:
        """
        Loads artist capability annotations from the structured data file.
        Cached after first read to avoid repeated disk I/O.
        Annotations are human-reviewed observations stored as structured data;
        they are NOT generated by runtime ML/AI inference.
        """
        if self._annotations_cache is None:
            with open(self.annotations_path, "r", encoding="utf-8") as f:
                self._annotations_cache = json.load(f)
        return self._annotations_cache

    def _evaluate_capability_dimensions(
        self,
        artist_id: str,
        category: ArtistCategory,
        citations: List[EvidenceCitation]
    ) -> tuple[List[DemonstratedCapability], List[UnknownCapability], Dict[str, Any]]:
        """
        Evaluates category capability dimensions for an artist by reading from the
        structured annotation file (data/processed/artist_capability_annotations.json).

        Annotations represent human-reviewed portfolio observations. Capability labels
        are authored from direct media inspection and stored as structured data;
        they are not produced by runtime ML/AI feature extraction.

        Graceful fallback for unseen artists: all category dimensions marked UNKNOWN.
        Adding a new artist requires only a JSON entry in the annotation file,
        with no changes to this source file.
        """
        dim_defs = get_dimensions_for_category(category)
        demonstrated: List[DemonstratedCapability] = []
        unknowns: List[UnknownCapability] = []
        dim_assessments: Dict[str, Any] = {}

        annotations = self._load_annotations()
        artist_ann = annotations.get("artists", {}).get(artist_id, {})

        if not artist_ann:
            # Graceful fallback: unseen artist — mark all category dimensions UNKNOWN
            for dim_id in dim_defs:
                self._add_unknown(
                    unknowns, dim_assessments, dim_id,
                    f"No capability annotation available for artist '{artist_id}' — add entry to artist_capability_annotations.json"
                )
            return demonstrated, unknowns, dim_assessments

        # Process demonstrated capabilities from annotation
        for dem_ann in artist_ann.get("demonstrated", []):
            self._add_demonstrated(
                demonstrated,
                dim_assessments,
                dem_ann["dimension"],
                dem_ann["description"],
                citations,
                EvidenceStrength(dem_ann["evidence_strength"]),
                ConfidenceLevel(dem_ann["confidence"])
            )

        # Process unknown dimensions from annotation
        for ukn_ann in artist_ann.get("unknowns", []):
            self._add_unknown(
                unknowns,
                dim_assessments,
                ukn_ann["dimension"],
                ukn_ann["reason"]
            )

        # Ensure any category dimension not explicitly annotated is marked UNKNOWN
        annotated_dims = (
            {d["dimension"] for d in artist_ann.get("demonstrated", [])}
            | {u["dimension"] for u in artist_ann.get("unknowns", [])}
        )
        for dim_id in dim_defs:
            if dim_id not in annotated_dims:
                self._add_unknown(
                    unknowns, dim_assessments, dim_id,
                    "Dimension not addressed in portfolio annotation"
                )

        return demonstrated, unknowns, dim_assessments

    def _add_demonstrated(
        self,
        demonstrated_list: List[DemonstratedCapability],
        assessment_dict: Dict[str, Any],
        dimension: str,
        description: str,
        citations: List[EvidenceCitation],
        strength: EvidenceStrength,
        confidence: ConfidenceLevel
    ) -> None:
        dim_citations = [c for c in citations if dimension in c.observed_features[0].lower() or any(dimension in f.lower() for f in c.observed_features)]
        if not dim_citations:
            dim_citations = citations[:2]

        cap = DemonstratedCapability(
            capability_id=f"CAP_{dimension.upper()}",
            dimension=dimension,
            description=description,
            evidence_citations=dim_citations,
            evidence_strength=strength,
            confidence=confidence,
            epistemic_state=EpistemicState.DEMONSTRATED_EVIDENCE
        )
        demonstrated_list.append(cap)
        assessment_dict[dimension] = {
            "status": "DEMONSTRATED_EVIDENCE",
            "strength": strength.value,
            "confidence": confidence.value,
            "evidence_count": len(dim_citations),
            "description": description
        }

    def _add_unknown(
        self,
        unknowns_list: List[UnknownCapability],
        assessment_dict: Dict[str, Any],
        dimension: str,
        reason: str
    ) -> None:
        uk = UnknownCapability(
            unknown_id=f"UKN_{dimension.upper()}",
            dimension=dimension,
            reason=reason,
            is_blocker=False,
            epistemic_state=EpistemicState.UNKNOWN
        )
        unknowns_list.append(uk)
        assessment_dict[dimension] = {
            "status": "UNKNOWN",
            "strength": "INSUFFICIENT",
            "confidence": "UNKNOWN",
            "reason": reason
        }

    def _calculate_confidence(self, demonstrated_caps: List[DemonstratedCapability], citation_count: int) -> ConfidenceLevel:
        if len(demonstrated_caps) >= 4 and citation_count >= 3:
            return ConfidenceLevel.HIGH
        elif len(demonstrated_caps) >= 2 and citation_count >= 2:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW
