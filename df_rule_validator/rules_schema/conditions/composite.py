from __future__ import annotations

"""Composite condition schema."""

from typing import Any, Dict, List, Union, Literal, TYPE_CHECKING

from .base import BaseCondition, ConditionValidator
from .comparison import ComparisonCondition
from .range import RangeCondition
from .expression import ExpressionCondition
from .factory import ConcreteConditionFactory

if TYPE_CHECKING:
    from .condition import CondicionalCondition

SimpleCondition = Union[ComparisonCondition, RangeCondition, ExpressionCondition]


class CompositeCondition(BaseCondition):
    """Schema representing a composite condition."""

    type: Literal["composite"]
    operator: Literal["AND", "OR"]
    conditions: List[Union[SimpleCondition, "CompositeCondition", "CondicionalCondition"]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "operator": self.operator,
            "conditions": [cond.to_dict() for cond in self.conditions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompositeCondition":
        # Importación diferida para evitar ciclo de importación
        from .condition import CondicionalCondition
        
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        validator.validate_required_field(data, "operator", "CompositeCondition")
        validator.validate_required_field(data, "conditions", "CompositeCondition")
        validator.validate_field_type(data["conditions"], list, "conditions", "CompositeCondition")

        processed_conditions = []
        for cond_data in data["conditions"]:
            if isinstance(cond_data, dict):
                if cond_data.get("type") == "conditional":
                    processed_conditions.append(CondicionalCondition.from_dict(cond_data))
                elif cond_data.get("type") == "composite":
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
