from __future__ import annotations

"""Abstract bases and helpers for rule schema conditions."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel


class ConditionValidator:
    """Helper responsible solely for validating condition data."""

    @staticmethod
    def validate_required_field(data: Dict[str, Any], field: str, context: str) -> None:
        if field not in data:
            raise ValueError(f"El campo '{field}' es obligatorio en {context}.")

    @staticmethod
    def validate_field_type(value: Any, expected_type: type, field: str, context: str) -> None:
        if not isinstance(value, expected_type):
            raise ValueError(
                f"El campo '{field}' debe ser de tipo {expected_type.__name__} en {context}."
            )

    @staticmethod
    def validate_condition_type(data: Dict[str, Any]) -> None:
        if "type" not in data:
            raise ValueError("Cada condición debe tener un campo 'type'.")


class BaseCondition(BaseModel, ABC):
    """Abstract base class for all condition schemas."""

    type: str

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the condition."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseCondition":
        """Build an instance from a dictionary."""
        raise NotImplementedError
