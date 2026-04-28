import pytest
from services.database.db_reader import get_product_info, get_all_products

def test_get_product_info_existente():
    """Verifica que se obtenga la información de un producto que existe en la BD."""
    # "Leche Entera" es un producto válido en product_db.py
    producto = get_product_info("Leche Entera")
    assert producto is not None
    assert producto["nombre"] == "Leche Entera"
    assert "precio" in producto

def test_get_product_info_no_existente():
    """Verifica que devuelva None si el producto no está en la base de datos."""
    producto = get_product_info("Producto Inexistente")
    assert producto is None

def test_get_all_products_formato():
    """Verifica que devuelva una lista con todos los productos."""
    productos = get_all_products()
    assert isinstance(productos, list)
    assert len(productos) > 0
    assert "id" in productos[0]