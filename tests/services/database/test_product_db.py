import pytest
from services.database.product_db import product_database

# Fixture para acceder a los productos de forma limpia
@pytest.fixture
def db():
    return product_database

# 1. Pruebas de Integridad de la Base de Datos
def test_db_not_empty(db):
    """Verifica que la base de datos contenga productos."""
    assert len(db) > 0

def test_product_ids_are_unique(db):
    """Verifica que no haya IDs duplicados entre los productos."""
    ids = [info["id"] for info in db.values()]
    assert len(ids) == len(set(ids))

# 2. Pruebas de Estructura de Producto
@pytest.mark.parametrize("product_name", product_database.keys())
def test_product_structure(db, product_name):
    """Verifica que cada producto tenga todos los campos requeridos y tipos correctos."""
    product = db[product_name]
    required_keys = [
        "id", "nombre", "categoria", "precio", "unidad", 
        "stock_minimo", "stock_maximo", "tiempo_reposicion", "historial_ventas"
    ]
    
    for key in required_keys:
        assert key in product, f"Falta la clave '{key}' en el producto {product_name}"

    assert isinstance(product["precio"], (int, float))
    assert isinstance(product["historial_ventas"], list)
    assert len(product["historial_ventas"]) == 20  # Según el archivo, todos tienen 20 entradas

# 3. Pruebas de Lógica de Negocio
def test_stock_ranges(db):
    """Verifica que el stock mínimo sea siempre menor que el máximo."""
    for name, info in db.items():
        assert info["stock_minimo"] < info["stock_maximo"], \
            f"Error de stock en {name}: el mínimo debe ser menor al máximo."

def test_positive_prices(db):
    """Verifica que no haya productos con precio negativo o cero."""
    for name, info in db.items():
        assert info["precio"] > 0, f"El producto {name} tiene un precio inválido."

# 4. Pruebas de Categorías Específicas
def test_refrigerados_category(db):
    """Valida que los productos en 'Refrigerados' tengan tiempos de reposición cortos."""
    refrigerados = [p for p in db.values() if p["categoria"] == "Refrigerados"]
    for prod in refrigerados:
        # Los refrigerados suelen tener reposición rápida (< 5 días)
        assert prod["tiempo_reposicion"] <= 4

# 5. Prueba de Historial de Ventas
def test_sales_history_is_numeric(db):
    """Verifica que todos los datos del historial de ventas sean números enteros."""
    for name, info in db.items():
        assert all(isinstance(venta, int) for venta in info["historial_ventas"]), \
            f"El historial de ventas de {name} contiene valores no enteros."

# 6. Ejemplo de búsqueda de un producto específico
def test_specific_product_data(db):
    """Verifica los datos exactos de un producto conocido (Leche Entera)."""
    leche = db.get("Leche Entera")
    assert leche is not None
    assert leche["id"] == "PROD001"
    assert leche["precio"] == 1.20