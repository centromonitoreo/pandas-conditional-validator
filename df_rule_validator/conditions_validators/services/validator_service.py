from .factory import ConditionValidatorFactory
from ...rules_schema import RulesConfig  

class ValidationService:
    """Servicio principal que usa Factory para validación"""
    
    def __init__(self):
        self.factory = ConditionValidatorFactory()
    
    def validate(self, df, rules: RulesConfig):
        results = {}
        for rule in rules.validations:
            contion_name = rule.name
            condition = rule.condition
            condition_type = condition.type
            condition_params = condition.to_dict()
            condition_params.pop('type', None)  # Eliminar 'type' del dict

            condition_validator = self.factory.create_validator(condition_type)
            
            results[contion_name] = condition_validator.validate_condition(df, **condition_params)
        return results
    
