import sqlite3
import os
import json
from product_db import product_database

def inicializar_sqlite():
    # Definir ruta relativa al archivo actual
    db_path = os.path.join(os.path.dirname(__file__), 'inventario.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. ELIMINAR LA TABLA SI YA EXISTE (Esto evita tu error actual)
    cursor.execute('DROP TABLE IF EXISTS productos')

    # 2. CREAR LA TABLA CON LA NUEVA ESTRUCTURA
    cursor.execute ('''
        CREATE TABLE productos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT CHECK(categoria IN (
                'Refrigerados', 'Conservas', 'Bebidas', 
                'Panadería', 'Despensa', 'Alimentos Básicos', 
                'Snacks', 'Desayuno'
            )),
            precio REAL,
            unidad TEXT,
            stock_minimo INTEGER,
            stock_actual INTEGER,
            stock_maximo INTEGER,
            tiempo_reposicion INTEGER,
            historial_ventas TEXT
        )
    ''')

    # Insertar los 27 productos
    for nombre, info in product_database.items():
        ventas_json = json.dumps(info.get('historial_ventas', []))
        
        cursor.execute('''
            INSERT OR REPLACE INTO productos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            info['id'], 
            info['nombre'], 
            info['categoria'], 
            info['precio'],
            info['unidad'], 
            info['stock_minimo'], 
            info.get('stock_actual', 0), # Añadido para coincidir con la imagen
            info['stock_maximo'],
            info['tiempo_reposicion'], 
            ventas_json
        ))

    conn.commit()
    conn.close()
    print(f"✅ SQLite creado exitosamente en: {db_path}")

if __name__ == "__main__":
    inicializar_sqlite()