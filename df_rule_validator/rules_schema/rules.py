"""Schemas representing complete validation rules.

This module builds upon the individual condition schemas to provide
higher level rule structures that may include conditional logic and
parameter validation.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Union, Literal

from pydantic import BaseModel, Field, field_validator

from .conditions import (
    BaseCondition,
    SimpleCondition,
    CompositeCondition,
    ConditionValidator,
    ConcreteConditionFactory,
)


class ConditionalRule(BaseCondition):
    """Rule that evaluates a condition only if another one is satisfied."""

    type: Literal["conditional"]
    if_: Union[SimpleCondition, CompositeCondition] = Field(..., alias="if")
    then: Union[SimpleCondition, CompositeCondition]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "if_": self.if_.to_dict(),
            "then": self.then.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConditionalRule":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        validator.validate_required_field(data, "if", "ConditionalRule")
        validator.validate_required_field(data, "then", "ConditionalRule")

        if_data = data["if"]
        validator.validate_field_type(if_data, dict, "if", "ConditionalRule")
        if if_data.get("type") == "composite":
            if_condition = CompositeCondition.from_dict(if_data)
        else:
            if_condition = factory.create_condition(if_data)

        then_data = data["then"]
        if isinstance(then_data, dict):
            if then_data.get("type") == "composite":
                then_condition = CompositeCondition.from_dict(then_data)
            else:
                then_condition = factory.create_condition(then_data)
        else:
            then_condition = then_data

        return cls(**{"if": if_condition, "then": then_condition, "type": data["type"]})


RuleType = Union[SimpleCondition, CompositeCondition, ConditionalRule]


class RuleValidator:
    """Utility class dedicated to validating rule names."""

    @staticmethod
    def validate_rule_name(name: str) -> str:
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            raise ValueError(
                "El nombre de la regla debe comenzar con una letra o guion bajo y "
                "contener solo letras, números y guiones bajos."
            )
        return name


class ParametricRule(BaseModel):
    """Rule that associates a name with a condition."""

    name: str
    condition: RuleType

    @field_validator("name", mode="before")
    def validate_name(cls, v: str) -> str:  # noqa: D401 - short description inherited
        return RuleValidator.validate_rule_name(v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParametricRule":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        validator.validate_required_field(data, "name", "ParametricRule")
        validator.validate_required_field(data, "condition", "ParametricRule")

        condition_data = data["condition"]
        if isinstance(condition_data, dict):
            condition_type = condition_data.get("type")
            if condition_type == "conditional":
                condition = ConditionalRule.from_dict(condition_data)
            elif condition_type == "composite":
                condition = CompositeCondition.from_dict(condition_data)
            else:
                condition = factory.create_condition(condition_data)
        else:
            condition = condition_data

        return cls(name=data["name"], condition=condition)
