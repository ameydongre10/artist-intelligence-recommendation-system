"""
Safe Conversation Reader.
Reads and parses hirer conversation and follow-up files.
"""

import os
from typing import Dict, List, Any
from src.utils.file_utils import read_text_file
from src.utils.errors import FileNotFoundCustomError


def read_conversation_file(file_path: str) -> Dict[str, Any]:
    """
    Safely reads a conversation transcript and returns basic metadata and content.
    """
    content = read_text_file(file_path)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return {
        "file_path": file_path,
        "filename": os.path.basename(file_path),
        "raw_text": content,
        "line_count": len(lines),
        "char_count": len(content)
    }
