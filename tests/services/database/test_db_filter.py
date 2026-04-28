import pytest
from services.database.db_filter import get_sales_history, get_by_category

def test_get_sales_history_existente():
    """Verifica que se obtenga el historial de un producto existente."""
    # Probamos con 'Leche Entera' que está en product_db.py
    historial = get_sales_history("Leche Entera", days=5)
    assert isinstance(historial, list)
    assert len(historial) == 5

def test_get_sales_history_no_existente():
    """Verifica que devuelva una lista vacía si el producto no existe."""
    historial = get_sales_history("Producto Inexistente")
    assert historial == []

def test_get_by_category_valida():
    """Verifica el filtrado de productos por categoría."""
    productos = get_by_category("Refrigerados")
    assert len(productos) > 0
    # Todos los productos devueltos deben ser de la categoría solicitada
    assert all(p["categoria"] == "Refrigerados" for p in productos)

def test_get_by_category_vacia():
    """Verifica que devuelva lista vacía para categorías inexistentes."""
    productos = get_by_category("Electrónica")
    assert productos == []