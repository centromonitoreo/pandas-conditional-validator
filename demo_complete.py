#!/usr/bin/env python3
"""
Demostración del sistema de validación con metadata completa
"""

from df_rule_validator.rules_schema import RulesConfig
import json
from typing import Dict, Any

def demo_complete_rules():
    """Demostración completa del sistema con metadata."""
    print("🚀 Demostración del Sistema de Validación Completo\n")
    
    # Cargar el archivo YAML completo
    print("📁 Cargando configuración completa...")
    try:
        rules = RulesConfig.from_yaml("examples/rules_complete.yaml")
        print("✅ Configuración cargada exitosamente\n")
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return
    
    # Mostrar información general
    print("📋 INFORMACIÓN GENERAL:")
    if rules.metadata:
        print(f"  - Versión: {rules.metadata.version}")
        print(f"  - Descripción: {rules.metadata.description}")
        print(f"  - Autor: {rules.metadata.author}")
        print(f"  - Última modificación: {rules.metadata.last_modified}")
    
    print(f"  - Reglas paramétricas: {len(rules.parametros) if rules.parametros else 0}")
    print(f"  - Reglas globales: {len(rules.global_rules) if rules.global_rules else 0}")
    
    # Mostrar configuración de logging
    if rules.logging_config:
        print(f"  - Logging habilitado: {rules.logging_config.level}")
    
    # Mostrar configuración de documentación
    if rules.documentation_config:
        print(f"  - Documentación automática: {rules.documentation_config.auto_generate}")
    
    print("\n" + "="*60 + "\n")
    
    # Mostrar metadata de reglas paramétricas
    if rules.parametros:
        print("📝 REGLAS PARAMÉTRICAS:")
        for rule_name, rule in rules.parametros.items():
            print(f"\n🔸 {rule_name}")
            if rule.metadata:
                print(f"  📛 Nombre: {rule.metadata.name}")
                print(f"  📄 Descripción: {rule.metadata.description}")
                print(f"  🏷️  Categoría: {rule.metadata.category}")
                print(f"  ⚠️  Severidad: {rule.metadata.severity}")
                print(f"  📋 Regla de negocio: {rule.metadata.business_rule}")
                if rule.metadata.tags:
                    print(f"  🏪 Tags: {', '.join(rule.metadata.tags)}")
                if rule.metadata.documentation_url:
                    print(f"  🔗 Documentación: {rule.metadata.documentation_url}")
            print(f"  🔧 Tipo de condición: {type(rule.condition).__name__}")
    
    print("\n" + "="*60 + "\n")
    
    # Mostrar metadata de reglas globales
    if rules.global_rules:
        print("🌍 REGLAS GLOBALES:")
        for i, rule in enumerate(rules.global_rules):
            print(f"\n🔸 Regla Global #{i+1}")
            if hasattr(rule, 'metadata') and rule.metadata:
                print(f"  📛 Nombre: {rule.metadata.name}")
                print(f"  📄 Descripción: {rule.metadata.description}")
                print(f"  🏷️  Categoría: {rule.metadata.category}")
                print(f"  ⚠️  Severidad: {rule.metadata.severity}")
                if rule.metadata.tags:
                    print(f"  🏪 Tags: {', '.join(rule.metadata.tags)}")
            print(f"  🔧 Tipo: {type(rule).__name__}")
    
    print("\n" + "="*60 + "\n")
    
    # Demostrar agrupación por categorías
    print("📁 AGRUPACIÓN POR CATEGORÍAS:")
    all_metadata = rules.get_all_rule_metadata()
    categories = set()
    for metadata in all_metadata.values():
        if metadata.category:
            categories.add(metadata.category)
    
    for category in sorted(categories):
        category_rules = rules.get_rules_by_category(category)
        print(f"\n🏷️  {category.upper()}: {len(category_rules)} reglas")
        for rule_name in category_rules.keys():
            print(f"    - {rule_name}")
    
    print("\n" + "="*60 + "\n")
    
    # Demostrar agrupación por severidad
    print("⚠️  AGRUPACIÓN POR SEVERIDAD:")
    severities = ["critical", "error", "warning", "info"]
    for severity in severities:
        severity_rules = rules.get_rules_by_severity(severity)
        if severity_rules:
            print(f"\n🚨 {severity.upper()}: {len(severity_rules)} reglas")
            for rule_name in severity_rules.keys():
                print(f"    - {rule_name}")
    
    print("\n" + "="*60 + "\n")
    
    # Demostrar resolución de parámetros
    print("🔧 DEMOSTRACIÓN DE RESOLUCIÓN DE PARÁMETROS:")
    
    # Definir parámetros de ejemplo
    sample_parameters = {
        # Para Relacion_NP
        "nitrogen_column": "nitrogeno_total",
        "nitrogen_threshold": 5.0,
        "phosphorus_column": "fosforo_disponible", 
        "phosphorus_low": 3.0,
        "phosphorus_mid_min": 4.0,
        "phosphorus_mid_max": 6.0,
        "target_column": "indice_calidad",
        "target_threshold": 2.0,
        
        # Para Temperatura_Rango
        "temperature_column": "temperatura_ambiente",
        "temp_min": 18.0,
        "temp_max": 25.0,
        
        # Para pH_Optimo
        "ph_column": "ph_solucion",
        "ph_min": 6.5,
        "ph_max": 8.5,
        
        # Para Calidad_Integral
        "optimal_temp_min": 20.0,
        "optimal_temp_max": 24.0,
        "humidity_column": "humedad_relativa",
        "humidity_min": 45.0,
        "humidity_max": 65.0,
        "pressure_column": "presion_sistema",
        "pressure_threshold": 2.0,
        "flow_column": "flujo_liquido",
        "flow_min": 10.0,
        "quality_score_column": "puntuacion_calidad",
        "quality_min_score": 85.0,
        "defect_rate_column": "tasa_defectos",
        "max_defect_rate": 0.05,
        
        # Para Formula_Personalizada
        "efficiency_column": "eficiencia_proceso",
        "yield_column": "rendimiento_producto",
        "input_column": "materia_prima",
        "efficiency_threshold": 0.8,
        
        # Para reglas globales
        "record_id_column": "id_registro",
        "timestamp_column": "fecha_hora",
        "data_age_days": "dias_antiguedad",
        "max_data_age": 30,
        "confidence_score": "confianza_datos",
        "min_confidence": 0.7
    }
    
    print("\n📊 Parámetros de ejemplo:")
    for key, value in list(sample_parameters.items())[:5]:  # Mostrar solo algunos
        print(f"  - {key}: {value}")
    print("  - ... (y más)")
    
    # Resolver una regla específica
    print(f"\n🔍 Resolviendo regla 'Relacion_NP':")
    resolved_rule = rules.resolve_rule_parameters("Relacion_NP", sample_parameters)
    if resolved_rule:
        print("✅ Regla resuelta exitosamente")
        if resolved_rule.metadata:
            print(f"📛 Nombre: {resolved_rule.metadata.name}")
        print(f"🔧 Tipo: {type(resolved_rule.condition).__name__}")
        
        # Mostrar la estructura resuelta (simplificada)
        if hasattr(resolved_rule.condition, 'if_'):
            print("📋 Estructura:")
            print("  IF: Condiciones de entrada resueltas")
            print("  THEN: Condición de salida resuelta")
    
    print("\n🏁 Demostración completada exitosamente!")

def generate_metadata_report(rules: RulesConfig):
    """Genera un reporte de metadata en formato JSON."""
    print("\n📄 GENERANDO REPORTE DE METADATA...")
    
    report = {
        "config_metadata": rules.metadata.model_dump() if rules.metadata else None,
        "logging_config": rules.logging_config.model_dump() if rules.logging_config else None,
        "documentation_config": rules.documentation_config.model_dump() if rules.documentation_config else None,
        "rules_metadata": {}
    }
    
    # Agregar metadata de todas las reglas
    all_metadata = rules.get_all_rule_metadata()
    for rule_name, metadata in all_metadata.items():
        report["rules_metadata"][rule_name] = metadata.model_dump()
    
    # Guardar reporte
    with open("metadata_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ Reporte guardado en 'metadata_report.json'")

if __name__ == "__main__":
    demo_complete_rules()
