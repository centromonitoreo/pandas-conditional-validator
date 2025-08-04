"""
Protocols (interfaces) para el sistema de validación de condiciones
"""
from .validation_protocols import (
    ColumnValidator,
    RangeValidator,
    ExpressionValidator,
    CompositeValidator
)

__all__ = [
    'ColumnValidator',
    'RangeValidator', 
    'ExpressionValidator',
    'CompositeValidator'
]
