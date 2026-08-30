"""Utils package."""
from src.utils.errors import (
    ArtistSystemError,
    FileNotFoundCustomError,
    FileUnreadableError,
    UnsupportedFormatError,
    InvalidSchemaError,
    InsufficientEvidenceError,
    IdentifierInconsistencyError,
    ProcessingFailedError
)
from src.utils.file_utils import (
    resolve_path,
    read_json_file,
    write_json_file,
    read_jsonl_file,
    write_jsonl_file,
    read_text_file
)
from src.utils.validation import validate_schema, validate_jsonl_records

__all__ = [
    "ArtistSystemError",
    "FileNotFoundCustomError",
    "FileUnreadableError",
    "UnsupportedFormatError",
    "InvalidSchemaError",
    "InsufficientEvidenceError",
    "IdentifierInconsistencyError",
    "ProcessingFailedError",
    "resolve_path",
    "read_json_file",
    "write_json_file",
    "read_jsonl_file",
    "write_jsonl_file",
    "read_text_file",
    "validate_schema",
    "validate_jsonl_records"
]
