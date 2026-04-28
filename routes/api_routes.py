# routes/api_routes.py
from flask import Blueprint, jsonify, render_template
from datetime import datetime

# IMPORTACIONES NECESARIAS: El archivo necesita saber de dónde sacar estas funciones
from services.database.db_reader import get_product_info, get_all_products 
from services.database.db_filter import get_sales_history 
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics 
from services.inventory.valuation import calculate_inventory_value 
from services.prediction.stock_predictor import predict_stock_outage
from services.database.product_db import product_database

# Creamos el Blueprint en lugar de usar 'app' directamente
api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return render_template('index.html')

@api_bp.route('/api/test')
def test_api():
    return jsonify({
        "status": "success",
        "message": "✅ API de Inventario Inteligente funcionando",
        "version": "3.0",
        "timestamp": datetime.now().isoformat(),
        "servicios": ["vision", "database", "prediction", "inventory"]
    })

@api_bp.route('/api/analizar-inventario')
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

@api_bp.route('/api/productos')
def obtener_productos():
    return jsonify({"status": "success", "total": len(get_all_products()), "productos": get_all_products()})

@api_bp.route('/api/producto/<nombre>')
def obtener_producto(nombre):
    producto = get_product_info(nombre)
    if producto:
        return jsonify({"status": "success", "producto": producto})
    else:
        return jsonify({"status": "error", "message": f"Producto '{nombre}' no encontrado"}), 404

@api_bp.route('/api/recomendaciones')
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