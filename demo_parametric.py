#!/usr/bin/env python3
"""
Demostración del sistema de reglas parametrizadas
"""

from df_rule_validator.rules_schema import RulesConfig
import pandas as pd

def demo_parametric_rules():
    """Demostrar el uso de reglas parametrizadas."""
    print("🚀 Demostrando reglas parametrizadas\n")
    
    # Cargar reglas parametrizadas
    print("📋 Cargando reglas parametrizadas...")
    rules = RulesConfig.from_yaml("examples/rules_parametric.yaml")
    print(f"✅ Cargadas {len(rules.parametros)} reglas paramétricas")
    print(f"✅ Cargadas {len(rules.global_rules)} reglas globales")
    
    # Escenario 1: Análisis de suelos agrícolas
    print("\n🌱 Escenario 1: Análisis de suelos agrícolas")
    agricultural_params = {
        'nitrogen_column': 'nitrógeno_ppm',
        'nitrogen_threshold': 15.0,
        'phosphorus_column': 'fósforo_ppm', 
        'phosphorus_low': 5.0,
        'phosphorus_mid_min': 8.0,
        'phosphorus_mid_max': 12.0,
        'target_column': 'ph_suelo',
        'target_threshold': 7.5,
        'temperature_column': 'temp_ambiente',
        'temp_min': 18.0,
        'temp_max': 28.0,
        'quality_column': 'calidad_general',
        'quality_threshold': 0.8,
        'count_column': 'num_muestras'
    }
    
    # Resolver reglas para este escenario
    resolved_config = rules.get_resolved_config(agricultural_params)
    
    print("  📝 Regla resuelta para 'Relacion_NP':")
    np_rule = resolved_config.parametros['Relacion_NP']
    print(f"     Condición: {np_rule.condition}")
    
    print("  📝 Regla resuelta para 'Temperatura_Rango':")
    temp_rule = resolved_config.parametros['Temperatura_Rango']
    print(f"     Condición: {temp_rule.condition}")
    
    # Escenario 2: Análisis de agua
    print("\n💧 Escenario 2: Análisis de calidad del agua")
    water_params = {
        'nitrogen_column': 'nitrato_mg_l',
        'nitrogen_threshold': 50.0,
        'phosphorus_column': 'fosfato_mg_l',
        'phosphorus_low': 0.1,
        'phosphorus_mid_min': 0.5,
        'phosphorus_mid_max': 1.0,
        'target_column': 'turbidez_ntu',
        'target_threshold': 4.0,
        'temperature_column': 'temperatura_celsius',
        'temp_min': 4.0,
        'temp_max': 30.0,
        'quality_column': 'indice_calidad',
        'quality_threshold': 0.7,
        'count_column': 'num_analisis'
    }
    
    # Resolver reglas para el segundo escenario
    water_config = rules.get_resolved_config(water_params)
    
    print("  📝 Regla resuelta para 'Relacion_NP' (agua):")
    np_water_rule = water_config.parametros['Relacion_NP']
    print(f"     Condición: {np_water_rule.condition}")
    
    # Escenario 3: Resolver solo una regla específica
    print("\n🎯 Escenario 3: Resolver regla específica")
    specific_params = {
        'temperature_column': 'temp_reactor',
        'temp_min': 60.0,
        'temp_max': 80.0
    }
    
    specific_rule = rules.resolve_rule_parameters('Temperatura_Rango', specific_params)
    if specific_rule:
        print("  📝 Regla 'Temperatura_Rango' para reactor:")
        print(f"     Condición: {specific_rule.condition}")
    
    # Mostrar reglas globales resueltas
    print("\n🌍 Reglas globales resueltas:")
    global_resolved = resolved_config.global_rules
    for i, rule in enumerate(global_resolved, 1):
        print(f"  {i}. {rule}")

def demo_flexible_columns():
    """Demostrar flexibilidad de columnas."""
    print("\n🔄 Demostrando flexibilidad de columnas...")
    
    # Crear un DataFrame de ejemplo para agricultura
    agri_data = pd.DataFrame({
        'nitrógeno_ppm': [10, 20, 15, 8],
        'fósforo_ppm': [4, 7, 10, 2],
        'ph_suelo': [6.5, 8.0, 7.2, 6.8],
        'temp_ambiente': [22, 25, 30, 19],
        'calidad_general': [0.9, 0.6, 0.8, 0.95],
        'num_muestras': [5, 3, 4, 6]
    })
    
    # Crear un DataFrame de ejemplo para agua
    water_data = pd.DataFrame({
        'nitrato_mg_l': [45, 55, 30, 60],
        'fosfato_mg_l': [0.3, 1.2, 0.8, 0.05],
        'turbidez_ntu': [2.1, 5.2, 3.8, 1.9],
        'temperatura_celsius': [18, 25, 22, 15],
        'indice_calidad': [0.85, 0.65, 0.75, 0.9],
        'num_analisis': [2, 4, 3, 5]
    })
    
    print(f"📊 DataFrame agrícola:")
    print(agri_data.head())
    print(f"\n📊 DataFrame de agua:")
    print(water_data.head())
    
    print("\n✅ Mismas reglas, diferentes columnas - ¡máxima flexibilidad!")

if __name__ == "__main__":
    try:
        demo_parametric_rules()
        demo_flexible_columns()
        print("\n🎉 Demo completada exitosamente!")
    except Exception as e:
        print(f"❌ Error en la demo: {e}")
        import traceback
        traceback.print_exc()
