"""
Standard Error Hierarchy & Custom Exceptions for the Intelligence System.
"""

from typing import Optional, Dict, Any


class ArtistSystemError(Exception):
    """Base exception for the Artist Intelligence & Recommendation System."""
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class FileNotFoundCustomError(ArtistSystemError):
    def __init__(self, file_path: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="FILE_NOT_FOUND",
            message=f"Required file not found at path: {file_path}",
            details={"file_path": file_path, **(details or {})}
        )


class FileUnreadableError(ArtistSystemError):
    def __init__(self, file_path: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="FILE_UNREADABLE",
            message=f"File at {file_path} is unreadable: {reason}",
            details={"file_path": file_path, "reason": reason, **(details or {})}
        )


class UnsupportedFormatError(ArtistSystemError):
    def __init__(self, file_ext: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="UNSUPPORTED_FORMAT",
            message=f"File format '{file_ext}' is not supported by the processor",
            details={"extension": file_ext, **(details or {})}
        )


class InvalidSchemaError(ArtistSystemError):
    def __init__(self, model_name: str, errors: Any, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="INVALID_SCHEMA",
            message=f"Validation failed for schema '{model_name}'",
            details={"model": model_name, "validation_errors": str(errors), **(details or {})}
        )


class InsufficientEvidenceError(ArtistSystemError):
    def __init__(self, artist_id: str, capability_dimension: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="INSUFFICIENT_EVIDENCE",
            message=f"Insufficient evidence available to evaluate '{capability_dimension}' for artist '{artist_id}'",
            details={"artist_id": artist_id, "dimension": capability_dimension, **(details or {})}
        )


class IdentifierInconsistencyError(ArtistSystemError):
    def __init__(self, source_id: str, declared_id: Optional[str], details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="IDENTIFIER_INCONSISTENCY",
            message=f"Artist identifier mismatch between folder '{source_id}' and declared header '{declared_id}'",
            details={"source_folder_id": source_id, "declared_id": declared_id, **(details or {})}
        )


class ProcessingFailedError(ArtistSystemError):
    def __init__(self, target_entity: str, failure_reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="PROCESSING_FAILED",
            message=f"Processing failed for entity '{target_entity}': {failure_reason}",
            details={"target_entity": target_entity, "reason": failure_reason, **(details or {})}
        )
