import pytest
import sqlite3
import json
from unittest.mock import patch 
from services.database.db_reader import get_all_products, get_product_info

# --- FIXTURES ---

@pytest.fixture
def mock_db(tmp_path):
    """
    Crea una base de datos SQLite temporal con datos de prueba.
    """
    db_file = tmp_path / "test_inventario.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Crear tabla basada en la estructura implícita de db_reader.py
    cursor.execute('''
        CREATE TABLE productos (
            id TEXT,
            nombre TEXT,
            categoria TEXT,
            precio REAL,
            unidad TEXT,
            stock_minimo INTEGER,
            stock_maximo INTEGER,
            tiempo_reposicion INTEGER,
            historial_ventas TEXT
        )
    ''')
    
    # Insertar datos de prueba
    productos_demo = [
        ("PROD001", "Leche Entera", "Refrigerados", 1.20, "litro", 5, 30, 2, json.dumps([3, 4, 5])),
        ("PROD002", "Yogur Natural", "Refrigerados", 0.55, "unidad", 8, 60, 2, json.dumps([10, 12]))
    ]
    
    cursor.executemany("INSERT INTO productos VALUES (?,?,?,?,?,?,?,?,?)", productos_demo)
    conn.commit()
    conn.close()
    
    # Usamos patch para que db_reader.DB_PATH apunte a nuestro archivo temporal
    with patch("services.database.db_reader.DB_PATH", str(db_file)): 
        yield str(db_file)

# --- TESTS ---

def test_get_all_products(mock_db):
    """Verifica que se recuperen todos los productos y el JSON se convierta a lista."""
    productos = get_all_products()
    
    assert len(productos) == 2
    assert productos[0]["nombre"] == "Leche Entera"
    # Verifica la conversión de JSON a lista
    assert isinstance(productos[0]["historial_ventas"], list)
    assert productos[0]["historial_ventas"] == [3, 4, 5]

def test_get_product_info_success(mock_db):
    """Verifica la recuperación de un producto específico por nombre."""
    producto = get_product_info("Yogur Natural")
    
    assert producto is not None
    assert producto["id"] == "PROD002"
    assert producto["precio"] == 0.55
    assert producto["historial_ventas"] == [10, 12]

def test_get_product_info_not_found(mock_db):
    """Verifica que devuelva None si el producto no existe."""
    producto = get_product_info("Producto Inexistente")
    assert producto is None

def test_get_all_products_malformed_json(tmp_path):
    """Verifica que el error de JSON mal formado se maneje devolviendo una lista vacía."""
    db_file = tmp_path / "bad_json.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE productos (nombre TEXT, historial_ventas TEXT)")
    # Insertamos un JSON inválido (faltan corchetes o comillas)
    cursor.execute("INSERT INTO productos VALUES (?, ?)", ("Error Prod", "esto-no-es-json"))
    conn.commit()
    conn.close()

    with patch("services.database.db_reader.DB_PATH", str(db_file)):
        productos = get_all_products()
        # El código corregido ahora cierra el assert correctamente
        assert productos[0]["historial_ventas"] == []