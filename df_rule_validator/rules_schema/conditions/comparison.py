from __future__ import annotations

"""Comparison-based condition schemas."""

from typing import Any, Dict, Union, Literal

from .base import BaseCondition, ConditionValidator


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
