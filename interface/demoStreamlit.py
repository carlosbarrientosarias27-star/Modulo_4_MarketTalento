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
    if 'mostrar_formulario' not in st.session_state:
        st.session_state.mostrar_formulario = False

    if st.button('➕ Productos', use_container_width=False):
        st.session_state.mostrar_formulario = True
    if st.session_state.mostrar_formulario:    
        st.subheader("📦 Registro de Nuevo Producto")
        
        # 1. Inicia el formulario
        with st.form("nuevo_producto_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("ID / SKU", value="AUTO-GENERADO", disabled=True)
                nombre_nuevo = st.text_input("Nombre completo")
                
                # Lista ajustada para evitar errores de la base de datos[cite: 1, 2]
                lista_categorias = [
                    "Refrigerados (Frío)", "Conservas", "Bebidas", 
                    "Panadería", "Despensa", "Alimentos Básicos", 
                    "Snacks", "Desayuno" , "Otros"
                ]
                categoria = st.selectbox("Categoría", lista_categorias)
                precio = st.number_input("Precio de Venta (€)", min_value=0.0, format="%.2f")
                unidad_medida = st.text_input("Unidad de medida", placeholder="Ej: kg, Litros, Pack")
            
            with col_b:
                stock_inicial = st.number_input("Stock Inicial", min_value=0, disabled=True)
                stock_minimo_n = st.number_input("Stock Mínimo", min_value=0, step=1)
                stock_maximo_n = st.number_input("Stock Máximo", min_value=0, step=1)
                t_reposicion_n = st.number_input("Tiempo de Reposición (Días)", min_value=1, step=1)
            
            # 2. EL BOTÓN DEBE ESTAR AQUÍ (DENTRO DEL FORM)
            submit_button = st.form_submit_button("Guardar Producto")

            # 3. LA LÓGICA DE GUARDADO TAMBIÉN DENTRO DEL FORM
            if submit_button:
                if not nombre_nuevo:
                    st.error("❌ El nombre del producto es obligatorio.")
                else:
                    datos = {
                        'nombre': nombre_nuevo,
                        'categoria': categoria,
                        'precio': precio,
                        'unidad': unidad_medida,
                        'min': stock_minimo_n,
                        'inicial': stock_inicial,
                        'max': stock_maximo_n,
                        'reposicion': t_reposicion_n
                    }
                    
                    # Llamamos a la función de database_manager.py
                    if guardar_producto_nuevo(datos):
                        st.success(f"✅ ¡{nombre_nuevo} guardado con éxito!")
                        st.session_state.mostrar_formulario = False
                        st.rerun()  # Recarga para que aparezca en el inventario[cite: 3, 5]
                    else:
                        st.error("❌ Error al guardar. Revisa que la categoría sea correcta.")
                        

with col_btn2:
    # --- BOTÓN DE ANÁLISIS (DERECHA) ---
    if st.button('🔍 Analizar Inventario', use_container_width=False):
        # 1. Procesamiento de detección (Cámara)
        deteccion = detect_products()
        lista_detectados = deteccion.get('productos', [])
        
        # 2. PREPARACIÓN DE DATOS PARA EVITAR EL KEYERROR
        # Creamos una versión de la DB donde 'cantidad' sea el stock guardado
        # o lo que la cámara detectó en ese momento.
        full_db_con_cantidad = []
        detectados_dict = {p['nombre']: p.get('cantidad', 0) for p in lista_detectados}

        for p in todos_los_productos:
            p_copia = p.copy()
            # Si la cámara lo vio, usamos esa cantidad; si no, 0 o su stock inicial
            p_copia['cantidad'] = detectados_dict.get(p['nombre'], 0)
            full_db_con_cantidad.append(p_copia)

        # 3. LLAMADA A MÉTRICAS (Ahora ya llevan la clave 'cantidad')
        metricas_full = calculate_inventory_metrics(full_db_con_cantidad, todos_los_productos)
        resumen = metricas_full['resumen']

        # --- Sección A — Métricas Visuales ---
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric('Detectados', len(lista_detectados))
        m2.metric('Unidades', resumen['total_unidades'])
        m3.metric('Críticos', resumen['productos_criticos'])
        m4.metric('Stock Bajo', resumen['productos_bajos'])
        m5.metric('Total DB', len(todos_los_productos))

        st.markdown("---")

        # --- Sección B — Detalle del Análisis (Los 28 productos) ---
        st.subheader('📊 Detalle del Análisis')
        filas = []

        for info_p in full_db_con_cantidad:
            nombre = info_p['nombre']
            stock_det = info_p['cantidad'] # Ya está definida arriba
            
            stock_max = info_p.get('stock_maximo', 0)
            sug_compra = max(0, stock_max - stock_det)
            h_ventas = info_p.get('historial_ventas', [])

            # Predicción y Recomendación
            pred = predict_stock_outage(h_ventas, stock_det, info_p)
            pred['producto'] = nombre
            pred['stock_actual'] = stock_det
            est_pred = pred.get('estado', 'Normal')

            rec_text = 'OK'
            if est_pred != 'Normal':
                recs = generate_recommendations([pred])
                rec_text = recs[0].get('accion', 'Revisar') if recs else 'Sin datos'

            filas.append({
                "Producto": nombre,
                "Stock Actual": stock_det,
                "Estado": est_pred,
                "Días hasta Agotarse": pred.get('dias_hasta_agotarse', 'N/A'),
                "Recomendación": rec_text, 
                "Sugerencia Compra": sug_compra
            })

        # Mostrar los 28 productos en la tabla
        df = pd.DataFrame(filas)
        st.dataframe(df, use_container_width=True)

# --- SECCIÓN C — RECOMENDACIONES Y VALOR (¡AHORA DENTRO DEL IF!) ---
        st.markdown("---")
        col_rec, col_val = st.columns(2)

        with col_rec:
            st.subheader('🚨 Recomendaciones')
            # Aquí 'df' ya existe porque estamos dentro del botón
            alertas = df[df["Estado"].str.upper().isin(["CRÍTICO", "BAJO"])]
            if not alertas.empty:
                for _, row in alertas.iterrows():
                    color = "red" if row["Estado"].upper() == "CRÍTICO" else "orange"
                    st.markdown(f":{color}[**{row['Producto']}**]: {row['Recomendación']}")
            else:
                st.success("Inventario optimizado.")

        with col_val:
            st.subheader('💰 Valor del Inventario')
            # Calculamos el valor usando los 28 productos
            valor_total = calculate_inventory_value(lista_detectados, todos_los_productos)
            st.metric('Valor Total estimado', f'{valor_total:.2f} €')