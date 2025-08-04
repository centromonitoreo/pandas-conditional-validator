"""
Condiciones para validación de rangos
"""
import pandas as pd
from typing import Union
from .base import ValidatedCondition


class BetweenCondition(ValidatedCondition):
    """Validador para condición de rango (between)"""

    def validate_condition(self, df: pd.DataFrame, col: str, min_value: Union[float, int], max_value: Union[float, int]) -> pd.Series:
        """Valida si los valores en la columna están entre los valores dados."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        self._validate_numeric_values(min_value, max_value)
        self._validate_range_logic(min_value, max_value)
        
        return (df[col] >= min_value) & (df[col] <= max_value)
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
    
    def _validate_numeric_values(self, min_value: Union[float, int], max_value: Union[float, int]) -> None:
        if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
            raise ValueError("Los valores mínimo y máximo deben ser numéricos")
    
    def _validate_range_logic(self, min_value: Union[float, int], max_value: Union[float, int]) -> None:
        if min_value > max_value:
            raise ValueError(f"El valor mínimo ({min_value}) no puede ser mayor que el máximo ({max_value})")
