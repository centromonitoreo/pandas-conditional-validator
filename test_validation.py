#!/usr/bin/env python3
"""
Script para probar la validación completa de la estructura Pydantic
"""

from df_rule_validator.rules_schema import RulesConfig
import pandas as pd
from pydantic import ValidationError

def test_yaml_validation():
    """Probar la validación del archivo YAML de ejemplo"""
    print("🔍 Probando validación del archivo YAML...")
    
    try:
        # Cargar y validar el archivo YAML
        rules = RulesConfig.from_yaml("examples/rules_example.yaml")
        print("✅ Validación exitosa!")
        
        # Mostrar la estructura validada
        print("\n📋 Estructura validada:")
        print(f"Parámetros: {list(rules.parametros.keys()) if rules.parametros else 'None'}")
        print(f"Reglas globales: {len(rules.global_rules) if rules.global_rules else 0}")
        
        # Verificar estructura de parámetros
        if rules.parametros:
            for param_name, param_rule in rules.parametros.items():
                print(f"\n📝 Parámetro '{param_name}':")
                print(f"  - Tipo de condición: {type(param_rule.condition).__name__}")
                print(f"  - Condición: {param_rule.condition}")
        
        # Verificar reglas globales
        if rules.global_rules:
            print(f"\n🌍 Reglas globales ({len(rules.global_rules)}):")
            for i, rule in enumerate(rules.global_rules):
                print(f"  {i+1}. Tipo: {type(rule).__name__}")
                print(f"     Contenido: {rule}")
        
        return rules
        
    except ValidationError as e:
        print("❌ Error de validación:")
        for error in e.errors():
            print(f"  - Campo: {error['loc']}")
            print(f"    Error: {error['msg']}")
            print(f"    Valor: {error['input']}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def test_invalid_yaml():
    """Probar con un YAML inválido para verificar que la validación detecte errores"""
    print("\n🧪 Probando con YAML inválido...")
    
    # Crear un archivo YAML con errores
    invalid_yaml_content = """
parametros:
  ReglaInvalida:
    condition:
      type: greater_than
      # Falta 'col' y 'value' requeridos
_global:
  - type: between
    col: temperatura
    # Faltan 'min' y 'max' requeridos
"""
    
    # Guardar archivo temporal
    with open("test_invalid.yaml", "w", encoding="utf-8") as f:
        f.write(invalid_yaml_content)
    
    try:
        rules = RulesConfig.from_yaml("test_invalid.yaml")
        print("⚠️  ADVERTENCIA: Se esperaba un error de validación pero no ocurrió")
    except ValidationError as e:
        print("✅ Validación detectó errores correctamente:")
        for error in e.errors():
            print(f"  - Campo: {'.'.join(map(str, error['loc']))}")
            print(f"    Error: {error['msg']}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    # Limpiar archivo temporal
    import os
    if os.path.exists("test_invalid.yaml"):
        os.remove("test_invalid.yaml")

def test_nested_structure():
    """Probar acceso a estructura anidada"""
    print("\n🔗 Probando acceso a estructura anidada...")
    
    rules = RulesConfig.from_yaml("examples/rules_example.yaml")
    if rules:
        # Acceder a regla paramétrica
        if rules.parametros and "Relacion_NP" in rules.parametros:
            relacion_np = rules.parametros["Relacion_NP"]
            condition = relacion_np.condition
            print(f"✅ Acceso a regla paramétrica: {type(condition).__name__}")
            
            # Si es una regla condicional, acceder a sus partes
            if hasattr(condition, 'if_') and hasattr(condition, 'then'):
                print(f"  - Condición 'if': {type(condition.if_).__name__}")
                print(f"  - Condición 'then': {type(condition.then).__name__}")
                
                # Acceder a condiciones anidadas
                if hasattr(condition.if_, 'conditions'):
                    print(f"  - Número de condiciones en 'if': {len(condition.if_.conditions)}")
                    for i, subcond in enumerate(condition.if_.conditions):
                        print(f"    {i+1}. {type(subcond).__name__}: {subcond}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de validación Pydantic\n")
    
    # Prueba 1: Validación del YAML válido
    rules = test_yaml_validation()
    
    # Prueba 2: Validación con YAML inválido
    test_invalid_yaml()
    
    # Prueba 3: Acceso a estructura anidada
    if rules:
        test_nested_structure()
    
    print("\n🏁 Pruebas completadas")
