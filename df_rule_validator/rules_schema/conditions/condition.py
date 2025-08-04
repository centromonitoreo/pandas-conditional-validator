from __future__ import annotations

"""Conditional condition schema."""

from typing import Any, Dict, List, Union, Literal, TYPE_CHECKING

from .base import BaseCondition, ConditionValidator
from .comparison import ComparisonCondition
from .range import RangeCondition
from .expression import ExpressionCondition
from .factory import ConcreteConditionFactory

if TYPE_CHECKING:
    from .composite import CompositeCondition

SimpleCondition = Union[ComparisonCondition, RangeCondition, ExpressionCondition]


class CondicionalCondition(BaseCondition):
    """Schema representing a conditional condition (if-then logic)."""

    type: Literal["conditional"]
    if_: Union[SimpleCondition, "CondicionalCondition", "CompositeCondition"]
    then: Union[SimpleCondition, "CondicionalCondition", "CompositeCondition"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "if_": self.if_.to_dict(),
            "then": self.then.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CondicionalCondition":
        # Importación diferida para evitar ciclo de importación
        from .composite import CompositeCondition
        
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        
        if_key = "if" if "if" in data else "if_"
        validator.validate_required_field(data, if_key, "CondicionalCondition")
        validator.validate_required_field(data, "then", "CondicionalCondition")
        
        # Process if_ condition
        if_condition = None
        if_data = data[if_key]
        if isinstance(if_data, dict):
            if if_data.get("type") == "conditional":
                if_condition = cls.from_dict(if_data)
            elif if_data.get("type") == "composite":
                if_condition = CompositeCondition.from_dict(if_data)
            else:
                if_condition = factory.create_condition(if_data)
        else:
            if_condition = if_data
        
        # Process then condition
        then_condition = None
        then_data = data["then"]
        if isinstance(then_data, dict):
            if then_data.get("type") == "conditional":
                then_condition = cls.from_dict(then_data)
            elif then_data.get("type") == "composite":
                then_condition = CompositeCondition.from_dict(then_data)
            else:
                then_condition = factory.create_condition(then_data)
        else:
            then_condition = then_data

        return cls(
            type=data["type"],
            if_=if_condition,
            then=then_condition,
        )
