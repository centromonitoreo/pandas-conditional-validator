"""Schema definitions for individual conditions.

This module contains Pydantic models that describe the supported
conditions that can appear in the YAML rule configuration.  The goal of
this layer is to keep the conversion from raw dictionaries into typed
objects isolated from other concerns of the project.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol, Union, Literal, runtime_checkable

from pydantic import BaseModel


@runtime_checkable
class ConditionProtocol(Protocol):
    """Common interface that all condition schemas must implement."""

    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the condition."""
        ...


@runtime_checkable
class ConditionFactory(Protocol):
    """Protocol for objects capable of building conditions from dictionaries."""

    @abstractmethod
    def create_condition(self, data: Dict[str, Any]) -> "ConditionProtocol":
        """Create a condition from a dictionary."""
        ...


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


class ComparisonCondition(BaseCondition):
    """Schema for simple comparison conditions."""

    type: Literal["greater_than", "greater_or_equal", "less_or_equal", "less_than"]
    col: str
    value: Union[float, str]

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "col": self.col, "value": self.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComparisonCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "col", "ComparisonCondition")
        validator.validate_required_field(data, "value", "ComparisonCondition")
        validator.validate_required_field(data, "type", "ComparisonCondition")
        return cls(**data)


class RangeCondition(BaseCondition):
    """Schema for range-based conditions."""

    type: Literal["between"]
    col: str
    min: Union[float, str]
    max: Union[float, str]

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "col": self.col, "min": self.min, "max": self.max}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RangeCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "col", "RangeCondition")
        validator.validate_required_field(data, "min", "RangeCondition")
        validator.validate_required_field(data, "max", "RangeCondition")
        return cls(**data)


class ExpressionCondition(BaseCondition):
    """Schema for expression-based conditions."""

    type: Literal["expression"]
    expr: str
    operator: Literal[">", "<", ">=", "<=", "==", "!="]
    value: Union[float, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "expr": self.expr,
            "operator": self.operator,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExpressionCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "expr", "ExpressionCondition")
        validator.validate_required_field(data, "operator", "ExpressionCondition")
        validator.validate_required_field(data, "value", "ExpressionCondition")
        return cls(**data)


class ConcreteConditionFactory(ConditionFactory):
    """Factory responsible for instantiating concrete condition schemas."""

    _condition_map = {
        "greater_than": ComparisonCondition,
        "greater_or_equal": ComparisonCondition,
        "less_or_equal": ComparisonCondition,
        "less_than": ComparisonCondition,
        "between": RangeCondition,
        "expression": ExpressionCondition,
    }

    def create_condition(self, data: Dict[str, Any]) -> BaseCondition:
        ConditionValidator.validate_condition_type(data)
        condition_type = data["type"]
        if condition_type not in self._condition_map:
            raise ValueError(f"Tipo de condición no soportado: {condition_type}")
        condition_class = self._condition_map[condition_type]
        condition = condition_class.from_dict(data)
        if not isinstance(condition, ConditionProtocol):
            raise TypeError(
                f"{condition_class.__name__} debe implementar ConditionProtocol"
            )
        return condition


# Alias to keep backwards compatibility with previous naming
SimpleCondition = Union[ComparisonCondition, RangeCondition, ExpressionCondition]


class CompositeCondition(BaseCondition):
    """Schema representing a composite condition."""

    type: Literal["composite"]
    operator: Literal["AND", "OR"]
    conditions: List[Union[SimpleCondition, "CompositeCondition"]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "operator": self.operator,
            "conditions": [cond.to_dict() for cond in self.conditions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompositeCondition":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        validator.validate_required_field(data, "operator", "CompositeCondition")
        validator.validate_required_field(data, "conditions", "CompositeCondition")
        validator.validate_field_type(data["conditions"], list, "conditions", "CompositeCondition")

        processed_conditions = []
        for cond_data in data["conditions"]:
            if isinstance(cond_data, dict):
                if cond_data.get("type") == "composite":
                    processed_conditions.append(cls.from_dict(cond_data))
                else:
                    processed_conditions.append(factory.create_condition(cond_data))
            else:
                processed_conditions.append(cond_data)

        return cls(
            type=data["type"],
            operator=data["operator"],
            conditions=processed_conditions,
        )


CompositeCondition.model_rebuild()
