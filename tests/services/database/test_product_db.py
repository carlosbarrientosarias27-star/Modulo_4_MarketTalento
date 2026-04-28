import pytest
from services.database.db_reader import get_product_info, get_all_products
from services.database.db_filter import get_sales_history

def test_get_product_info_existente():
    """Verifica que se obtenga la información correcta de un producto real."""
    producto = get_product_info("Leche Entera")
    assert producto is not None
    assert producto["id"] == "PROD001"
    assert producto["precio"] == 1.20

def test_get_product_info_no_existente():
    """Verifica que devuelva None si el producto no existe."""
    producto = get_product_info("Producto Fantasma")
    assert producto is None

def test_get_all_products():
    """Verifica que la lista de productos no esté vacía."""
    productos = get_all_products()
    assert len(productos) > 0
    # Comprobar que los elementos son diccionarios con nombre
    assert "nombre" in productos[0]

def test_get_sales_history_formato():
    """Verifica que el historial de ventas sea una lista de números."""
    historial = get_sales_history("Yogur Natural", days=5)
    assert isinstance(historial, list)
    assert all(isinstance(x, (int, float)) for x in historial)