"""
Condiciones compuestas que combinan múltiples validaciones
"""
import pandas as pd
from .base import ValidatedCondition
from ..services.factory import ConditionValidatorFactory

class CompositeCondition(ValidatedCondition):
    """Condición compuesta que combina múltiples condiciones con operadores lógicos"""

    def __init__(self):
        self._operators = {
            "AND": self._and_operation,
            "OR": self._or_operation,
            "NOT": self._not_operation
        }
        self.factory = ConditionValidatorFactory()

    def validate_condition(self, df: pd.DataFrame, conditions: list, operator: str = "AND") -> pd.Series:
        """Combina múltiples condiciones con el operador especificado."""
        self.validate_input(df)
        self._validate_conditions(conditions)
        self._validate_operator(operator)
        
        if not conditions:
            raise ValueError("La lista de condiciones no puede estar vacía")
        
        resolved_conditions = []
        for condition in conditions:
            condition_type = condition['type']
            sub_validator = self.factory.create_validator(condition_type)
            resolved_conditions.append(sub_validator.validate_condition(df, **condition['params']))
        
        return self._operators[operator.upper()](resolved_conditions)
    
    def _validate_conditions(self, conditions: list) -> None:
        if not isinstance(conditions, list):
            raise ValueError("Las condiciones deben ser una lista")
        
        for i, condition in enumerate(conditions):
            if not isinstance(condition, pd.Series):
                raise ValueError(f"La condición {i} debe ser una Serie de pandas")
            if not pd.api.types.is_bool_dtype(condition):
                raise ValueError(f"La condición {i} debe contener valores booleanos")
    
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
