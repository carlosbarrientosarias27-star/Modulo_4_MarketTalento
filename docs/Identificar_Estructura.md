## 1. Arquitectura de Software (Común en ambos)Ambos códigos siguen un patrón de "Servicios Simulados" dentro de un solo archivo:

- Base de Datos Simulada: Un diccionario product_database que contiene el catálogo, precios, stocks mínimos y el historial de ventas.
- Servicio de Visión Artificial (detect_products): Simula la captura de una cámara eligiendo aleatoriamente entre tres escenarios (Stock moderado, alto o bajo).
- Servicio de Inventario (calculate_inventory_metrics): Compara lo "detectado" por la cámara contra las reglas de negocio de la base de datos para determinar si hay faltantes.- - Servicio de Predicción (predict_stock_outage): Calcula el promedio de ventas diarias y estima cuántos días faltan para que el stock se agote.

## 2. Comparativa de Componentes

| Característica | `InventarioAlfa.py` | `EndPoint_Api.py` |
| :--- | :--- | :--- |
| **Objetivo** | Versión para alumnos (Refactorización) | Dashboard de pruebas de API |
| **Puerto de ejecución** | 5005 | 5002 |
| **Interfaz (Frontend)** | Enfocada en resultados visuales (gráficos de estado, tablas). | Enfocada en desarrollo (botones para probar cada endpoint JSON). |
| **Endpoints API** | `/api/test`, `/api/analizar-inventario`, `/api/productos`. | Los anteriores + `/api/producto/<nombre>` y `/api/recomenaciones`. |
| **Complejidad Lógica** | Estándar. | Ligeramente superior (incluye lógica de recomendaciones detallada). |

## 3. Flujo de Datos
El sistema funciona de forma lineal cada vez que se llama al endpoint de análisis:

- Detección: Se genera una lista aleatoria de productos y cantidades (detect_products).
- Cruce de Datos: Se busca cada producto detectado en la product_database.
- Cálculo: * Se calcula el valor monetario del inventario.
    Se ejecuta la fórmula de predicción: $VentasPromedio = \frac{\sum Historial}{N}$.
    Se estima: $DíasRestantes = \frac{StockActual}{VentasPromedio}$.
- Respuesta: Se devuelve un JSON con el resumen y se renderiza en la interfaz HTML.

## 4. Observaciones para Refactorización
Si tu objetivo es mejorar estos códigos (como sugiere el comentario en InventarioAlfa.py), la estructura actual es un Antipatrón (Spaghetti Code) porque mezcla:

- Datos (Diccionarios).
- Lógica de negocio (Funciones de cálculo).
- Rutas de red (Flask).
- Interfaz (HTML/JavaScript embebido en strings).

### Sugerencia de carpetas:
- /models: Para la base de datos y lógica de productos.
- /services: Para la visión artificial y predicciones.
- /routes: Para los endpoints de Flask.
- /templates: Para extraer el código HTML a archivos .html reales.