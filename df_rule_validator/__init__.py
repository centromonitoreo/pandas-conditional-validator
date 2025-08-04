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

# Esquemas y configuración
from .rules_schema import (
    RulesConfig,
    ParametricRule,
    ConditionalRule,
    CompositeCondition as SchemaCompositeCondition,
    ComparisonCondition,
    RangeCondition,
    ExpressionCondition as SchemaExpressionCondition
)


# Alias para compatibilidad con versiones anteriores
rules_schema_refactored = __import__(__name__ + '.rules_schema', fromlist=[''])


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
    
    # Configuración y esquemas
    'RulesConfig',
    'ParametricRule',
    'ConditionalRule',
    'SchemaCompositeCondition',
    'ComparisonCondition',
    'RangeCondition',
    'SchemaExpressionCondition',
    
    
    # Compatibilidad
    'rules_schema',
]