#services/database/db_reader.py
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventario.db')

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    conn.close()

    productos = [dict(row) for row in rows]

    for p in productos:
        if isinstance(p.get('historial_ventas'), str):
            try:
                p['historial_ventas'] = json.loads(p['historial_ventas'])
            except json.JSONDecodeError:
                p['historial_ventas'] = []

    return productos

def get_product_info(product_name):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (product_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        producto = dict(row)
        if isinstance(producto.get('historial_ventas'), str):
            try:
                producto['historial_ventas'] = json.loads(producto['historial_ventas'])
            except json.JSONDecodeError:
                producto['historial_ventas'] = []
        return producto

    return None