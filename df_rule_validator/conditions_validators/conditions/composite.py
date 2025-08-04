"""
Condiciones compuestas que combinan múltiples validaciones
"""
import pandas as pd
from .base import ValidatedCondition

class CompositeCondition(ValidatedCondition):
    """Condición compuesta que combina múltiples condiciones con operadores lógicos"""

    def __init__(self):
        self._operators = {
            "AND": self._and_operation,
            "OR": self._or_operation,
            "NOT": self._not_operation
        }

    def validate_condition(self, df: pd.DataFrame, conditions: list, operator: str = "AND") -> pd.Series:
        """Combina múltiples condiciones con el operador especificado."""
        # Import here to avoid circular import
        from ..services.factory import ConditionValidatorFactory
        
        self.validate_input(df)
        self._validate_operator(operator)
        
        if not conditions:
            raise ValueError("La lista de condiciones no puede estar vacía")
        
        factory = ConditionValidatorFactory()
        resolved_conditions = []
        for condition in conditions:
            condition_type = condition['type']
            sub_validator = factory.create_validator(condition_type)
            condition.pop('type', None)
            resolved_conditions.append(sub_validator.validate_condition(df, **condition))
        
        return self._operators[operator.upper()](resolved_conditions)
    
    
    def _validate_operator(self, operator: str) -> None:
        if operator.upper() not in self._operators:
            raise ValueError(f"Operador '{operator}' no soportado. Usar: {list(self._operators.keys())}")
    
    def _and_operation(self, conditions: list) -> pd.Series:
        """Operación AND entre todas las condiciones"""
        result = conditions[0]
        for condition in conditions[1:]:
            result = result & condition
        return result
    
    def _or_operation(self, conditions: list) -> pd.Series:
        """Operación OR entre todas las condiciones"""
        result = conditions[0]
        for condition in conditions[1:]:
            result = result | condition
        return result
    
    def _not_operation(self, conditions: list) -> pd.Series:
        """Operación NOT (solo para la primera condición)"""
        return ~conditions[0]
