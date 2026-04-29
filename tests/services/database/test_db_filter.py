import pytest
import sqlite3
import json
from unittest.mock import patch
from services.database.db_filter import get_sales_history

# --- FIXTURES ---

@pytest.fixture
def mock_db_filter(tmp_path):
    """
    Crea una base de datos SQLite temporal para probar el filtrado.
    """
    db_file = tmp_path / "test_filter.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Creamos la tabla necesaria para la función
    cursor.execute('''
        CREATE TABLE productos (
            nombre TEXT,
            historial_ventas TEXT
        )
    ''')
    
    # Insertamos datos de prueba con JSON serializado
    datos = [
        ("Leche Entera", json.dumps([3, 4, 5, 2])),
        ("Yogur Natural", json.dumps([10, 15, 20]))
    ]
    
    cursor.executemany("INSERT INTO productos VALUES (?, ?)", datos)
    conn.commit()
    conn.close()
    
    # Parcheamos DB_PATH en el módulo db_filter
    with patch("services.database.db_filter.DB_PATH", str(db_file)):
        yield str(db_file)

# --- TESTS ---

def test_get_sales_history_success(mock_db_filter):
    """Verifica que se obtenga el historial correcto y se convierta a lista."""
    historial = get_sales_history("Leche Entera")
    
    assert isinstance(historial, list)
    assert len(historial) == 4
    assert historial == [3, 4, 5, 2]

def test_get_sales_history_empty_product(mock_db_filter):
    """Verifica que devuelva una lista vacía si el producto no existe."""
    historial = get_sales_history("Producto Inexistente")
    
    assert historial == []

def test_get_sales_history_structure(mock_db_filter):
    """Verifica que los datos recuperados sean del tipo esperado."""
    historial = get_sales_history("Yogur Natural")
    
    assert all(isinstance(v, int) for v in historial)
    assert historial[0] == 10