import sqlite3
import os
import json
from product_db import product_database

def inicializar_sqlite():
    # Definir ruta relativa al archivo actual
    db_path = os.path.join(os.path.dirname(__file__), 'inventario.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla con la estructura de tu product_db.py
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL,
            unidad TEXT,
            stock_minimo INTEGER,
            stock_maximo INTEGER,
            tiempo_reposicion INTEGER,
            historial_ventas TEXT
        )
    ''')

    # Insertar los 27 productos
    for nombre, info in product_database.items():
        # Convertimos la lista de ventas a JSON para guardarla como texto
        ventas_json = json.dumps(info['historial_ventas'])
        
        cursor.execute('''
            INSERT OR REPLACE INTO productos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            info['id'], info['nombre'], info['categoria'], info['precio'],
            info['unidad'], info['stock_minimo'], info['stock_maximo'],
            info['tiempo_reposicion'], ventas_json
        ))

    conn.commit()
    conn.close()
    print(f"✅ SQLite creado exitosamente en: {db_path}")

if __name__ == "__main__":
    inicializar_sqlite()