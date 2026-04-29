# services/database/db_filter.py 
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventario.db')

def get_sales_history(product_name):
    """Obtiene el historial de ventas desde SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT historial_ventas FROM productos WHERE nombre = ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0]) # Convertimos el JSON de vuelta a lista[cite: 1]
    return []