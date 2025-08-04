import pandas as pd
import json
from datetime import datetime
from .logger import ValidationLogger
import operator
from .rules_schema import RulesConfig

OPS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne
}


def eval_condition(df, cond):
    """Evalúa una condición o conjunto de condiciones AND/OR sobre un DataFrame y devuelve un mask booleano."""
    if "operator" in cond and "conditions" in cond:
        # Lógica compuesta
        sub_masks = [eval_condition(df, c) for c in cond["conditions"]]
        if cond["operator"].upper() == "AND":
            mask = sub_masks[0]
            for m in sub_masks[1:]:
                mask &= m
            return mask
        elif cond["operator"].upper() == "OR":
            mask = sub_masks[0]
            for m in sub_masks[1:]:
                mask |= m
            return mask
        else:
            raise ValueError(f"Operador no soportado: {cond['operator']}")
    else:
        # Condición simple
        if cond["type"] == "greater_than":
            return df[cond["col"]] > cond["value"]
        elif cond["type"] == "less_than":
            return df[cond["col"]] < cond["value"]
        elif cond["type"] == "between":
            return (df[cond["col"]] >= cond["min"]) & (df[cond["col"]] <= cond["max"])
        elif cond["type"] == "expression":
            expr_values = df.eval(cond["expr"])
            return OPS[cond["operator"]](expr_values, cond["value"])
        else:
            raise ValueError(f"Tipo de condición no soportada: {cond['type']}")

def validate_dataframe(df: pd.DataFrame, rules: RulesConfig, action="log_only", log_file=None, param_col=None):
    logger = ValidationLogger(log_file)
    fails_list = []

    if param_col is None:
        raise ValueError("Debe especificarse 'param_col' con el nombre de la columna de parámetros")

    # Validar por parámetro
    if rules.parametros:
        for param, rule in rules.parametros.items():
            subset = df[df[param_col] == param]
            mask_if, mask_then = None, None

            if rule["condition"]["type"] == "conditional":
                mask_if = eval_condition(subset, rule["condition"]["if"])
                mask_then = eval_condition(subset, rule["condition"]["then"])
                fails = subset[mask_if & ~mask_then]
            else:
                mask = eval_condition(subset, rule["condition"])
                fails = subset[~mask]

            for _, row in fails.iterrows():
                logger.log_failure(param, row.to_dict(), rule, param_col)
                fails_list.append(row.name)

    if rules._global:
        for rule in rules._global:
            mask = eval_condition(df, rule)
            fails = df[~mask]
            for _, row in fails.iterrows():
                logger.log_failure(row.get(param_col), row.to_dict(), rule, param_col)
                fails_list.append(row.name)

    if action == "drop_rows":
        df = df.drop(fails_list)
    elif action == "mask_values":
        df.loc[fails_list, :] = None

    logger.save()
    return fails_list, df


