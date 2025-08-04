import pandas as pd
from .base import ValidatedCondition

class ConditionalCondition(ValidatedCondition):

    def validate_condition(self, df, if_: dict, then: dict) -> pd.Series:
        
        """Valida una condición condicional en el DataFrame."""
        self.validate_input(df)
        self._validate_condition(if_)
        self._validate_condition(then)

        from ..services.factory import ConditionValidatorFactory

        validator_composite = ConditionValidatorFactory.create_validator("composite")
        result = validator_composite.validate_condition(df, conditions = [if_, then], operator="AND")

        return result


    def _validate_condition(self, if_: dict) -> None:
        if not isinstance(if_, dict):
            raise ValueError("La condición 'if' debe ser un diccionario")
        if not 'type' in if_:
            raise ValueError("La condición 'if' debe contener una clave 'type'")