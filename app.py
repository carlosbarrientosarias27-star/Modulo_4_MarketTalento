# ============================================================
# codigoInicio.py - SISTEMA DE INVENTARIO INTELIGENTE
# Versión unificada para alumnos - SIN creación automática de archivos
# ============================================================
# Los alumnos deben refactorizar este código en módulos separados
# NO genera archivos automáticamente al ejecutarse
# ============================================================

import random
import statistics
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template 
from services.database.product_db import product_database 
from services.database.db_reader import get_product_info, get_all_products 
from services.database.db_filter import get_sales_history 
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics 
from services.inventory.recommender import generate_recommendations 
from services.inventory.valuation import calculate_inventory_value 
from services.prediction.stock_predictor import predict_stock_outage

app = Flask(__name__)



# ============================================================
# RUTAS DE LA APLICACIÓN
# ============================================================

@app.route('/')
def home():
    return render_template('index.html')

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