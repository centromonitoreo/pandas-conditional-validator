"""
Protocols específicos para validación de condiciones en DataFrames
Aplicando Interface Segregation Principle (ISP) de SOLID
"""
import pandas as pd
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ColumnValidator(Protocol):
    """Protocolo para validadores que trabajan con columnas específicas"""
    
    def validate_condition(self, df: pd.DataFrame, col: str, value: Any) -> pd.Series:
        """Valida una condición en una columna específica"""
        ...
    
    def get_condition_type(self) -> str:
        """Retorna el tipo de condición"""
        ...


@runtime_checkable
class RangeValidator(Protocol):
    """Protocolo para validadores de rangos"""
    
    def validate_condition(self, df: pd.DataFrame, col: str, min_value: Any, max_value: Any) -> pd.Series:
        """Valida si los valores están en un rango"""
        ...
    
    def get_condition_type(self) -> str:
        """Retorna el tipo de condición"""
        ...


@runtime_checkable
class ExpressionValidator(Protocol):
    """Protocolo para validadores que evalúan expresiones"""
    
    def validate_condition(self, df: pd.DataFrame, expr: str, **kwargs) -> pd.Series:
        """Evalúa una expresión sobre el DataFrame"""
        ...
    
    def get_condition_type(self) -> str:
        """Retorna el tipo de condición"""
        ...


@runtime_checkable
class CompositeValidator(Protocol):
    """Protocolo para validadores compuestos"""
    
    def validate_condition(self, df: pd.DataFrame, conditions: list, operator: str = "AND") -> pd.Series:
        """Combina múltiples condiciones"""
        ...
    
    def get_condition_type(self) -> str:
        """Retorna el tipo de condición"""
        ...
