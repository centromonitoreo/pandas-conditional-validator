from df_rule_validator.services import ValidationService
from df_rule_validator.rules_schema import RulesConfig
import pandas as pd

# Cargar reglas y datos de ejemplo
rules = RulesConfig.from_yaml("examples/rules.yml")
df = pd.read_csv("examples/demo_data.csv")

validation_service = ValidationService()
results = validation_service.validate(df, rules)

print(results)
