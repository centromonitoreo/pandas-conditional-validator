from typing import List, Union, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import yaml
import re


class SimpleCondition(BaseModel):
    type: Literal["greater_than", "greater_or_equal", "less_or_equal", "less_than", "between", "expression", "conditional"]
    col: Optional[str] = None
    value: Optional[Union[float, str]] = None  # Ahora puede ser string para parámetros
    min: Optional[Union[float, str]] = None
    max: Optional[Union[float, str]] = None
    expr: Optional[str] = None
    operator: Optional[Literal[">", "<", ">=", "<=", "==", "!="]] = None
   
class CompositeCondition(BaseModel):
    type: Literal["composite"]
    operator: Literal["AND", "OR"]
    conditions: List[Union["SimpleCondition", "CompositeCondition"]]

    @classmethod
    def from_dict(cls, **kwargs) -> "CompositeCondition":
        if not "operator" in kwargs:
            raise ValueError("El campo 'operator' es obligatorio en CompositeCondition.")
        
        if not "conditions" in kwargs:
            raise ValueError("El campo 'conditions' es obligatorio en CompositeCondition.")
        
        if not isinstance(kwargs["conditions"], list):
            raise ValueError("El campo 'conditions' debe ser una lista de condiciones.")
        
        # Validar que todas las condiciones sean del tipo correcto
        for cond in kwargs["conditions"]:
            if isinstance(cond, dict):
                if "type" not in cond:
                    raise ValueError("Cada condición debe tener un campo 'type'.")
                elif cond["type"] == "composite":
                    cond = CompositeCondition.from_dict(**cond)
                else:
                    cond = SimpleCondition(**cond)
            elif not isinstance(cond, (SimpleCondition, CompositeCondition)):
                raise ValueError("Las condiciones deben ser instancias de SimpleCondition o CompositeCondition.")
        
        return cls(type = kwargs['type'],operator=kwargs["operator"], conditions=kwargs["conditions"])


CompositeCondition.model_rebuild()

class ConditionalRule(BaseModel):
    type: Literal["conditional"]
    if_: Union[SimpleCondition, CompositeCondition] = Field(..., alias="if")
    then: Union[SimpleCondition, CompositeCondition]

    @classmethod
    def from_dict(cls, **kwargs) -> "ConditionalRule":
        if not "if" in kwargs:
            raise ValueError("El campo 'if' es obligatorio en ConditionalRule.")
        
        if not "then" in kwargs:
            raise ValueError("El campo 'then' es obligatorio en ConditionalRule.")
        
        data_if = kwargs["if"]
        if not isinstance(data_if, dict):
            raise ValueError("El campo 'if' debe ser un diccionario con la estructura de una condición.")
        
        if "type" not in data_if:
            raise ValueError("El campo 'if' debe contener el tipo de condición ('type').")
        
        elif data_if["type"] == "composite":
            kwargs["if"] = CompositeCondition.from_dict(**data_if)
        else:
            kwargs["if"] = SimpleCondition(**data_if)

        if isinstance(kwargs["then"], dict):
            if "type" not in kwargs["then"]:
                raise ValueError("El campo 'then' debe contener el tipo de condición ('type').")
            elif kwargs["then"]["type"] == "composite":
                kwargs["then"] = CompositeCondition.from_dict(**kwargs["then"])
            else:
                kwargs["then"] = SimpleCondition(**kwargs["then"])
        
        return cls(**kwargs)    

RuleType = Union[SimpleCondition, CompositeCondition, ConditionalRule]

class ParametricRule(BaseModel):
    name: str
    condition: RuleType

    @field_validator("name", mode="before")
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", v):
            raise ValueError("El nombre de la regla debe comenzar con una letra o guion bajo y contener solo letras, números y guiones bajos.")
        return v
    
    @classmethod
    def from_dict(cls, **kwargs) -> "ParametricRule":

        if not "name" in kwargs:
            raise ValueError("El campo 'name' es obligatorio en ParametricRule.")
        
        if "condition" not in kwargs:
            raise ValueError("El campo 'condition' es obligatorio en ParametricRule.")
        
        if isinstance(kwargs["condition"], dict) and kwargs["condition"].get("type") == "conditional":
            condition = ConditionalRule.from_dict(**kwargs["condition"])

        elif isinstance(kwargs["condition"], dict) and kwargs["condition"].get("type") == "composite":
            condition = CompositeCondition.from_dict(**kwargs["condition"])

        else:
            condition = SimpleCondition(**kwargs["condition"])

        return cls(name=kwargs["name"], condition=condition)
    

    
class RulesConfig(BaseModel):
    validations: List[ParametricRule] = None
    
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "RulesConfig":
        with open(yaml_path, 'r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)


        params_raw = raw.get('validations')
        if not isinstance(params_raw, list):
            raise ValueError("El archivo YAML debe contener una lista de validaciones bajo la clave 'validations'.")
        
        validations = []
        for param in params_raw:
            validations.append(ParametricRule.from_dict(**param))
            

       
        return cls(
            validations=validations
        )
