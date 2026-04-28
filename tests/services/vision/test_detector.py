import pytest
from services.vision.detector import detect_products

def test_detect_products_formato():
    """Verifica que la detección devuelva un diccionario con productos."""
    resultado = detect_products()
    assert isinstance(resultado, dict)
    assert "productos" in resultado
    assert len(resultado["productos"]) >= 0

def test_detect_products_contiene_datos():
    """Verifica que los productos detectados tengan nombre y cantidad."""
    resultado = detect_products()
    if resultado["productos"]:
        producto = resultado["productos"][0]
        assert "nombre" in producto
        assert "cantidad" in producto