# interface/demoStreamlit.py

import sys
import os


# Añade la carpeta raíz del proyecto al PATH de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, jsonify, render_template_string
from datetime import datetime, timedelta
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics
from services.inventory.valuation import calculate_inventory_value
from services.database.db_reader import get_product_info, get_all_products
from services.database.db_filter import get_sales_history
from services.prediction.stock_predictor import predict_stock_outage 
from services.database.product_db import product_database 

app = Flask(__name__) 

# ============================================================
# TEMPLATES HTML (embebidos como cadenas)
# ============================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario Inteligente</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .card { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; border: none; }
        .card-header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 15px 15px 0 0 !important; }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
        .stat-card { text-align: center; padding: 20px; border-radius: 10px; color: white; }
        .loading { display: none; text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="text-center mb-4">
            <h1 class="text-white">📦 Sistema de Inventario Inteligente</h1>
            <p class="text-white-50">Análisis con Visión Artificial y Predicción de Demanda</p>
        </div>
        <div class="row">
            <div class="col-md-3 mb-4">
                <div class="card">
                    <div class="card-header"><h5 class="mb-0">📊 Panel de Control</h5></div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" onclick="location.href='/'">🏠 Inicio</button>
                            <button class="btn btn-success" onclick="analizarInventario()">🔍 Analizar Inventario</button>
                            <button class="btn btn-info" onclick="verProductos()">📦 Ver Productos</button>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">🔌 Endpoints de la API</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary btn-api" onclick="callAPI('/api/test')">
                                <i class="fas fa-vial"></i> GET /api/test
                            </button>
                            <button class="btn btn-success btn-api" onclick="callAPI('/api/analizar-inventario')">
                                <i class="fas fa-chart-line"></i> GET /api/analizar-inventario
                            </button>
                            <button class="btn btn-info btn-api" onclick="callAPI('/api/productos')">
                                <i class="fas fa-boxes"></i> GET /api/productos
                            </button>
                            <button class="btn btn-warning btn-api" onclick="callAPI('/api/producto/Leche')">
                                <i class="fas fa-box"></i> GET /api/producto/Leche
                            </button>
                            <button class="btn btn-secondary btn-api" onclick="callAPI('/api/recomendaciones')">
                                <i class="fas fa-lightbulb"></i> GET /api/recomendaciones
                            </button>
                        </div>
                        <hr>
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary" onclick="location.href='/'">
                                <i class="fas fa-home"></i> Inicio
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <div class="card">
                    <div class="card-header"><h5 class="mb-0">Panel Principal</h5></div>
                    <div class="card-body">
                        <div id="loading" class="loading"><div class="spinner-border text-primary"></div><p>Procesando...</p></div>
                        <div id="content">
                            <div class="text-center">
                                <i class="fas fa-robot" style="font-size: 4em; color: #667eea;"></i>
                                <h3>Bienvenido</h3>
                                <p>Haz clic en "Analizar Inventario" para comenzar</p>
                            </div>
                        </div>
                    </div>
                </div>
            <!-- Panel derecho: Resultados -->
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">📊 Respuesta de la API</h5>
                    </div>
                    <div class="card-body">
                        <div id="loading" class="loading">
                            <div class="spinner-border text-primary"></div>
                            <p class="mt-2">Consultando API...</p>
                        </div>
                        <div id="response" class="response-area">
                            <i class="fas fa-info-circle"></i> Haz clic en cualquier botón para probar un endpoint
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
    <script>
        function callAPI(url) {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('response').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('response').innerHTML = 
                        '<div class="mb-2"><strong>📡 Endpoint:</strong> ' + url + '</div>' +
                        '<div class="mb-2"><strong>✅ Status:</strong> ' + (data.status || 'success') + '</div>' +
                        '<hr>' +
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('response').innerHTML = 
                        '<div class="alert alert-danger">❌ Error: ' + error + '</div>';
                });
        }
        function analizarInventario() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('content').innerHTML = '<p class="text-center">🔍 Analizando inventario...</p>';
            fetch('/api/analizar-inventario')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    let html = '<div class="alert alert-success">✅ Análisis completado</div>';
                    if (data.resumen) {
                        html += '<div class="row mb-4">' +
                            '<div class="col-md-4"><div class="stat-card bg-primary"><i class="fas fa-boxes"></i><h3>' + data.resumen.total_productos + '</h3><p>Productos Analizados</p></div></div>' +
                            '<div class="col-md-4"><div class="stat-card bg-danger"><i class="fas fa-exclamation-triangle"></i><h3>' + (data.resumen.productos_criticos || 0) + '</h3><p>Productos Críticos</p></div></div>' +
                            '<div class="col-md-4"><div class="stat-card bg-success"><i class="fas fa-dollar-sign"></i><h3>$' + (data.valor_inventario || 0) + '</h3><p>Valor Inventario</p></div></div>' +
                            '</div>';
                    }
                    if (data.productos && data.productos.length > 0) {
                        html += '<h5>📋 Detalle de Productos</h5><div class="table-responsive"><table class="table table-striped"><thead><tr><th>Producto</th><th>Stock</th><th>Días hasta agotarse</th><th>Estado</th></tr></thead><tbody>';
                        for (let p of data.productos) {
                            html += `<tr><td>${p.producto}</td><td>${p.stock_actual}</td><td>${p.prediccion?.dias_hasta_agotarse || 'N/A'}</td><td>${p.prediccion?.estado || 'Desconocido'}</td></tr>`;
                        }
                        html += '</tbody></table></div>';
                    }
                    document.getElementById('content').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('content').innerHTML = '<div class="alert alert-danger">Error: ' + error + '</div>';
                });
        }
        function verProductos() {
            document.getElementById('loading').style.display = 'block';
            fetch('/api/productos')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    if (data.productos) {
                        let html = '<h5>📦 Catálogo de Productos</h5><table class="table"><thead><tr><th>Nombre</th><th>Categoría</th><th>Precio</th></tr></thead><tbody>';
                        for (let p of data.productos) html += `<tr><td>${p.nombre}</td><td>${p.categoria}</td><td>$${p.precio}</td></tr>`;
                        html += '</tbody></table>';
                        document.getElementById('content').innerHTML = html;
                    }
                });
        }
    </script>
</body>
</html>
'''


# ============================================================
# RUTAS DE LA APLICACIÓN
# ============================================================

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/test')
def test_api():
    return jsonify({
        "status": "success",
        "message": "✅ API de Inventario Inteligente funcionando",
        "version": "3.0",
        "timestamp": datetime.now().isoformat(),
        "servicios": ["vision", "database", "prediction", "inventory"]
    })

@app.route('/api/analizar-inventario')
def analizar_inventario():
    print("\n🔄 INICIANDO ANÁLISIS DE INVENTARIO")
    deteccion = detect_products()
    productos_detectados = deteccion.get("productos", [])
    
    productos_analizados = []
    for producto_detectado in productos_detectados:
        nombre = producto_detectado["nombre"]
        stock_actual = producto_detectado["cantidad"]
        producto_info = get_product_info(nombre)
        
        if producto_info:
            historial_ventas = get_sales_history(nombre, days=30)
            prediccion = predict_stock_outage(historial_ventas, stock_actual, producto_info)
            productos_analizados.append({
                "producto": nombre,
                "stock_actual": stock_actual,
                "informacion": {"categoria": producto_info.get("categoria"), "precio": producto_info.get("precio")},
                "prediccion": prediccion
            })
        else:
            productos_analizados.append({
                "producto": nombre,
                "stock_actual": stock_actual,
                "informacion": None,
                "prediccion": {"dias_hasta_agotarse": "N/A", "estado": "NO ENCONTRADO EN BD"}
            })
    
    analisis = calculate_inventory_metrics(productos_detectados, product_database)
    valor_inventario = calculate_inventory_value(productos_detectados, product_database)
    
    return jsonify({
        "status": "success",
        "deteccion": deteccion,
        "productos": productos_analizados,
        "analisis": analisis,
        "valor_inventario": valor_inventario,
        "resumen": {
            "total_productos": len(productos_analizados),
            "productos_criticos": analisis["resumen"]["productos_criticos"],
            "valor_total": valor_inventario
        }
    })

@app.route('/api/productos')
def obtener_productos():
    return jsonify({"status": "success", "total": len(get_all_products()), "productos": get_all_products()})

@app.route('/api/producto/<nombre>')
def obtener_producto(nombre):
    producto = get_product_info(nombre)
    if producto:
        return jsonify({"status": "success", "producto": producto})
    else:
        return jsonify({"status": "error", "message": f"Producto '{nombre}' no encontrado"}), 404

@app.route('/api/recomendaciones')
def obtener_recomendaciones():
    productos = get_all_products()
    recomendaciones = []
    for producto in productos[:5]:
        recomendaciones.append({
            "producto": producto["nombre"],
            "accion": "REVISAR STOCK",
            "prioridad": "MEDIA",
            "motivo": f"Producto con historial de {len(producto['historial_ventas'])} días"
        })
    return jsonify({"status": "success", "recomendaciones": recomendaciones, "total": len(recomendaciones)})

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("📦 SISTEMA DE INVENTARIO INTELIGENTE - VERSIÓN UNIFICADA")
    print("=" * 60)
    print("🌐 Servidor disponible en: http://localhost:5020")
    print("📝 Presiona Ctrl+C para detener")
    print("=" * 60)
    app.run(debug=True, port=5020, host='0.0.0.0', threaded=True)
