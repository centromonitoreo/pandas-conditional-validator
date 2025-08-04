"""
Módulo principal del sistema de validación de reglas para DataFrames
"""
# Protocols (Interfaces)
from .protocols import (
    ColumnValidator,
    RangeValidator,
    ExpressionValidator,
    CompositeValidator
)

# Condiciones base y concretas
from .conditions import (
    ValidatedCondition,
    GreaterThanCondition,
    LessThanCondition,
    GreaterOrEqualCondition,
    LessOrEqualCondition,
    EqualCondition,
    NotEqualCondition,
    BetweenCondition,
    ExpressionCondition,
    CompositeCondition
)

# Servicios implementados
from .services import (
    ValidationService,           # Servicio principal 
    ConditionValidatorFactory,   # Factory pattern
)



__all__ = [
    # Protocols
    'ColumnValidator',
    'RangeValidator',
    'ExpressionValidator', 
    'CompositeValidator',
    
    # Conditions
    'ValidatedCondition',
    'GreaterThanCondition',
    'LessThanCondition',
    'GreaterOrEqualCondition',
    'LessOrEqualCondition',
    'EqualCondition',
    'NotEqualCondition',
    'BetweenCondition',
    'ExpressionCondition',
    'CompositeCondition',
    
    # Services (principales)
    'ValidationService',          # ⭐ Servicio principal - usar este
    'ConditionValidatorFactory',  # Factory pattern
    
]