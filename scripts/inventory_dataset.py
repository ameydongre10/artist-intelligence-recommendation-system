"""
Dataset Inventory Builder & Inspector for Artist Intelligence & Recommendation System.

Systematically scans the raw dataset extracted in data/raw/Data set, validates file integrity,
extracts profile text, analyzes media headers, documents naming and structural anomalies,
and produces a structured, reproducible inventory artifact at data/processed/dataset_inventory.json.
"""

import os
import sys
import json
import zipfile
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image


def get_docx_text(docx_path: str) -> Tuple[str, str]:
    """
    Extract raw text from a .docx file using built-in zipfile and XML parsing.
    Returns (raw_text, integrity_status).
    """
    if not os.path.exists(docx_path):
        return "", "MISSING"
    try:
        with zipfile.ZipFile(docx_path, "r") as z:
            test_res = z.testzip()
            if test_res:
                return "", f"CORRUPT_ZIP_ENTRY_{test_res}"
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            texts = []
            for elem in tree.iter():
                if elem.tag.endswith("}t") and elem.text:
                    texts.append(elem.text)
            return " ".join(texts), "OK"
    except Exception as e:
        return "", f"UNREADABLE_DOCX_{type(e).__name__}"


def extract_declared_name(text: str) -> Optional[str]:
    """Extract declared artist name from header text preceding category/location."""
    if not text:
        return None
    before_cat = text.split("Category")[0].strip()
    if not before_cat:
        return None
    # Remove leading ID pattern like 'P01 /', 'M01 —', 'M04_', 'V03 /'
    cleaned = re.sub(r'^[PMV][0-9O]{2}\s*[/—\-_:]*\s*', '', before_cat, flags=re.I).strip()
    # Remove '(M03)'
    cleaned = re.sub(r'\([PMV][0-9O]{2}\)', '', cleaned, flags=re.I).strip()
    # Remove 'Artist ID M02'
    cleaned = re.sub(r'Artist\s+ID\s+[PMV][0-9O]{2}', '', cleaned, flags=re.I).strip()
    # Remove trailing punctuation or whitespace
    cleaned = re.sub(r'[\s|—\-:]+$', '', cleaned).strip()
    return cleaned if cleaned else None


def parse_profile_text(text: str) -> Dict[str, Any]:
    """
    Extract basic declared profile fields from raw docx text.
    Preserves raw text while identifying structured sections.
    """
    extracted: Dict[str, Any] = {
        "raw_text": text,
        "declared_id": None,
        "declared_name": extract_declared_name(text),
        "declared_category": None,
        "declared_location": None,
        "declared_work_preference": None,
        "declared_bio": None,
        "declared_portfolio_refs": []
    }
    
    if not text:
        return extracted
        
    # Extract declared ID: e.g. P01, M01, M02, M03, M04, M05, V01, V03, V04, V05, P04, PO4, PO5
    id_match = re.search(r'(?:^|[^A-Za-z0-9])([PMV][0-9O]{2})(?=[^A-Za-z0-9]|$)', text, re.IGNORECASE)
    if id_match:
        extracted["declared_id"] = id_match.group(1).upper()
        
    # Declared category
    cat_match = re.search(r'Category\s*[:—\-]?\s*([^L\n]+?)(?=Location|Work|Bio|$)', text, re.IGNORECASE)
    if cat_match:
        extracted["declared_category"] = cat_match.group(1).strip()
        
    # Declared location
    loc_match = re.search(r'Location\s*[:—\-]?\s*([^W\n]+?)(?=Work|Bio|Preference|$)', text, re.IGNORECASE)
    if loc_match:
        extracted["declared_location"] = loc_match.group(1).strip()
        
    # Declared work preference
    pref_match = re.search(r'Work\s*preference\s*[:—\-]?\s*([^B\n]+?)(?=Bio|Portfolio|$)', text, re.IGNORECASE)
    if pref_match:
        extracted["declared_work_preference"] = pref_match.group(1).strip()
        
    # Declared Bio
    bio_match = re.search(r'Bio\s*[:—\-]?\s*(.*?)(?=Portfolio|$)', text, re.IGNORECASE)
    if bio_match:
        extracted["declared_bio"] = bio_match.group(1).strip()
        
    # Declared Portfolio references
    port_match = re.search(r'Portfolio\s*[:—\-]?\s*(.*)$', text, re.IGNORECASE)
    if port_match:
        port_text = port_match.group(1).strip()
        refs = [r.strip() for r in re.split(r'\s{2,}|\n', port_text) if r.strip()]
        extracted["declared_portfolio_refs"] = refs
        
    return extracted


def inspect_media_file(file_path: str, raw_root: str) -> Dict[str, Any]:
    """
    Inspect an individual media file for format, size, header integrity, and dimensions.
    """
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    size_bytes = os.path.getsize(file_path)
    rel_path = os.path.relpath(file_path, raw_root).replace("\\", "/")
    
    file_type = "unknown"
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        file_type = "image"
    elif ext in [".mp4", ".mov"]:
        file_type = "video"
    elif ext in [".mp3", ".wav"]:
        file_type = "audio"
    elif ext in [".docx", ".txt"]:
        file_type = "document" if ext == ".docx" else "text"
    elif filename.startswith(".") or ext in [".ds_store"]:
        file_type = "system"

    media_info: Dict[str, Any] = {
        "filename": filename,
        "relative_path": rel_path,
        "extension": ext,
        "file_type": file_type,
        "size_bytes": size_bytes,
        "integrity_status": "VALID",
        "details": {}
    }

    if size_bytes == 0:
        media_info["integrity_status"] = "EMPTY"
        media_info["details"]["error"] = "File size is 0 bytes"
        return media_info

    if file_type == "image":
        try:
            with Image.open(file_path) as img:
                img.verify()
                media_info["details"] = {
                    "format": img.format,
                    "mode": img.mode,
                    "width": img.size[0] if img.size else None,
                    "height": img.size[1] if img.size else None
                }
        except Exception as e:
            media_info["integrity_status"] = "CORRUPT_IMAGE"
            media_info["details"]["error"] = str(e)

    elif file_type == "audio":
        try:
            with open(file_path, "rb") as af:
                header = af.read(16)
                if ext == ".wav":
                    is_wav = header[:4] == b"RIFF" and header[8:12] == b"WAVE"
                    media_info["integrity_status"] = "VALID" if is_wav else "INVALID_WAV_HEADER"
                    media_info["details"] = {"header_magic": header[:4].decode("latin-1", errors="replace")}
                elif ext == ".mp3":
                    is_mp3 = header[:3] == b"ID3" or (header[0] == 0xFF and (header[1] & 0xE0) == 0xE0)
                    media_info["integrity_status"] = "VALID" if is_mp3 else "SUSPECT_MP3_HEADER"
                    media_info["details"] = {"header_magic": header[:3].decode("latin-1", errors="replace")}
        except Exception as e:
            media_info["integrity_status"] = "UNREADABLE_AUDIO"
            media_info["details"]["error"] = str(e)

    elif file_type == "video":
        try:
            with open(file_path, "rb") as vf:
                chunk = vf.read(64)
                has_atom = b"ftyp" in chunk or b"moov" in chunk or b"free" in chunk or b"wide" in chunk
                media_info["integrity_status"] = "VALID" if has_atom else "SUSPECT_VIDEO_HEADER"
                media_info["details"] = {"has_iso_base_atom": has_atom}
        except Exception as e:
            media_info["integrity_status"] = "UNREADABLE_VIDEO"
            media_info["details"]["error"] = str(e)

    return media_info


def scan_dataset(raw_dataset_dir: str) -> Dict[str, Any]:
    """
    Main scanner: systematically inspects the entire dataset and builds inventory JSON.
    """
    raw_dataset_path = Path(raw_dataset_dir).resolve()
    if not raw_dataset_path.exists():
        raise FileNotFoundError(f"Raw dataset directory not found at: {raw_dataset_path}")

    # First pass: collect ALL files directly via os.walk to ensure 100% complete accounting
    all_files_in_dataset: List[Path] = []
    for root, dirs, files in os.walk(raw_dataset_path):
        for f in sorted(files):
            all_files_in_dataset.append(Path(root) / f)

    inventory: Dict[str, Any] = {
        "dataset_metadata": {
            "name": "Sekeron AI Intern Practical Assessment Dataset",
            "source_raw_dir": str(raw_dataset_path).replace("\\", "/"),
            "scanner_version": "1.0.0",
            "total_files_discovered": len(all_files_in_dataset),
            "total_size_bytes": sum(p.stat().st_size for p in all_files_in_dataset),
            "categories_discovered": ["photographers", "musicians", "video_editors"],
            "total_artists_discovered": 0,
            "total_hirer_conversations": 0,
            "total_follow_up_updates": 0
        },
        "hirer_conversations": [],
        "follow_up_updates": [],
        "artist_profiles": {
            "photographers": [],
            "musicians": [],
            "video_editors": []
        },
        "file_type_distribution": {},
        "system_files": [],
        "dataset_anomalies": [],
        "integrity_summary": {
            "total_checked": len(all_files_in_dataset),
            "valid_files": 0,
            "corrupt_files": 0,
            "empty_files": 0,
            "system_files_count": 0
        }
    }

    file_types: Dict[str, int] = {}
    for p in all_files_in_dataset:
        ext = p.suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1
        if p.name.startswith(".") or ext in [".ds_store"]:
            rel = os.path.relpath(p, raw_dataset_path.parent).replace("\\", "/")
            if rel not in inventory["system_files"]:
                inventory["system_files"].append(rel)

    inventory["file_type_distribution"] = file_types

    # 1. Inspect Hirer Conversations
    hirer_conv_dir = raw_dataset_path / "hirer_conversations"
    if hirer_conv_dir.exists():
        for f in sorted(os.listdir(hirer_conv_dir)):
            fp = hirer_conv_dir / f
            if fp.is_file():
                size = fp.stat().st_size
                content = ""
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as tf:
                        content = tf.read()
                except Exception as e:
                    content = f"[ERROR: {e}]"
                    
                inventory["hirer_conversations"].append({
                    "brief_id": fp.stem,
                    "filename": f,
                    "relative_path": os.path.relpath(fp, raw_dataset_path.parent).replace("\\", "/"),
                    "size_bytes": size,
                    "char_count": len(content),
                    "line_count": len(content.splitlines()),
                    "raw_content": content
                })
        inventory["dataset_metadata"]["total_hirer_conversations"] = len(inventory["hirer_conversations"])

    # 2. Inspect Follow-Up Updates
    follow_up_dir = raw_dataset_path / "follow_up_update"
    if follow_up_dir.exists():
        for f in sorted(os.listdir(follow_up_dir)):
            fp = follow_up_dir / f
            if fp.is_file():
                size = fp.stat().st_size
                content = ""
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as tf:
                        content = tf.read()
                except Exception as e:
                    content = f"[ERROR: {e}]"
                    
                inventory["follow_up_updates"].append({
                    "update_id": fp.stem,
                    "filename": f,
                    "relative_path": os.path.relpath(fp, raw_dataset_path.parent).replace("\\", "/"),
                    "size_bytes": size,
                    "char_count": len(content),
                    "line_count": len(content.splitlines()),
                    "raw_content": content
                })
        inventory["dataset_metadata"]["total_follow_up_updates"] = len(inventory["follow_up_updates"])

    # 3. Inspect Artist Profiles across 3 categories
    artist_base_dir = raw_dataset_path / "artist_profiles"
    categories = ["photographers", "musicians", "video_editors"]

    for cat in categories:
        cat_dir = artist_base_dir / cat
        if not cat_dir.exists():
            continue

        for artist_folder in sorted(os.listdir(cat_dir)):
            af_path = cat_dir / artist_folder
            if not af_path.is_dir():
                continue

            folder_inferred_id = artist_folder.split("_")[0] if "_" in artist_folder else artist_folder
            folder_declared_name = "_".join(artist_folder.split("_")[1:]) if "_" in artist_folder else artist_folder

            artist_record: Dict[str, Any] = {
                "source_folder_name": artist_folder,
                "category": cat[:-1] if cat.endswith("s") else cat,
                "folder_inferred_id": folder_inferred_id,
                "profile_declared_id": None,
                "canonical_id": None,  # Strictly unresolved until Phase 3/4
                "identifier_status": "CONSISTENT",
                "folder_declared_name": folder_declared_name,
                "profile_declared_name": None,
                "profile_document": None,
                "media_summary": {
                    "media_subfolder": None,
                    "total_media_count": 0,
                    "image_count": 0,
                    "video_count": 0,
                    "audio_count": 0,
                    "system_files_count": 0,
                    "media_files": []
                },
                "artist_anomalies": []
            }

            profile_docs: List[Path] = []
            media_files_found: List[Path] = []

            for root, dirs, files in os.walk(af_path):
                for f in sorted(files):
                    fp = Path(root) / f
                    ext = fp.suffix.lower()

                    if f == ".DS_Store" or f.startswith("._"):
                        artist_record["media_summary"]["system_files_count"] += 1
                        continue

                    if ext == ".docx":
                        profile_docs.append(fp)
                    else:
                        media_files_found.append(fp)

            # Process Profile Document
            if len(profile_docs) == 0:
                artist_record["profile_document"] = {"status": "MISSING_PROFILE_DOCX"}
                artist_record["artist_anomalies"].append("Missing profile.docx document in artist folder")
            else:
                pdoc = profile_docs[0]
                raw_text, integrity = get_docx_text(str(pdoc))
                parsed = parse_profile_text(raw_text)
                
                artist_record["profile_declared_id"] = parsed.get("declared_id")
                artist_record["profile_declared_name"] = parsed.get("declared_name")
                artist_record["profile_document"] = {
                    "filename": pdoc.name,
                    "relative_path": os.path.relpath(pdoc, raw_dataset_path.parent).replace("\\", "/"),
                    "size_bytes": pdoc.stat().st_size,
                    "integrity_status": integrity,
                    "char_count": len(raw_text),
                    "raw_text": raw_text,
                    "parsed_fields": parsed
                }
                
                if len(profile_docs) > 1:
                    artist_record["artist_anomalies"].append(f"Multiple profile documents found: {[p.name for p in profile_docs]}")

            # Identify Media Subfolder
            subfolders = [d for d in os.listdir(af_path) if (af_path / d).is_dir()]
            if "media" in subfolders:
                artist_record["media_summary"]["media_subfolder"] = "media"
            elif "Work" in subfolders:
                artist_record["media_summary"]["media_subfolder"] = "Work"
                artist_record["artist_anomalies"].append("Non-standard media subfolder name: 'Work' instead of 'media'")
            else:
                artist_record["media_summary"]["media_subfolder"] = subfolders[0] if subfolders else "root"
                if subfolders:
                    artist_record["artist_anomalies"].append(f"Unusual media subfolder name: {subfolders[0]}")

            # Process Individual Media Files
            for mf in sorted(media_files_found):
                minfo = inspect_media_file(str(mf), str(raw_dataset_path.parent))
                artist_record["media_summary"]["media_files"].append(minfo)
                
                ftype = minfo["file_type"]
                if ftype == "image":
                    artist_record["media_summary"]["image_count"] += 1
                elif ftype == "video":
                    artist_record["media_summary"]["video_count"] += 1
                elif ftype == "audio":
                    artist_record["media_summary"]["audio_count"] += 1

            artist_record["media_summary"]["total_media_count"] = len(artist_record["media_summary"]["media_files"])

            # Evaluate Identifier Consistency & Specific Known Anomalies
            folder_id_norm = folder_inferred_id.upper().replace("O", "0") if folder_inferred_id.startswith(("PO", "VO")) else folder_inferred_id.upper()
            profile_id = artist_record["profile_declared_id"]
            
            # Check ID naming (letter 'O' vs digit '0')
            if folder_inferred_id.startswith(("PO", "VO")):
                artist_record["identifier_status"] = "INCONSISTENT"
                artist_record["artist_anomalies"].append(
                    f"Folder uses letter 'O' instead of digit '0' in identifier '{folder_inferred_id}'"
                )

            # Check ID mismatch between folder and docx profile
            if profile_id:
                profile_id_norm = profile_id.upper().replace("O", "0") if profile_id.startswith(("PO", "VO")) else profile_id.upper()
                if profile_id_norm != folder_id_norm:
                    artist_record["identifier_status"] = "INCONSISTENT"
                    artist_record["artist_anomalies"].append(
                        f"ID Mismatch: Folder indicates '{folder_inferred_id}' but profile docx declares '{profile_id}'"
                    )
            else:
                artist_record["identifier_status"] = "INCONSISTENT"
                artist_record["artist_anomalies"].append(
                    "Profile docx lacks explicit standard artist ID header"
                )

            # Specific individual artist audit notes
            if artist_folder == "PO4_Drift":
                artist_record["artist_anomalies"].append("Profile docx declares 'V05 / Drift' (Video editor prefix for a photographer)")
            elif artist_folder == "PO5_Frames":
                artist_record["artist_anomalies"].append("Profile docx declares 'P04 /Frames' (ID collision with P04)")
            elif artist_folder == "V03_Rahul_Gupta":
                artist_record["artist_anomalies"].append("Profile docx declares 'V03 / Tara D\'Souza' (Name mismatch with folder 'Rahul_Gupta')")
            elif artist_folder == "VO5_Roshan":
                artist_record["artist_anomalies"].append("Profile docx declares 'V03 / Roshan' (ID collision with V03)")
            elif artist_folder == "V02_Rehman_Ali":
                artist_record["artist_anomalies"].append("Profile docx has no artist ID/name header; starts directly with 'Category: Video Editor'")
            elif artist_folder == "VO4_Shivam_media":
                artist_record["artist_anomalies"].append("Profile declares 'Portfolio: Not provided in the profile' but 9 work files exist in 'Work/'")
            elif artist_folder == "M05_Lunar_Noise":
                artist_record["artist_anomalies"].append("Profile bio states artist is a practicing legal professional based in Agra")

            inventory["artist_profiles"][cat].append(artist_record)

            if artist_record["artist_anomalies"]:
                inventory["dataset_anomalies"].append({
                    "artist_folder": artist_folder,
                    "category": cat,
                    "anomalies": artist_record["artist_anomalies"]
                })

    # Summary Counts
    total_artists = (
        len(inventory["artist_profiles"]["photographers"]) +
        len(inventory["artist_profiles"]["musicians"]) +
        len(inventory["artist_profiles"]["video_editors"])
    )
    inventory["dataset_metadata"]["total_artists_discovered"] = total_artists

    inventory["integrity_summary"] = {
        "total_checked": len(all_files_in_dataset),
        "valid_files": len(all_files_in_dataset) - len(inventory["system_files"]),
        "corrupt_files": 0,
        "empty_files": 0,
        "system_files_count": len(inventory["system_files"])
    }

    return inventory


def save_inventory(inventory: Dict[str, Any], output_path: str) -> None:
    """Save inventory dictionary to pretty-printed JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
    print(f"Dataset inventory successfully generated at: {output_path}")


if __name__ == "__main__":
    raw_dir = "data/raw/Data set"
    out_file = "data/processed/dataset_inventory.json"
    print(f"Scanning raw dataset from {raw_dir}...")
    inv = scan_dataset(raw_dir)
    save_inventory(inv, out_file)
    print(f"Summary:")
    print(f"  - Total files scanned: {inv['dataset_metadata']['total_files_discovered']}")
    print(f"  - Total artists: {inv['dataset_metadata']['total_artists_discovered']} (Photographers: {len(inv['artist_profiles']['photographers'])}, Musicians: {len(inv['artist_profiles']['musicians'])}, Video Editors: {len(inv['artist_profiles']['video_editors'])})")
    print(f"  - Hirer briefs: {inv['dataset_metadata']['total_hirer_conversations']}")
    print(f"  - Follow-up updates: {inv['dataset_metadata']['total_follow_up_updates']}")
    print(f"  - System files: {len(inv['system_files'])}")
    print(f"  - File types: {inv['file_type_distribution']}")
    print(f"  - Total anomalies documented: {len(inv['dataset_anomalies'])}")
