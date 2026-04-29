# Documentación de Fase 1: Limpieza y Modularización

## 1. Estado Actual de app.py
El archivo app.py se encuentra en un estado de transición. Aunque ya incluye las sentencias import para los nuevos módulos, todavía conserva internamente funciones que ahora deberían ser consumidas exclusivamente desde services/database/.

- Elementos a Eliminar en app.py
- Debes borrar las siguientes definiciones de funciones dentro de app.py para evitar conflictos de nombres y redundancia:
    calculate_inventory_metrics: Esta lógica debe moverse a un nuevo servicio de inventario.
    calculate_inventory_value: Esta lógica debe delegarse.
    generate_recommendations: Debe salir del archivo principal.

## 2. Cambios Requeridos en los Módulos de Base de Datos
Tras revisar tus archivos db_filter.py y db_reader.py, se identificaron errores que impedirán que app.py funcione correctamente:

### Corrección en services/database/db_filter.py
La función get_sales_history tiene un error de sintaxis al intentar usar un diccionario como una función.

- Error actual: product = product_database(product_name)
- Corrección: product = product_database.get(product_name)

### Corrección en services/database/db_reader.py
Asegúrate de que este archivo solo contenga las funciones de lectura pura para mantener la responsabilidad única del módulo.

## 3. Sincronización de Datos (Crítico)
Existe una discrepancia entre los nombres que usa el simulador de visión en app.py y los datos reales en product_db.py. Si no se sincronizan, la API devolverá siempre "Producto no encontrado".

| Producto en Visión (`app.py`) | Producto en DB (`product_db.py`) | Estado |
| :--- | :--- | :--- |
| "Leche" | "Leche Entera" | ❌ Incompatible |
| "Huevos" | "Huevos M" | ❌ Incompatible |
| "Agua" | "Agua Mineral" | ❌ Incompatible |
| "Café" | "Café Molido" | ❌ Incompatible |

Acción necesaria: Debes actualizar la función detect_products en app.py para que los nombres coincidan exactamente con las llaves del diccionario en product_db.py.

## 4. Estructura de Importación Final
Para que la Fase 1 se considere exitosa, la cabecera de tu app.py debe lucir así, sin ninguna definición de base de datos local:Python# app.py modificado

from services.database.product_db import product_database
from services.database.db_reader import get_product_info, get_all_products
from services.database.db_filter import get_sales_history

## 5. Verificación de la Fase 1
Una vez realizados los cambios, puedes verificar la integración usando el endpoint de prueba:
Endpoint: GET /api/producto/Leche Entera
Resultado esperado: Un JSON con el precio (1.20) y la categoría (Refrigerados) extraídos directamente de product_db.py.

### Referencias:

- Archivo product_db.py (Base de datos de productos y diccionarios).
- Archivo db_filter.py (Lógica de filtrado y ventas).
- Archivo db_reader.py (Funciones de lectura de productos).
- Archivo app.py (Código principal del sistema de inventario).

## 6. Transición a SQLite3 (Infraestructura)
Para garantizar la persistencia de datos y facilitar la integración con Streamlit, se migrará el diccionario `product_database` a un archivo `inventario.db`.

- **Ubicación:** `services/database/inventario.db`
- **Herramienta de migración:** `services/database/setup_db.py`
- **Impacto:** Las funciones `get_product_info` y `get_sales_history` ahora realizarán consultas SQL.

---

Para cerrar este capítulo en tus archivos .md:

docs/Fase1_cambios_database.md
Validación de Diccionarios: Se confirmó que db_reader.py transforma las filas de SQLite en diccionarios nativos de Python para mantener la compatibilidad con los servicios de métricas.  

Mapeo de Memoria: Se implementó la técnica de db_lookup para optimizar las búsquedas de productos, reduciendo la complejidad de los cálculos de inventario.