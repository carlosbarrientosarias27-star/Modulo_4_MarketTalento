import sys
import os
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE RUTAS Y PÁGINA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.database.product_db import product_database
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics 
from services.inventory.valuation import calculate_inventory_value
from services.prediction.stock_predictor import predict_stock_outage

st.set_page_config(page_title="Smart Inventory Dashboard", layout="wide", page_icon="📦")

# 2. ESTILOS PERSONALIZADOS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE ESTADO (SESSION STATE)
if 'scan_data' not in st.session_state:
    st.session_state.scan_data = None

# 4. SIDEBAR - CONTROL DE ACCIONES
with st.sidebar:
    st.header("🎮 Panel de Control")
    st.info("Simula el escaneo de una estantería o almacén usando Visión Artificial.")
    
    if st.button("🔍 Escanear Nuevo Escenario", use_container_width=True):
        # Llamada al detector (que usa scenario_loader internamente)
        resultado_deteccion = detect_products()
        st.session_state.scan_data = resultado_deteccion
        st.success(f"Escenario: {resultado_deteccion['descripcion']}")

# 5. UI PRINCIPAL
st.title("📦 Sistema de Inventario Inteligente")

if st.session_state.scan_data:
    escenario = st.session_state.scan_data
    productos_detectados = escenario['productos']
    
    # --- PROCESAMIENTO DE DATOS ---
    resumen_metricas = calculate_inventory_metrics(productos_detectados, product_database)
    valor_total = calculate_inventory_value(productos_detectados, product_database)
    
    # --- SECCIÓN 1: KPIs ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Valor del Stock", f"{valor_total} €")
    with col2:
        st.metric("Total Productos", resumen_metricas['resumen']['total_productos'])
    with col3:
        st.metric("Alertas Críticas", resumen_metricas['resumen']['productos_criticos'], delta_color="inverse")
    with col4:
        st.metric("Escenario Actual", escenario['descripcion'][:15] + "...")

    st.divider()

    # --- SECCIÓN 2: TABLA DETALLADA ---
    st.subheader("📋 Detalle del Inventario y Predicciones")
    
    tabla_data = []
    for p in productos_detectados:
        nombre = p['nombre']
        stock_actual = p['cantidad']
        info_base = product_database.get(nombre, {})
        
        # Obtener predicción
        prediccion = predict_stock_outage(
            info_base.get('historial_ventas', []), 
            stock_actual
        )
        
        tabla_data.append({
            "Producto": nombre,
            "Categoría": info_base.get('categoria', 'N/A'),
            "Stock Actual": stock_actual,
            "Mín. Requerido": info_base.get('stock_minimo', 0),
            "Días Restantes": prediccion['dias_hasta_agotarse'],
            "Estado": prediccion['estado'],
            "Sugerencia Compra": prediccion['cantidad_recommendada'] if stock_actual < info_base.get('stock_minimo', 0) else 0
        })
    
    df = pd.DataFrame(tabla_data)
    
    # Aplicar color a la tabla
    def color_estado(val):
        if "CRÍTICO" in str(val) or "AGOTADO" in str(val): return 'background-color: #ffcccc'
        if "BAJO" in str(val): return 'background-color: #fff4cc'
        if "ADEQUADO" in str(val): return 'background-color: #ccffcc'
        return ''

    st.dataframe(df.style.applymap(color_estado, subset=['Estado']), use_container_width=True)

    # --- SECCIÓN 3: RECOMENDACIONES ---
    with st.expander("💡 Recomendaciones de Reposición"):
        for rec in resumen_metricas['recomendaciones']:
            st.write(f"• {rec}")

else:
    st.warning("⚠️ No hay datos de escaneo. Presiona el botón 'Escanear' en el menú lateral para comenzar.")
    
    # Mostrar catálogo base si no hay escaneo
    with st.expander("Ver Catálogo de Productos"):
        st.json(product_database)