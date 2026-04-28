import pytest
from services.inventory.metrics import calculate_inventory_metrics

def test_calculate_inventory_metrics_basico():
    """Verifica el resumen de métricas con datos controlados."""
    # Simulamos base de datos y productos detectados
    db_fake = {
        "Leche": {"stock_minimo": 5},
        "Pan": {"stock_minimo": 10}
    }
    detectados = [
        {"nombre": "Leche", "cantidad": 2}, # Bajo (2 < 5)
        {"nombre": "Pan", "cantidad": 15}    # Adecuado (15 > 10)
    ]
    
    resultado = calculate_inventory_metrics(detectados, db_fake)
    
    assert resultado["resumen"]["total_productos"] == 2
    assert resultado["resumen"]["productos_bajos"] == 1
    assert resultado["resumen"]["productos_adecuados"] == 1
    assert "recomendaciones" in resultado