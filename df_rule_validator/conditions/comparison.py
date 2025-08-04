"""
Condiciones básicas de comparación para columnas individuales
"""
import pandas as pd
from typing import Union, Any
from .base import ValidatedCondition


class GreaterThanCondition(ValidatedCondition):
    """Validador para condición 'mayor que'"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Union[float, int]) -> pd.Series:
        """Valida si los valores en la columna son mayores que el valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        self._validate_numeric_value(value)
        
        return df[col] > value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
    
    def _validate_numeric_value(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"El valor debe ser numérico, recibido: {type(value)}")


class LessThanCondition(ValidatedCondition):
    """Validador para condición 'menor que'"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Union[float, int]) -> pd.Series:
        """Valida si los valores en la columna son menores que el valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        self._validate_numeric_value(value)
        
        return df[col] < value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
    
    def _validate_numeric_value(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"El valor debe ser numérico, recibido: {type(value)}")


class GreaterOrEqualCondition(ValidatedCondition):
    """Validador para condición 'mayor o igual que'"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Union[float, int]) -> pd.Series:
        """Valida si los valores en la columna son mayores o iguales que el valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        self._validate_numeric_value(value)
        
        return df[col] >= value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
    
    def _validate_numeric_value(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"El valor debe ser numérico, recibido: {type(value)}")


class LessOrEqualCondition(ValidatedCondition):
    """Validador para condición 'menor o igual que'"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Union[float, int]) -> pd.Series:
        """Valida si los valores en la columna son menores o iguales que el valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        self._validate_numeric_value(value)
        
        return df[col] <= value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
    
    def _validate_numeric_value(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"El valor debe ser numérico, recibido: {type(value)}")


class EqualCondition(ValidatedCondition):
    """Validador para condición de igualdad"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Any) -> pd.Series:
        """Valida si los valores en la columna son iguales al valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        
        return df[col] == value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")


class NotEqualCondition(ValidatedCondition):
    """Validador para condición de desigualdad"""

    def validate_condition(self, df: pd.DataFrame, col: str, value: Any) -> pd.Series:
        """Valida si los valores en la columna son diferentes al valor dado."""
        self.validate_input(df)
        self._validate_column_exists(df, col)
        
        return df[col] != value
    
    def _validate_column_exists(self, df: pd.DataFrame, col: str) -> None:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en el DataFrame")
