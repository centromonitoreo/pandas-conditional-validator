"""
Factory para crear validadores específicos usando protocols
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..protocols import ColumnValidator, RangeValidator, ExpressionValidator, CompositeValidator
    from ..conditions import ValidatedCondition

from ..conditions import (
    GreaterThanCondition,
    LessThanCondition,
    BetweenCondition,
    ExpressionCondition,
    GreaterOrEqualCondition,
    LessOrEqualCondition,
    EqualCondition,
    NotEqualCondition,
    CompositeCondition,
    ValidatedCondition
)


class ConditionValidatorFactory:
    """Factory que crea validadores específicos usando protocols"""
    
    _validators = {
        "greater_than": GreaterThanCondition,
        "less_than": LessThanCondition,
        "between": BetweenCondition,
        "expression": ExpressionCondition,
        "greater_or_equal": GreaterOrEqualCondition,
        "less_or_equal": LessOrEqualCondition,
        "equal": EqualCondition,
        "not_equal": NotEqualCondition,
        "composite": CompositeCondition
    }
    
    @classmethod
    def create_validator(cls, condition_type: str) -> 'ValidatedCondition':
        """Crea un validador del tipo especificado"""
        if condition_type not in cls._validators:
            raise ValueError(f"Tipo de condición '{condition_type}' no soportado. "
                           f"Tipos disponibles: {list(cls._validators.keys())}")
        
        return cls._validators[condition_type]()
    
    @classmethod
    def create_column_validator(cls, condition_type: str) -> 'ColumnValidator':
        """Crea un validador que implementa ColumnValidator protocol"""
        column_validators = ["greater_than", "less_than", "greater_or_equal", 
                           "less_or_equal", "equal", "not_equal"]
        
        if condition_type not in column_validators:
            raise ValueError(f"Tipo '{condition_type}' no es un validador de columna. "
                           f"Disponibles: {column_validators}")
        
        validator = cls.create_validator(condition_type)
        
        # Import aquí para evitar circular imports
        from ..protocols import ColumnValidator
        if not isinstance(validator, ColumnValidator):
            raise TypeError(f"El validador {condition_type} no implementa ColumnValidator")
        
        return validator
    
    @classmethod
    def create_range_validator(cls) -> 'RangeValidator':
        """Crea un validador que implementa RangeValidator protocol"""
        validator = cls.create_validator("between")
        
        # Import aquí para evitar circular imports
        from ..protocols import RangeValidator
        if not isinstance(validator, RangeValidator):
            raise TypeError("BetweenCondition debe implementar RangeValidator")
        
        return validator
    
    @classmethod
    def create_expression_validator(cls) -> 'ExpressionValidator':
        """Crea un validador que implementa ExpressionValidator protocol"""
        validator = cls.create_validator("expression")
        
        # Import aquí para evitar circular imports
        from ..protocols import ExpressionValidator
        if not isinstance(validator, ExpressionValidator):
            raise TypeError("ExpressionCondition debe implementar ExpressionValidator")
        
        return validator
    
    @classmethod
    def create_composite_validator(cls) -> 'CompositeValidator':
        """Crea un validador que implementa CompositeValidator protocol"""
        validator = cls.create_validator("composite")
        
        # Import aquí para evitar circular imports
        from ..protocols import CompositeValidator
        if not isinstance(validator, CompositeValidator):
            raise TypeError("CompositeCondition debe implementar CompositeValidator")
        
        return validator
    
    @classmethod
    def register_validator(cls, condition_type: str, validator_class: type) -> None:
        """Registra un nuevo tipo de validador (extensibilidad)"""
        if not issubclass(validator_class, ValidatedCondition):
            raise ValueError("El validador debe heredar de ValidatedCondition")
        
        cls._validators[condition_type] = validator_class
    
    @classmethod
    def get_available_types(cls) -> list:
        """Retorna los tipos de condición disponibles"""
        return list(cls._validators.keys())
