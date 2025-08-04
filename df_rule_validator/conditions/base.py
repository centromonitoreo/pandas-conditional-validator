"""
Clases base y abstractas para el sistema de validación
"""
from abc import ABC, abstractmethod
import pandas as pd


class ValidatedCondition(ABC):
    """Clase base abstracta para todas las condiciones de validación"""

    @abstractmethod
    def validate_condition(self, df: pd.DataFrame, *args, **kwargs) -> pd.Series:
        """Método abstracto para validar la condición sobre un DataFrame"""
        pass
    
    def get_condition_type(self) -> str:
        """Retorna el tipo de condición para identificación"""
        return self.__class__.__name__.replace("Condition", "").lower()
    
    def validate_input(self, df: pd.DataFrame) -> None:
        """Validación común de entrada"""
        if df.empty:
            raise ValueError("DataFrame no puede estar vacío")
