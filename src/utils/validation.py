"""
Validation Utilities for Domain Models and Mandatory Artifacts.
"""

from typing import Type, TypeVar, Any, Dict, List
from pydantic import BaseModel, ValidationError
from src.utils.errors import InvalidSchemaError

T = TypeVar("T", bound=BaseModel)


def validate_schema(model_class: Type[T], data: Any) -> T:
    """
    Validate data against a Pydantic model class.
    Raises InvalidSchemaError if validation fails.
    """
    try:
        if isinstance(data, model_class):
            return data
        return model_class.model_validate(data)
    except ValidationError as e:
        raise InvalidSchemaError(model_name=model_class.__name__, errors=e.errors())


def validate_jsonl_records(model_class: Type[T], records: List[Dict[str, Any]]) -> List[T]:
    """
    Validate a list of JSONL dictionary records against a Pydantic model class.
    """
    validated: List[T] = []
    for idx, rec in enumerate(records):
        try:
            validated.append(model_class.model_validate(rec))
        except ValidationError as e:
            raise InvalidSchemaError(
                model_name=model_class.__name__,
                errors=f"Record #{idx} validation failed: {e.errors()}",
                details={"record_index": idx, "raw_record": rec}
            )
    return validated
