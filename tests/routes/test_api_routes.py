import sys
import os
import pytest
from flask import Flask
from routes.api_routes import api_bp



@pytest.fixture
def client():
    """Fixture que configura el cliente de pruebas de Flask."""
    app = Flask(__name__)
    # Es necesario registrar el Blueprint que quieres probar
    app.register_blueprint(api_bp)
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_api_test_endpoint(client):
    """Verifica que el endpoint /api/test responda correctamente."""
    response = client.get('/api/test')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "vision" in data["servicios"]

def test_analizar_inventario_flujo(client):
    """Verifica el flujo principal de análisis de inventario."""
    response = client.get('/api/analizar-inventario')
    data = response.get_json()
    
    assert response.status_code == 200
    assert "deteccion" in data
    assert "valor_inventario" in data
    assert isinstance(data["productos"], list)

def test_obtener_productos(client):
    """Verifica que la lista de productos no esté vacía."""
    response = client.get('/api/productos')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["total"] > 0
    assert isinstance(data["productos"], list)

def test_obtener_producto_existente(client):
    """Verifica la recuperación de un producto real (Leche Entera)."""
    response = client.get('/api/producto/Leche Entera')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["producto"]["nombre"] == "Leche Entera"

def test_obtener_producto_inexistente(client):
    """Verifica el manejo de error 404 para productos que no existen."""
    response = client.get('/api/producto/ProductoFantasma')
    data = response.get_json()
    
    assert response.status_code == 404
    assert "no encontrado" in data["message"]

def test_obtener_recomendaciones(client):
    """Verifica que se generen recomendaciones iniciales."""
    response = client.get('/api/recomendaciones')
    data = response.get_json()
    
    assert response.status_code == 200
    assert "recomendaciones" in data
    assert len(data["recomendaciones"]) <= 5