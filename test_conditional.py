#!/usr/bin/env python3
"""
Script de prueba para verificar que CondicionalCondition funciona correctamente.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_condicional_condition():
    """Prueba básica de la clase CondicionalCondition."""
    # Importar solo lo necesario para evitar dependencias
    from df_rule_validator.rules_schema.conditions.condition import CondicionalCondition
    from df_rule_validator.rules_schema.conditions.comparison import ComparisonCondition
    
    # Crear datos de prueba
    test_data = {
        "type": "conditional",
        "if_": {
            "type": "greater_than",
            "column": "age",
            "value": 18
        },
        "then": {
            "type": "less_than",
            "column": "score",
            "value": 100
        }
    }
    
    try:
        # Crear instancia desde dictionary
        condition = CondicionalCondition.from_dict(test_data)
        print("✓ CondicionalCondition.from_dict() funciona correctamente")
        
        # Convertir de vuelta a dictionary
        result_dict = condition.to_dict()
        print("✓ CondicionalCondition.to_dict() funciona correctamente")
        
        # Verificar que los campos están presentes
        assert result_dict["type"] == "conditional"
        assert "if_" in result_dict
        assert "then" in result_dict
        print("✓ Los campos obligatorios están presentes")
        
        print("\n🎉 ¡CondicionalCondition implementada correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al probar CondicionalCondition: {e}")
        return False

if __name__ == "__main__":
    test_condicional_condition()
