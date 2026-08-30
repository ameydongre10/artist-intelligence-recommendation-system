"""
Safe File Utilities for Reading and Writing Processed Artifacts (JSON, JSONL, TXT).
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Generator
from src.utils.errors import FileNotFoundCustomError, FileUnreadableError


def resolve_path(relative_or_absolute_path: str, base_dir: str = ".") -> Path:
    """Resolve a file path safely relative to base directory."""
    p = Path(relative_or_absolute_path)
    if not p.is_absolute():
        p = Path(base_dir) / p
    return p.resolve()


def read_json_file(file_path: str) -> Dict[str, Any]:
    """Safely read and parse a JSON file."""
    path = resolve_path(file_path)
    if not path.exists():
        raise FileNotFoundCustomError(str(path))
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise FileUnreadableError(str(path), f"JSON parse error: {e}")


def write_json_file(data: Any, file_path: str, indent: int = 2) -> None:
    """Safely write a dictionary or list to a JSON file."""
    path = resolve_path(file_path)
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_jsonl_file(file_path: str) -> List[Dict[str, Any]]:
    """Safely read all lines from a JSONL file into a list of dictionaries."""
    path = resolve_path(file_path)
    if not path.exists():
        raise FileNotFoundCustomError(str(path))
    records: List[Dict[str, Any]] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                clean_line = line.strip()
                if clean_line:
                    records.append(json.loads(clean_line))
        return records
    except Exception as e:
        raise FileUnreadableError(str(path), f"JSONL parse error on line: {e}")


def write_jsonl_file(records: List[Dict[str, Any]], file_path: str) -> None:
    """Safely write a list of dictionaries to a JSONL file (one JSON object per line)."""
    path = resolve_path(file_path)
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_text_file(file_path: str) -> str:
    """Safely read a text file."""
    path = resolve_path(file_path)
    if not path.exists():
        raise FileNotFoundCustomError(str(path))
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        raise FileUnreadableError(str(path), f"Text read error: {e}")
