import json 
import sys
import os

# Adds the parent directory to the path so it can find 'services'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from services.database.db_reader import get_all_products 
from services.vision.detector import detect_products
from services.inventory.metrics import calculate_inventory_metrics 
from services.inventory.valuation import calculate_inventory_value
from services.inventory.recommender import generate_recommendations
from services.prediction.stock_predictor import predict_stock_outage

# Configuración inicial de la página
st.set_page_config(page_title='Markettalento Inventario', page_icon='📦', layout='wide')
st.title('📦 Sistema de Inventario — Markettalento')

todos_los_productos = get_all_products()

# Disparador del análisis
if st.button('🔍 Analizar Inventario'):
    # 1. Procesamiento de datos mediante Visión Artificial
    deteccion = detect_products()
    productos = deteccion['productos']

    # --- Sección A — Resultados del Análisis (Métricas) ---
    # 1. Preparamos los datos de la DB para que la función no falle
    # Añadimos una cantidad por defecto (ej. stock_maximo) para que pueda calcular
    full_db_con_stock = []
    for p in todos_los_productos: 
        p_copia = p.copy()
        # Si el producto fue detectado por la cámara, usamos esa cantidad
        # Si no, usamos 0 o su stock_maximo para la métrica
        p_copia['cantidad'] = p_copia.get('cantidad', p_copia.get('stock_maximo', 0))
        full_db_con_stock.append(p_copia)
        
    # Calculamos las métricas antes de mostrarlas
    metricas_full = calculate_inventory_metrics(full_db_con_stock, todos_los_productos)

    # Extraemos el diccionario de resumen para facilitar el acceso
    resumen = metricas_full['resumen']

    col1, col2, col3, col4, col5= st.columns(5)
    col1.metric('Productos Detectados', resumen['total_productos'])
    col2.metric('Unidades Totales', resumen['total_unidades'])
    col3.metric('Productos Críticos', resumen['productos_criticos'])
    col4.metric('Stock Bajo', resumen['productos_bajos'])
    col5.metric('Total DB', len(todos_los_productos))

    st.markdown("---")

# --- Sección B — Detalle del Análisis (Tabla) ---
    st.subheader('📊 Detalle del Análisis')
    filas = []
    
    # Mapeo para búsqueda rápida en la lista de SQLite
    db_lookup = {p['nombre']: p for p in todos_los_productos}

    for p in productos:
        # 1. Extraer nombre y stock detectado
        nombre = p['nombre']
        stock_actual = p['cantidad']

        # 2. Obtener info de la base de datos
        info_producto = db_lookup.get(nombre, {}) 
        stock_maximo = info_producto.get('stock_maximo', stock_actual)
        sugerencia_cantidad = max(0, stock_maximo - stock_actual)
    
        # Si ya arreglaste db_reader.py, esto ya vendrá como lista
        historial_ventas = info_producto.get('historial_ventas', [])

        # 3. Llamar al predictor con los TRES argumentos
        pred = predict_stock_outage(historial_ventas, stock_actual, info_producto)
        
        # ADD THIS LINE: Ensure the 'producto' key exists for the recommender
        pred['producto'] = nombre
        pred['stock_actual'] = stock_actual

        # FIX: Define estado_pred here, inside the loop
        estado_pred = pred.get('estado', 'Normal')

        # 4. Generate recommendation safely
        if estado_pred != 'Normal':
                # Get the recommendation list
                # Now [pred] contains the 'producto' key required by recommender.py
                recommendations = generate_recommendations([pred])
            
                # Verify the list isn't empty and the key exists
                if recommendations and len(recommendations) > 0:
                    rec = recommendations[0].get('accion', 'Acción no definida')
                else:
                    rec = 'Sin recomendación disponible'
        else:
                rec = 'OK'

        filas.append({
                "Producto": nombre,
                "Stock Actual": stock_actual,
                "Estado": estado_pred,
                "Días hasta Agotarse": pred.get('dias_hasta_agotarse', 'N/A'),
                "Recomendación": rec, 
                "Sugerencia Compra": sugerencia_cantidad
        })

        df = pd.DataFrame(filas)
        st.dataframe(df, use_container_width=True)
        st.markdown("---")

# --- Sección C — Recomendaciones y Valor del Inventario ---
    col_rec, col_val = st.columns(2)

    with col_rec:
        st.subheader('🚨 Recomendaciones de Reposición')
        alertas = df[df["Estado"].str.upper().isin(["CRÍTICO", "BAJO"])]
        
        if not alertas.empty:
            for _, row in alertas.iterrows():
                color = "red" if row["Estado"] == "Crítico" else "orange"
                st.markdown(f":{color}[**{row['Producto']}**]: {row['Recomendación']}")
        else:
            st.success("Inventario optimizado. No se requieren acciones inmediatas.")

    with col_val:
        st.subheader('💰 Valor del Inventario')
        valor = calculate_inventory_value(productos, todos_los_productos)
        st.metric('Valor Total estimado', f'{valor:.2f} €')