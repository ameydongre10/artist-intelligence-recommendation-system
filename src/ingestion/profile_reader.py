"""
Safe Profile Reader.
Parses .docx profile files into raw text and structured ProfileMetadata without altering files.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from typing import Tuple, Optional, Dict, Any
from src.utils.errors import FileNotFoundCustomError, FileUnreadableError
from src.models.artist import ProfileMetadata
from scripts.inventory_dataset import parse_profile_text, get_docx_text


def read_profile_document(docx_path: str) -> Tuple[str, ProfileMetadata]:
    """
    Reads a docx profile document safely and returns (raw_text, ProfileMetadata).
    """
    if not os.path.exists(docx_path):
        raise FileNotFoundCustomError(docx_path)

    raw_text, integrity = get_docx_text(docx_path)
    if integrity != "OK":
        raise FileUnreadableError(docx_path, f"Integrity check failed with: {integrity}")

    parsed = parse_profile_text(raw_text)
    metadata = ProfileMetadata(
        raw_bio=parsed.get("declared_bio"),
        location=parsed.get("declared_location"),
        work_preference=parsed.get("declared_work_preference"),
        declared_portfolio_claims=parsed.get("declared_portfolio_refs", [])
    )
    return raw_text, metadata
