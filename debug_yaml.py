#!/usr/bin/env python3
"""
Script de depuración para verificar el comportamiento de la carga YAML
"""

from df_rule_validator.rules_schema import RulesConfig
import yaml

def debug_yaml_loading():
    """Depurar el proceso de carga del YAML"""
    print("🔍 Depurando carga de YAML...")
    
    # Leer el YAML crudo
    with open("examples/rules_example.yaml", 'r', encoding='utf-8') as file:
        raw_data = yaml.safe_load(file)
    
    print("\n📄 Datos crudos del YAML:")
    print(f"Claves principales: {list(raw_data.keys())}")
    print(f"Contenido completo: {raw_data}")
    
    # Crear instancia de RulesConfig
    print("\n🔧 Creando instancia RulesConfig...")
    try:
        rules = RulesConfig.from_yaml("examples/rules_example.yaml")
        print("✅ Carga exitosa")
        
        print(f"\n📊 Resultado:")
        print(f"  - parametros: {rules.parametros is not None}")
        print(f"  - global_rules: {rules.global_rules is not None}")
        
        if rules.parametros:
            print(f"  - Número de parámetros: {len(rules.parametros)}")
        
        if rules.global_rules:
            print(f"  - Número de reglas globales: {len(rules.global_rules)}")
        else:
            print("  - ⚠️ No se cargaron reglas globales")
            
        # Verificar el contenido del modelo
        print(f"\n🔍 Contenido del modelo:")
        print(f"Model dump: {rules.model_dump()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_yaml_loading()
