from __future__ import annotations

"""Factory for building concrete condition schema instances."""

from typing import Dict, Any

from ..protocols import ConditionFactory, ConditionProtocol
from .base import BaseCondition, ConditionValidator
from .comparison import ComparisonCondition
from .range import RangeCondition
from .expression import ExpressionCondition


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
