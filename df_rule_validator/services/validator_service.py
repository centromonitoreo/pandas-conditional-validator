from .factory import ConditionValidatorFactory


class ValidationService:
    """Servicio principal que usa Factory para validación"""
    
    def __init__(self):
        self.factory = ConditionValidatorFactory()
    
    def validate(self, df, rules):
        results = {}
        for rule in rules:
            condition_type = rule['type']
            condition = self.factory.create_validator(condition_type)
            
            results[rule['name']] = condition.validate_condition(df, **rule['params'])
        return results
    
