import pytest
from flask import Flask
from unittest.mock import patch
from routes.api_routes import api_bp

# --- CONFIGURACIÓN DE LA APP DE PRUEBAS ---

@pytest.fixture
def app():
    """Crea una instancia de Flask para pruebas."""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Cliente de pruebas para realizar peticiones HTTP."""
    return app.test_client()

# --- TESTS ---

def test_home_route(client):
    """Verifica que la ruta raíz cargue el index."""
    with patch('routes.api_routes.render_template') as mock_render:
        mock_render.return_value = "Página de Inicio"
        response = client.get('/')
        assert response.status_code == 200
        assert "Página de Inicio" in response.get_data(as_text=True) 

def test_api_test_endpoint(client):
    """Verifica el endpoint de salud de la API."""
    response = client.get('/api/test')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "version" in data
    assert "servicios" in data

@patch('routes.api_routes.get_all_products')
def test_obtener_productos(mock_get_all, client):
    """Prueba la obtención de la lista completa de productos."""
    mock_get_all.return_value = [
        {"nombre": "Leche", "precio": 1.20, "historial_ventas": []}
    ]
    
    response = client.get('/api/productos')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["total"] == 1
    assert data["productos"][0]["nombre"] == "Leche"

@patch('routes.api_routes.get_product_info')
def test_obtener_producto_por_nombre(mock_info, client):
    """Prueba la búsqueda de un producto existente e inexistente."""
    # Caso: Producto encontrado
    mock_info.return_value = {"nombre": "Leche", "categoria": "Lácteos"}
    response = client.get('/api/producto/Leche')
    assert response.status_code == 200
    assert response.get_json()["producto"]["nombre"] == "Leche"
    
    # Caso: Producto no encontrado
    mock_info.return_value = None
    response = client.get('/api/producto/Inexistente')
    assert response.status_code == 404
    assert "no encontrado" in response.get_json()["message"]

@patch('routes.api_routes.detect_products')
@patch('routes.api_routes.get_all_products')
@patch('routes.api_routes.get_product_info')
@patch('routes.api_routes.get_sales_history')
@patch('routes.api_routes.predict_stock_outage')
@patch('routes.api_routes.calculate_inventory_metrics')
@patch('routes.api_routes.calculate_inventory_value')
def test_analizar_inventario_completo(
    mock_val, mock_met, mock_pred, mock_hist, mock_info, mock_all, mock_det, client
):
    """Prueba el flujo completo de análisis de inventario."""
    mock_det.return_value = {"productos": [{"nombre": "Leche", "cantidad": 5}]}
    mock_all.return_value = []
    mock_info.return_value = {"categoria": "Refrigerados", "precio": 1.20}
    mock_hist.return_value = [1, 2, 3]
    mock_pred.return_value = {"dias_hasta_agotarse": 5, "estado": "OK"}
    mock_met.return_value = {"resumen": {"productos_criticos": 0}}
    mock_val.return_value = 100.0

    response = client.get('/api/analizar-inventario')
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert len(data["productos"]) == 1
    assert data["valor_inventario"] == 100.0