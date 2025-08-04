from df_rule_validator.validator import validate_dataframe
from df_rule_validator.rules_schema import RulesConfig
import pandas as pd
# Cargar reglas
rules = RulesConfig.from_yaml("examples/rules_parametric.yaml")

df = pd.read_csv("examples/data_example.csv")

fails, cleaned_df = validate_dataframe(
    df,
    rules,
    action="drop_rows",
    log_file="validation_log.jsonl"
)

print("Filas eliminadas:", fails)
print("DataFrame limpio:", cleaned_df)
