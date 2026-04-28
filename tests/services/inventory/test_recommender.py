import pytest
from services.inventory.recommender import generate_recommendations

def test_recomendacion_urgente():
    """Verifica prioridad ALTA para stock agotado."""
    productos = [{"producto": "Leche", "stock_actual": 0, "stock_minimo": 5}]
    resultado = generate_recommendations(productos)
    assert resultado[0]["prioridad"] == "ALTA"
    assert "urgentemente" in resultado[0]["recomendacion"]

def test_recomendacion_media():
    """Verifica prioridad MEDIA para stock bajo."""
    productos = [{"producto": "Pan", "stock_actual": 2, "stock_minimo": 10}]
    resultado = generate_recommendations(productos)
    assert resultado[0]["prioridad"] == "MEDIA"