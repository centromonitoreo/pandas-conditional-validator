#!/usr/bin/env python3
"""
Debug específico para reglas globales
"""

from df_rule_validator.rules_schema import RulesConfig
import yaml

def debug_global_rules():
    """Debug específico para reglas globales."""
    print("🔍 Debug de Reglas Globales\n")
    
    # Leer YAML crudo
    with open("examples/rules_complete.yaml", 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    
    print(f"Claves en YAML: {list(raw.keys())}")
    
    # Examinar reglas globales crudas
    globs = raw.get('_global')
    print(f"Reglas globales crudas: {type(globs)}")
    print(f"Cantidad: {len(globs) if globs else 0}")
    
    if globs:
        for i, rule in enumerate(globs):
            print(f"  Regla {i}: {rule}")
    
    # Cargar con RulesConfig
    print("\n--- Cargando con RulesConfig ---")
    rules = RulesConfig.from_yaml("examples/rules_complete.yaml")
    
    print(f"rules.global_rules type: {type(rules.global_rules)}")
    print(f"rules.global_rules is None: {rules.global_rules is None}")
    if rules.global_rules is not None:
        print(f"len(rules.global_rules): {len(rules.global_rules)}")
        for i, rule in enumerate(rules.global_rules):
            print(f"  Regla global {i}: {type(rule).__name__}")
    else:
        print("global_rules is None!")

if __name__ == "__main__":
    debug_global_rules()
