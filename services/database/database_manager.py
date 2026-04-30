import sqlite3
import os

def obtener_ruta_db():
    # Como este archivo está en services/database/, subimos dos niveles 
    # para llegar a la raíz y luego entrar a /data/
    BASE_DIR = os.path.dirname(__file__)
    db_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'inventario.db'))
    return db_path

def guardar_producto_nuevo(datos_producto):
    db_path = obtener_ruta_db()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # El INSERT debe respetar el esquema definido en setup_db.py
        cursor.execute('''
            INSERT INTO productos (
                nombre, categoria, precio, unidad_medida, 
                stock_minimo, stock_inicial, stock_maximo, tiempo_reposicion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos_producto['nombre'], 
            datos_producto['categoria'], 
            datos_producto['precio'],
            datos_producto['unidad'],
            datos_producto['min'],
            datos_producto['inicial'],
            datos_producto['max'],
            datos_producto['reposicion']
        ))
        
        conn.commit() # ¡Vital para que los cambios se guarden!
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar: {e}")
        return False
    finally:
        conn.close()