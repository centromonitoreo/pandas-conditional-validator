"""
Versión refactorizada aplicando principios SOLID
"""
from typing import List, Union, Optional, Literal, Dict, Any, Protocol
from pydantic import BaseModel, Field, field_validator
from abc import ABC, abstractmethod
import yaml
import re



class ConditionProtocol(Protocol):
    """Protocolo que define la interfaz común para todas las condiciones"""
    type: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la condición a diccionario"""
        ...


class ConditionFactory(Protocol):
    """Factory para crear condiciones desde diccionarios"""
    
    @abstractmethod
    def create_condition(self, data: Dict[str, Any]) -> ConditionProtocol:
        """Crea una condición desde un diccionario"""
        ...



class ConditionValidator:
    """Responsabilidad única: validar datos de condiciones"""
    
    @staticmethod
    def validate_required_field(data: Dict[str, Any], field: str, context: str) -> None:
        if field not in data:
            raise ValueError(f"El campo '{field}' es obligatorio en {context}.")
    
    @staticmethod
    def validate_field_type(value: Any, expected_type: type, field: str, context: str) -> None:
        if not isinstance(value, expected_type):
            raise ValueError(f"El campo '{field}' debe ser de tipo {expected_type.__name__} en {context}.")
    
    @staticmethod
    def validate_condition_type(data: Dict[str, Any]) -> None:
        if "type" not in data:
            raise ValueError("Cada condición debe tener un campo 'type'.")


# 3. OPEN/CLOSED: Base abstracta para condiciones
class BaseCondition(BaseModel, ABC):
    """Clase base abstracta para todas las condiciones"""
    type: str
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la condición a diccionario"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseCondition":
        """Crea una instancia desde un diccionario"""
        pass


# 4. INTERFACE SEGREGATION: Condiciones específicas con interfaces mínimas
class ComparisonCondition(BaseCondition):
    """Condición de comparación simple"""
    type: Literal["greater_than", "greater_or_equal", "less_or_equal", "less_than"]
    col: str
    value: Union[float, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "col": self.col, "value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComparisonCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "col", "ComparisonCondition")
        validator.validate_required_field(data, "value", "ComparisonCondition")
        validator.validate_required_field(data, "type", "ComparisonCondition")
        
        return cls(**data)


class RangeCondition(BaseCondition):
    """Condición de rango"""
    type: Literal["between"]
    col: str
    min: Union[float, str]
    max: Union[float, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "col": self.col, "min": self.min, "max": self.max}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RangeCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "col", "RangeCondition")
        validator.validate_required_field(data, "min", "RangeCondition")
        validator.validate_required_field(data, "max", "RangeCondition")
        
        return cls(**data)


class ExpressionCondition(BaseCondition):
    """Condición de expresión"""
    type: Literal["expression"]
    expr: str
    operator: Literal[">", "<", ">=", "<=", "==", "!="]
    value: Union[float, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "expr": self.expr, "operator": self.operator, "value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExpressionCondition":
        validator = ConditionValidator()
        validator.validate_required_field(data, "expr", "ExpressionCondition")
        validator.validate_required_field(data, "operator", "ExpressionCondition")
        validator.validate_required_field(data, "value", "ExpressionCondition")
        
        return cls(**data)


# 5. SINGLE RESPONSIBILITY: Factory específico para crear condiciones
class ConcreteConditionFactory:
    """Factory concreto para crear condiciones simples"""
    
    _condition_map = {
        "greater_than": ComparisonCondition,
        "greater_or_equal": ComparisonCondition,
        "less_or_equal": ComparisonCondition,
        "less_than": ComparisonCondition,
        "between": RangeCondition,
        "expression": ExpressionCondition,
    }
    
    def create_condition(self, data: Dict[str, Any]) -> BaseCondition:
        ConditionValidator.validate_condition_type(data)
        
        condition_type = data["type"]
        if condition_type not in self._condition_map:
            raise ValueError(f"Tipo de condición no soportado: {condition_type}")
        
        condition_class = self._condition_map[condition_type]
        return condition_class.from_dict(data)


# Mantener compatibilidad con SimpleCondition original
SimpleCondition = Union[ComparisonCondition, RangeCondition, ExpressionCondition]


class CompositeCondition(BaseCondition):
    """Condición compuesta con mejor separación de responsabilidades"""
    type: Literal["composite"]
    operator: Literal["AND", "OR"]
    conditions: List[Union[SimpleCondition, "CompositeCondition"]]
    
    def __init__(self, **data):
        super().__init__(**data)
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "operator": self.operator,
            "conditions": [cond.to_dict() for cond in self.conditions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompositeCondition":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        
        # Validaciones específicas
        validator.validate_required_field(data, "operator", "CompositeCondition")
        validator.validate_required_field(data, "conditions", "CompositeCondition")
        validator.validate_field_type(data["conditions"], list, "conditions", "CompositeCondition")
        
        # Procesar condiciones anidadas
        processed_conditions = []
        for cond_data in data["conditions"]:
            if isinstance(cond_data, dict):
                if cond_data.get("type") == "composite":
                    processed_conditions.append(cls.from_dict(cond_data))
                else:
                    processed_conditions.append(factory.create_condition(cond_data))
            else:
                processed_conditions.append(cond_data)
        
        return cls(
            type=data["type"],
            operator=data["operator"],
            conditions=processed_conditions
        )


# Actualizar referencias
CompositeCondition.model_rebuild()


class ConditionalRule(BaseCondition):
    """Regla condicional con mejor separación de responsabilidades"""
    type: Literal["conditional"]
    if_: Union[SimpleCondition, CompositeCondition] = Field(..., alias="if")
    then: Union[SimpleCondition, CompositeCondition]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "if_": self.if_.to_dict(),
            "then": self.then.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConditionalRule":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        
        validator.validate_required_field(data, "if", "ConditionalRule")
        validator.validate_required_field(data, "then", "ConditionalRule")
        
        # Procesar condición 'if'
        if_data = data["if"]
        validator.validate_field_type(if_data, dict, "if", "ConditionalRule")
        
        if if_data.get("type") == "composite":
            if_condition = CompositeCondition.from_dict(if_data)
        else:
            if_condition = factory.create_condition(if_data)
        
        # Procesar condición 'then'
        then_data = data["then"]
        if isinstance(then_data, dict):
            if then_data.get("type") == "composite":
                then_condition = CompositeCondition.from_dict(then_data)
            else:
                then_condition = factory.create_condition(then_data)
        else:
            then_condition = then_data
        
        return cls(**{"if": if_condition, "then": then_condition, "type": data["type"]})


# Tipo unión actualizado
RuleType = Union[SimpleCondition, CompositeCondition, ConditionalRule]


class RuleValidator:
    """Responsabilidad única: validar reglas paramétricas"""
    
    @staticmethod
    def validate_rule_name(name: str) -> str:
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            raise ValueError(
                "El nombre de la regla debe comenzar con una letra o guion bajo y "
                "contener solo letras, números y guiones bajos."
            )
        return name


class ParametricRule(BaseModel):
    """Regla paramétrica con validación separada"""
    name: str
    condition: RuleType
    
    @field_validator("name", mode="before")
    def validate_name(cls, v: str) -> str:
        return RuleValidator.validate_rule_name(v)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParametricRule":
        validator = ConditionValidator()
        factory = ConcreteConditionFactory()
        
        validator.validate_required_field(data, "name", "ParametricRule")
        validator.validate_required_field(data, "condition", "ParametricRule")
        
        condition_data = data["condition"]
        
        if isinstance(condition_data, dict):
            condition_type = condition_data.get("type")
            
            if condition_type == "conditional":
                condition = ConditionalRule.from_dict(condition_data)
            elif condition_type == "composite":
                condition = CompositeCondition.from_dict(condition_data)
            else:
                condition = factory.create_condition(condition_data)
        else:
            condition = condition_data
        
        return cls(name=data["name"], condition=condition)


# 6. DEPENDENCY INVERSION: Interfaz para carga de configuración
class ConfigLoader(ABC):
    """Interfaz abstracta para cargar configuraciones"""
    
    @abstractmethod
    def load(self, source: str) -> Dict[str, Any]:
        """Carga datos desde una fuente"""
        pass


class YamlConfigLoader(ConfigLoader):
    """Implementación concreta para YAML"""
    
    def load(self, source: str) -> Dict[str, Any]:
        with open(source, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


class RulesConfig(BaseModel):
    """Configuración de reglas con mejor separación de responsabilidades"""
    validations: List[ParametricRule] = None
    
    @classmethod
    def from_source(cls, source: str, loader: ConfigLoader) -> "RulesConfig":
        """Carga configuración usando un loader específico"""
        raw_data = loader.load(source)
        return cls._build_from_data(raw_data)
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "RulesConfig":
        """Método de conveniencia para YAML (mantiene compatibilidad)"""
        loader = YamlConfigLoader()
        return cls.from_source(yaml_path, loader)
    
    @classmethod
    def _build_from_data(cls, raw_data: Dict[str, Any]) -> "RulesConfig":
        """Construye la configuración desde datos brutos"""
        params_raw = raw_data.get("validations")
        if not isinstance(params_raw, list):
            raise ValueError(
                "El archivo debe contener una lista de validaciones bajo la clave 'validations'."
            )
        
        validations = []
        for param in params_raw:
            validations.append(ParametricRule.from_dict(param))
        
        return cls(validations=validations)
