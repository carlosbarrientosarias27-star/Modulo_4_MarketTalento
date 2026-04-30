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
from services.database.database_manager import guardar_producto_nuevo

# Configuración inicial de la página
st.set_page_config(page_title='Markettalento Inventario', page_icon='📦', layout='wide')
st.title('📦 Sistema de Inventario — Markettalento')

todos_los_productos = get_all_products()

# Creamos las columnas: col_btn1 (Izquierda - Productos), col_btn2 (Derecha - Analizar)
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    # --- BOTÓN PARA AÑADIR PRODUCTOS (IZQUIERDA) ---
    if st.button('➕ Productos', use_container_width=False):
        st.subheader("📦 Registro de Nuevo Producto")
        with st.form("nuevo_producto_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                id_prod = st.text_input("ID / SKU del Producto", value="AUTO-GENERADO", 
                                        disabled=True)
                nombre_nuevo = st.text_input("Nombre completo")
                lista_categorias = [
                    "Refrigerados (Frío)", "Conservas", "Bebidas", 
                    "Panadería", "Despensa", "Alimentos Básicos", 
                    "Snacks", "Desayuno", "Otros"
                ]
                categoria = st.selectbox("Categoría", lista_categorias)
                precio = st.number_input("Precio de Venta (€)", min_value=0.0, format="%.2f")
                unidad_medida = st.text_input("Unidad de medida", placeholder="Ej: kg, Litros, Pack")
            with col_b:
                stock_actual = st.number_input("Stock Actual", value=0, disabled=True)
                stock_minimo_n = st.number_input("Stock Mínimo", min_value=0, step=1)
                stock_maximo_n = st.number_input("Stock Máximo", min_value=0, step=1)
                t_reposicion_n = st.number_input("Tiempo de Reposición (Días)", min_value=1, step=1)
            
            historial_raw = st.text_input("Historial de Ventas (ej: 10, 15)", value="[]", 
    disabled=True, help="El historial se iniciará vacío para productos nuevos.")
        submit_button = st.form_submit_button("Guardar Producto")

        if submit_button:
                try:
                    historial_lista = [int(x.strip()) for x in historial_raw.split(",")]
                    st.success(f"✅ Producto **{nombre_nuevo}** guardado correctamente.")
                except ValueError:
                    st.error("❌ El historial debe ser números separados por comas.")

        if submit_button:
                if not nombre_nuevo:
                    st.error("❌ El nombre del producto es obligatorio.")
                else:
                    # 1. Empaquetamos los datos para la función de base de datos
                    datos = {
                        'nombre': nombre_nuevo,
                        'categoria': categoria,
                        'precio': precio,
                        'unidad': unidad_medida,
                        'min': stock_minimo_n,
                        'actual': stock_actual,
                        'max': stock_maximo_n,
                        'reposicion': t_reposicion_n
                    }
                    
                    # 2. Llamamos a la función que creamos en database_manager.py
                    if guardar_producto_nuevo(datos):
                        st.success(f"✅ Producto **{nombre_nuevo}** guardado en inventario.db")
                        st.rerun() 
                    else:
                        st.error("❌ Error al intentar guardar en la base de datos. Verifica la conexión.")
                        

with col_btn2:
    # --- BOTÓN DE ANÁLISIS (DERECHA) ---
    if st.button('🔍 Analizar Inventario', use_container_width=False):
        # 1. Procesamiento
        deteccion = detect_products()
        productos = deteccion['productos']

        # --- Sección A — Resultados (Métricas) ---
        full_db_con_stock = []
        for p in todos_los_productos: 
            p_copia = p.copy()
            p_copia['cantidad'] = p_copia.get('cantidad', p_copia.get('stock_maximo', 0))
            full_db_con_stock.append(p_copia)
            
        metricas_full = calculate_inventory_metrics(full_db_con_stock, todos_los_productos)
        resumen = metricas_full['resumen']

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric('Detectados', resumen['total_productos'])
        m2.metric('Unidades', resumen['total_unidades'])
        m3.metric('Críticos', resumen['productos_criticos'])
        m4.metric('Stock Bajo', resumen['productos_bajos'])
        m5.metric('Total DB', len(todos_los_productos))

        st.markdown("---")

        # --- Sección B — Detalle del Análisis (Tabla) ---
        st.subheader('📊 Detalle del Análisis')
        filas = []
        db_lookup = {p['nombre']: p for p in todos_los_productos}

        for p in productos:
            nombre = p['nombre']
            stock_det = p['cantidad']
            info_p = db_lookup.get(nombre, {}) 
            stock_max = info_p.get('stock_maximo', stock_det)
            sug_compra = max(0, stock_max - stock_det)
            h_ventas = info_p.get('historial_ventas', [])

            pred = predict_stock_outage(h_ventas, stock_det, info_p)
            pred['producto'] = nombre
            pred['stock_actual'] = stock_det
            est_pred = pred.get('estado', 'Normal')

            if est_pred != 'Normal':
                recs = generate_recommendations([pred])
                rec_text = recs[0].get('accion', 'Revisar') if recs else 'Sin datos'
            else:
                rec_text = 'OK'

            filas.append({
                "Producto": nombre,
                "Stock Actual": stock_det,
                "Estado": est_pred,
                "Días hasta Agotarse": pred.get('dias_hasta_agotarse', 'N/A'),
                "Recomendación": rec_text, 
                "Sugerencia Compra": sug_compra
            })

        df = pd.DataFrame(filas)
        st.dataframe(df, use_container_width=True)

        # --- Sección C — Recomendaciones y Valor ---
        st.markdown("---")
        col_rec, col_val = st.columns(2)

        with col_rec:
            st.subheader('🚨 Recomendaciones')
            alertas = df[df["Estado"].str.upper().isin(["CRÍTICO", "BAJO"])]
            if not alertas.empty:
                for _, row in alertas.iterrows():
                    color = "red" if row["Estado"] == "Crítico" else "orange"
                    st.markdown(f":{color}[**{row['Producto']}**]: {row['Recomendación']}")
            else:
                st.success("Inventario optimizado.")

        with col_val:
            st.subheader('💰 Valor del Inventario')
            valor_total = calculate_inventory_value(productos, todos_los_productos)
            st.metric('Valor Total estimado', f'{valor_total:.2f} €')