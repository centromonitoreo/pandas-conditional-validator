from typing import List, Union, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import yaml
import re

class ValidationMetadata(BaseModel):
    """Metadata para documentación y logging de validaciones."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[Literal["info", "warning", "error", "critical"]] = None
    business_rule: Optional[str] = None
    documentation_url: Optional[str] = None
    tags: Optional[List[str]] = None
    unit: Optional[str] = None
    expected_range: Optional[str] = None
    impact: Optional[str] = None
    action: Optional[str] = None
    formula: Optional[str] = None

class SimpleCondition(BaseModel):
    type: Literal["greater_than", "less_than", "between", "expression"]
    col: Optional[str] = None
    value: Optional[Union[float, str]] = None  # Ahora puede ser string para parámetros
    min: Optional[Union[float, str]] = None
    max: Optional[Union[float, str]] = None
    expr: Optional[str] = None
    operator: Optional[Literal[">", "<", ">=", "<=", "==", "!="]] = None
    metadata: Optional[ValidationMetadata] = None
    
    def resolve_parameters(self, parameters: Dict[str, Any]) -> "SimpleCondition":
        """Resuelve parámetros dinámicos en la condición."""
        resolved_data = self.model_dump()
        
        # Resolver columna
        if resolved_data['col'] and isinstance(resolved_data['col'], str):
            resolved_data['col'] = self._resolve_value(resolved_data['col'], parameters)
        
        # Resolver valor
        if resolved_data['value'] is not None:
            resolved_data['value'] = self._resolve_value(resolved_data['value'], parameters)
        
        # Resolver min/max para between
        if resolved_data['min'] is not None:
            resolved_data['min'] = self._resolve_value(resolved_data['min'], parameters)
        if resolved_data['max'] is not None:
            resolved_data['max'] = self._resolve_value(resolved_data['max'], parameters)
        
        # Resolver expresión
        if resolved_data['expr']:
            resolved_data['expr'] = self._resolve_value(resolved_data['expr'], parameters)
        
        return SimpleCondition(**resolved_data)
    
    def _resolve_value(self, value: Any, parameters: Dict[str, Any]) -> Any:
        """Resuelve un valor que puede contener parámetros."""
        if isinstance(value, str):
            # Buscar patrones como ${param_name} o {param_name}
            pattern = r'\$?\{([^}]+)\}'
            matches = re.findall(pattern, value)
            
            resolved = value
            for match in matches:
                if match in parameters:
                    # Reemplazar el patrón completo
                    pattern_to_replace = r'\$?\{' + re.escape(match) + r'\}'
                    resolved = re.sub(pattern_to_replace, str(parameters[match]), resolved)
            
            # Si el valor resultante es completamente numérico, convertir
            try:
                if resolved.replace('.', '').replace('-', '').isdigit():
                    return float(resolved) if '.' in resolved else int(resolved)
            except:
                pass
            
            return resolved
        
        return value

class CompositeCondition(BaseModel):
    operator: Literal["AND", "OR"]
    conditions: List[Union["SimpleCondition", "CompositeCondition"]]
    metadata: Optional[ValidationMetadata] = None

    @field_validator('conditions')
    def validate_conditions_not_empty(cls, v):
        if not v:
            raise ValueError("'conditions' no puede estar vacía")
        return v
    
    def resolve_parameters(self, parameters: Dict[str, Any]) -> "CompositeCondition":
        """Resuelve parámetros dinámicos en todas las subcondiciones."""
        resolved_conditions = []
        for condition in self.conditions:
            if hasattr(condition, 'resolve_parameters'):
                resolved_conditions.append(condition.resolve_parameters(parameters))
            else:
                resolved_conditions.append(condition)
        
        return CompositeCondition(
            operator=self.operator,
            conditions=resolved_conditions,
            metadata=self.metadata
        )

CompositeCondition.model_rebuild()

class ConditionalRule(BaseModel):
    type: Literal["conditional"]
    if_: Union[SimpleCondition, CompositeCondition] = Field(..., alias="if")
    then: Union[SimpleCondition, CompositeCondition]
    metadata: Optional[ValidationMetadata] = None
    
    def resolve_parameters(self, parameters: Dict[str, Any]) -> "ConditionalRule":
        """Resuelve parámetros dinámicos en las condiciones if y then."""
        resolved_if = self.if_.resolve_parameters(parameters) if hasattr(self.if_, 'resolve_parameters') else self.if_
        resolved_then = self.then.resolve_parameters(parameters) if hasattr(self.then, 'resolve_parameters') else self.then
        
        # Usar el alias correcto para el campo if_
        return ConditionalRule.model_validate({
            'type': self.type,
            'if': resolved_if,
            'then': resolved_then,
            'metadata': self.metadata
        })

# Alias para todo tipo de regla
RuleType = Union[SimpleCondition, CompositeCondition, ConditionalRule]

class ParametricRule(BaseModel):
    condition: RuleType
    metadata: Optional[ValidationMetadata] = None
    
    def resolve_parameters(self, parameters: Dict[str, Any]) -> "ParametricRule":
        """Resuelve parámetros dinámicos en la condición."""
        resolved_condition = self.condition.resolve_parameters(parameters) if hasattr(self.condition, 'resolve_parameters') else self.condition
        return ParametricRule(condition=resolved_condition, metadata=self.metadata)

class LoggingConfig(BaseModel):
    """Configuración para logging automático."""
    level: Optional[str] = "INFO"
    include_metadata: Optional[bool] = True
    log_format: Optional[str] = "json"
    fields_to_log: Optional[List[str]] = None

class DocumentationConfig(BaseModel):
    """Configuración para generación automática de documentación."""
    auto_generate: Optional[bool] = True
    output_format: Optional[List[str]] = ["markdown"]
    include_examples: Optional[bool] = True
    group_by_category: Optional[bool] = True
    include_business_rules: Optional[bool] = True

class ConfigMetadata(BaseModel):
    """Metadata del archivo de configuración completo."""
    version: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    last_modified: Optional[str] = None

class RulesConfig(BaseModel):
    # Metadata del archivo completo
    metadata: Optional[ConfigMetadata] = None
    
    # Reglas paramétricas
    parametros: Optional[Dict[str, ParametricRule]] = None
    
    # Reglas globales
    global_rules: Optional[List[RuleType]] = Field(None, alias="_global")
    
    # Configuraciones adicionales
    logging_config: Optional[LoggingConfig] = None
    documentation_config: Optional[DocumentationConfig] = None
    
    def resolve_rule_parameters(self, rule_name: str, parameters: Dict[str, Any]) -> Optional[ParametricRule]:
        """Resuelve parámetros para una regla específica."""
        if not self.parametros or rule_name not in self.parametros:
            return None
        
        return self.parametros[rule_name].resolve_parameters(parameters)
    
    def resolve_global_parameters(self, parameters: Dict[str, Any]) -> List[RuleType]:
        """Resuelve parámetros para todas las reglas globales."""
        if not self.global_rules:
            return []
            
        resolved_rules = []
        for rule in self.global_rules:
            if hasattr(rule, 'resolve_parameters'):
                resolved_rules.append(rule.resolve_parameters(parameters))
            else:
                resolved_rules.append(rule)
        return resolved_rules
    
    def get_all_rule_metadata(self) -> Dict[str, ValidationMetadata]:
        """Obtiene toda la metadata de las reglas para documentación."""
        metadata_dict = {}
        
        # Metadata de reglas paramétricas
        if self.parametros:
            for rule_name, rule in self.parametros.items():
                if rule.metadata:
                    metadata_dict[f"parametros.{rule_name}"] = rule.metadata
        
        # Metadata de reglas globales
        if self.global_rules:
            for i, rule in enumerate(self.global_rules):
                if hasattr(rule, 'metadata') and rule.metadata:
                    metadata_dict[f"global.{i}"] = rule.metadata
        
        return metadata_dict
    
    def get_rules_by_category(self, category: str) -> Dict[str, Any]:
        """Obtiene todas las reglas de una categoría específica."""
        rules_by_category = {}
        
        # Buscar en reglas paramétricas
        if self.parametros:
            for rule_name, rule in self.parametros.items():
                if rule.metadata and rule.metadata.category == category:
                    rules_by_category[f"parametros.{rule_name}"] = rule
        
        # Buscar en reglas globales
        if self.global_rules:
            for i, rule in enumerate(self.global_rules):
                if hasattr(rule, 'metadata') and rule.metadata and rule.metadata.category == category:
                    rules_by_category[f"global.{i}"] = rule
        
        return rules_by_category
    
    def get_rules_by_severity(self, severity: str) -> Dict[str, Any]:
        """Obtiene todas las reglas de una severidad específica."""
        rules_by_severity = {}
        
        # Buscar en reglas paramétricas
        if self.parametros:
            for rule_name, rule in self.parametros.items():
                if rule.metadata and rule.metadata.severity == severity:
                    rules_by_severity[f"parametros.{rule_name}"] = rule
        
        # Buscar en reglas globales
        if self.global_rules:
            for i, rule in enumerate(self.global_rules):
                if hasattr(rule, 'metadata') and rule.metadata and rule.metadata.severity == severity:
                    rules_by_severity[f"global.{i}"] = rule
        
        return rules_by_severity
    
    def get_resolved_config(self, parameters: Dict[str, Any]) -> "RulesConfig":
        """Crea una nueva configuración con todos los parámetros resueltos."""
        resolved_parametros = {}
        if self.parametros:
            for name, rule in self.parametros.items():
                resolved_parametros[name] = rule.resolve_parameters(parameters)
        
        resolved_global = self.resolve_global_parameters(parameters)
        
        return RulesConfig(
            metadata=self.metadata,
            parametros=resolved_parametros,
            global_rules=resolved_global,
            logging_config=self.logging_config,
            documentation_config=self.documentation_config
        )

    @staticmethod
    def _validate_condition(condition_data: Any) -> RuleType:
        """Convierte dicts recursivamente a instancias Pydantic."""
        if isinstance(condition_data, dict):
            tipo = condition_data.get('type')
            if tipo == 'conditional':
                if_data = RulesConfig._validate_condition(condition_data['if'])
                then_data = RulesConfig._validate_condition(condition_data['then'])
                # Extraer metadata si existe
                metadata = condition_data.get('metadata')
                metadata_obj = ValidationMetadata(**metadata) if metadata else None
                # Usar el alias correcto para el campo if_
                return ConditionalRule(
                    type='conditional', 
                    **{'if': if_data}, 
                    then=then_data,
                    metadata=metadata_obj
                )
            elif 'conditions' in condition_data and 'operator' in condition_data:
                subs = [
                    RulesConfig._validate_condition(c)
                    for c in condition_data['conditions']
                ]
                # Extraer metadata si existe
                metadata = condition_data.get('metadata')
                metadata_obj = ValidationMetadata(**metadata) if metadata else None
                return CompositeCondition(
                    operator=condition_data['operator'], 
                    conditions=subs,
                    metadata=metadata_obj
                )
            else:
                # Extraer metadata si existe
                metadata = condition_data.get('metadata')
                metadata_obj = ValidationMetadata(**metadata) if metadata else None
                return SimpleCondition(**{k: v for k, v in condition_data.items() if k != 'metadata'}, metadata=metadata_obj)
        # Si ya es instancia, devolverla
        return condition_data

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "RulesConfig":
        with open(yaml_path, 'r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)

        # Procesar metadata del archivo
        metadata = raw.get('metadata')
        metadata_obj = ConfigMetadata(**metadata) if metadata else None

        # Procesar parámetros
        params_raw = raw.get('parametros') or {}
        validated_params = {}

        # Nueva estructura flexible: permite una lista de reglas con nombre explícito
        if isinstance(params_raw, list):
            for item in params_raw:
                name = item.get('name') or item.get('parametro') or item.get('param')
                if not name:
                    raise ValueError("Cada regla paramétrica debe incluir 'name' o 'parametro'")

                rule_metadata = item.get('metadata')
                rule_metadata_obj = ValidationMetadata(**rule_metadata) if rule_metadata else None

                cond = item.get('condition')
                validated = RulesConfig._validate_condition(cond)
                validated_params[name] = ParametricRule(
                    condition=validated,
                    metadata=rule_metadata_obj
                )
        elif isinstance(params_raw, dict):
            for name, rule_dict in params_raw.items():
                # Extraer metadata de la regla paramétrica
                rule_metadata = rule_dict.get('metadata')
                rule_metadata_obj = ValidationMetadata(**rule_metadata) if rule_metadata else None

                # Procesar condición
                cond = rule_dict.get('condition')
                validated = RulesConfig._validate_condition(cond)
                validated_params[name] = ParametricRule(
                    condition=validated,
                    metadata=rule_metadata_obj
                )
        else:
            raise ValueError("'parametros' debe ser un objeto o una lista de reglas")

        # Procesar reglas globales
        globs = raw.get('_global') or []
        validated_globs = [RulesConfig._validate_condition(c) for c in globs]

        # Procesar configuraciones
        logging_config = raw.get('logging_config')
        logging_config_obj = LoggingConfig(**logging_config) if logging_config else None
        
        documentation_config = raw.get('documentation_config')
        documentation_config_obj = DocumentationConfig(**documentation_config) if documentation_config else None

        return cls(
            metadata=metadata_obj,
            parametros=validated_params if validated_params else None,
            global_rules=validated_globs,  # No convertir a None si está vacía
            logging_config=logging_config_obj,
            documentation_config=documentation_config_obj
        )
