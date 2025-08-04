"""
Condiciones para evaluación de expresiones
"""
import pandas as pd
from .base import ValidatedCondition


class ExpressionCondition(ValidatedCondition):
    """Validador para evaluación de expresiones sobre DataFrame"""

    def validate_condition(self, df: pd.DataFrame, expr: str, **kwargs) -> pd.Series:
        """Evalúa una expresión sobre el DataFrame y devuelve un mask booleano."""
        self.validate_input(df)
        self._validate_expression(expr)
        
        try:
            result = df.eval(expr)
            self._validate_boolean_result(result, expr)
            return result
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión '{expr}': {e}")
    
    def _validate_expression(self, expr: str) -> None:
        if not isinstance(expr, str) or not expr.strip():
            raise ValueError("La expresión debe ser una cadena no vacía")
    
    def _validate_boolean_result(self, result: pd.Series, expr: str) -> None:
        if not pd.api.types.is_bool_dtype(result):
            raise ValueError(f"La expresión '{expr}' debe retornar valores booleanos")
