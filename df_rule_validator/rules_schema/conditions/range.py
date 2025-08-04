from __future__ import annotations

"""Range-based condition schemas."""

from typing import Any, Dict, Union, Literal

from .base import BaseCondition, ConditionValidator


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
