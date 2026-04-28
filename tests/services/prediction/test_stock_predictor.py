import pytest
from services.prediction.stock_predictor import predict_stock_outage

def test_stock_agotado():
    """Prueba que si el stock es 0, el estado sea AGOTADO."""
    # Simulación: Ventas de 10 unidades, pero stock actual 0
    resultado = predict_stock_outage([10, 10], 0)
    
    assert resultado["estado"] == "AGOTADO"
    assert resultado["dias_hasta_agotarse"] == 0

def test_stock_critico():
    """Prueba que si el stock dura menos de 2 días, el estado sea CRÍTICO."""
    # Ventas: 10/día, Stock: 1 -> dura aproximadamente 0.1 días
    resultado = predict_stock_outage([10, 10], 1)
    
    assert "CRÍTICO" in resultado["estado"]
    assert resultado["dias_hasta_agotarse"] <= 2

def test_sin_historial_ventas():
    """Prueba el comportamiento cuando no hay historial de ventas."""
    resultado = predict_stock_outage([], 10)
    
    assert resultado["estado"] == "SIN HISTORIAL"
    assert resultado["dias_hasta_agotarse"] == 0

def test_stock_adecuado():
    """Prueba que un stock abundante devuelva el estado ADECUADO."""
    # Ventas: 1/día, Stock: 50 -> dura 50 días
    resultado = predict_stock_outage([1, 1, 1], 50)
    
    assert "ADEQUADO" in resultado["estado"]
    assert resultado["dias_hasta_agotarse"] > 10