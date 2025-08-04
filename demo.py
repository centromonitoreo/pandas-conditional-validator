from df_rule_validator.services import ValidationService
from df_rule_validator.rules_schema import RulesConfig
import pandas as pd
# Cargar reglas
rules = RulesConfig.from_yaml("examples/rules_parametric.yaml")

df = pd.read_csv("examples/data_example.csv")

varsalidation_service = ValidationService()
failed_rows, result_df = varsalidation_service.validate(
    df,
    rules)