import sys
import os

# Adds the parent directory to the path so it can find 'services'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import pandas as pd
from services.database.product_db import product_database
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics 
from services.inventory.valuation import calculate_inventory_value
from services.inventory.recommender import generate_recommendations
from services.prediction.stock_predictor import predict_stock_outage

# Configuración inicial de la página
st.set_page_config(page_title='Markettalento Inventario', page_icon='📦', layout='wide')
st.title('📦 Sistema de Inventario — Markettalento')

# Disparador del análisis
if st.button('🔍 Analizar Inventario'):
    # 1. Procesamiento de datos mediante Visión Artificial
    deteccion = detect_products()
    productos = deteccion['productos']

# --- Sección A — Resultados del Análisis (Métricas) ---
    # Calculamos las métricas antes de mostrarlas
    metricas_full = calculate_inventory_metrics(productos, product_database)

    # Extraemos el diccionario de resumen para facilitar el acceso
    resumen = metricas_full['resumen']

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Productos Detectados', resumen['total_productos'])
    col2.metric('Unidades Totales', resumen['total_unidades'])
    col3.metric('Productos Críticos', resumen['productos_criticos'])
    col4.metric('Stock Bajo', resumen['productos_bajos'])

    st.markdown("---")

# --- Sección B — Detalle del Análisis (Tabla) ---
    st.subheader('📊 Detalle del Análisis')
    filas = []
    
    for p in productos:
        # 1. Extract name and stock from the detected product[cite: 4]
        nombre = p['nombre']
        stock_actual = p['cantidad']
    
        # 2. Retrieve product info and sales history from the database[cite: 4]
        # We use .get() to avoid errors if the product isn't in the DB
        info_producto = product_database.get(nombre, {})
        historial_ventas = info_producto.get('ventas', []) 
    
        # 3. Call the predictor with the correct THREE arguments
        pred = predict_stock_outage(historial_ventas, stock_actual, info_producto)
    
        estado_pred = pred.get('estado', 'Normal')[cite: 4]
    
        # 4. Generate recommendation[cite: 4]
        rec = generate_recommendations([pred])[0]['accion'] if estado_pred != 'Normal' else 'OK'[cite: 4]
    
        filas.append({
            "Producto": nombre,[cite: 4]
            "Stock Actual": stock_actual,[cite: 4]
            "Estado": estado_pred,[cite: 4]
            "Días hasta Agotarse": pred.get('dias_hasta_agotarse', 'N/A'),[cite: 4]
            "Recomendación": rec[cite: 4]
    })

    df = pd.DataFrame(filas)[cite: 4]
    st.dataframe(df, use_container_width=True)[cite: 4]
    st.markdown("---")

# --- Sección C — Recomendaciones y Valor del Inventario ---
    col_rec, col_val = st.columns(2)

    with col_rec:
        st.subheader('🚨 Recomendaciones de Reposición')
        alertas = df[df["Estado"].isin(["Crítico", "Bajo"])]
        
        if not alertas.empty:
            for _, row in alertas.iterrows():
                color = "red" if row["Estado"] == "Crítico" else "orange"
                st.markdown(f":{color}[**{row['Producto']}**]: {row['Recomendación']}")
        else:
            st.success("Inventario optimizado. No se requieren acciones inmediatas.")

    with col_val:
        st.subheader('💰 Valor del Inventario')
        valor = calculate_inventory_value(productos, product_database)
        st.metric('Valor Total estimado', f'{valor:.2f} €')