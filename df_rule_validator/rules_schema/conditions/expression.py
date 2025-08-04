from __future__ import annotations

"""Expression-based condition schemas."""

from typing import Any, Dict, Union, Literal

from .base import BaseCondition, ConditionValidator


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
