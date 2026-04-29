import pytest
from services.inventory.valuation import calculate_inventory_value

def test_calculate_inventory_value_basico():
    """Verifica el cálculo del valor total del inventario."""
    # Datos de prueba controlados
    db_fake = [
    {"nombre": "Leche Entera", "precio": 1.50},
    {"nombre": "Pan de Molde", "precio": 0.80}
    ]
    
    detectados = [
        {"nombre": "Leche Entera", "cantidad": 10}, # 10 * 1.50 = 15.00
        {"nombre": "Pan de Molde", "cantidad": 5}      # 5 * 0.80 = 4.00
    ]
    # Total esperado: 19.00
    assert calculate_inventory_value(detectados, db_fake) == 19.00

def test_calculate_inventory_value_vacio():
    """Verifica que el valor sea 0 si no hay productos."""
    assert calculate_inventory_value([], {}) == 0

def test_calculate_inventory_value_producto_desconocido():
    """Verifica que ignore productos que no están en la base de datos."""
    db_fake = [
    {"nombre": "Leche Entera", "precio": 1.50},
    {"nombre": "Pan de Molde", "precio": 0.80}
]
    detectados = [{"nombre": "Inexistente", "cantidad": 100}]
    assert calculate_inventory_value(detectados, db_fake) == 0