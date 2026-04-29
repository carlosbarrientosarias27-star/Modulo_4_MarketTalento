#services/database/db_reader.py
import sqlite3
import json 
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventario.db')

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    
    # Convertimos los objetos Row en diccionarios reales de Python
    productos = [dict(row) for row in rows]
    
    conn.close()
    for p in productos:
        # Si el historial viene como texto de la DB, lo convertimos a lista real
        if isinstance(p['historial_ventas'], str):
            try:
                p['historial_ventas'] = json.loads(p['historial_ventas'])
            except json.JSONDecodeError:
                p['historial_ventas'] = [] # Evita que rompa si el texto está mal formado
    
    return productos 

def get_product_info(product_name):
    """Busca un producto específico por nombre."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # <-- Añade esto para consistencia
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (product_name,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        producto = dict(row)
        # Procesar JSON igual que en get_all_products
        if isinstance(producto['historial_ventas'], str):
            producto['historial_ventas'] = json.loads(producto['historial_ventas'])
        return producto
    return None