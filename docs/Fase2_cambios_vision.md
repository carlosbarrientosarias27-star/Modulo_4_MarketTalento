Documentación de Fase 2: Integración de Visión Artificial

1. Arquitectura del Módulo de Visión
En esta fase, la lógica de detección de imágenes se ha desacoplado del núcleo de la aplicación (app.py) para residir en su propio paquete de servicios.

services/vision/detector.py: Actúa como el motor principal. Orquesta la carga de escenarios y la selección aleatoria de una "captura de cámara".
services/vision/scenario_loader.py: Funciona como la base de datos de imágenes simuladas, proporcionando listas de productos detectados, sus cantidades y el nivel de confianza de la IA.

2. Flujo de Datos en app.py
El archivo principal ahora consume el servicio de visión de forma modular. El flujo es el siguiente:

Activación: La ruta /api/analizar-inventario invoca la función detect_products().
Detección: El módulo detector.py selecciona un escenario (ej. "Estantería de supermercado").
Procesamiento: app.py recibe el JSON con los productos detectados y procede a cruzarlos con la base de datos centralizada en product_db.py.

3. Sincronización de Identificadores (Crucial)
Para que el sistema de inventario funcione, los nombres devueltos por la "visión" deben coincidir exactamente con los registros de la base de datos. Se han identificado y corregido las siguientes discrepancias en los archivos cargados:

Producto Detectado (scenario_loader.py) Producto en DB (product_db.py) Resultado del Cruce
"Leche" "Leche Entera" ❌ Error: No encontrado
"Leche Entera" "Leche Entera" ✅ Éxito: Sincronizado
"Huevos" "Huevos M" ❌ Error: No encontrado
"Huevos M" "Huevos M" ✅ Éxito: Sincronizado

Nota Técnica: Se recomienda que scenario_loader.py sea el archivo que se ajuste para reflejar las descripciones precisas de los productos de la Fase 1.

4. Métricas de Confianza y Calidad
El simulador de visión no solo entrega cantidades, sino también un valor de confianza (ej. 0.92 para Leche Entera). En futuras fases, este valor permitirá:

Ignorar detecciones dudosas (confianza < 0.70).
Solicitar una "segunda revisión" humana si la confianza es baja.5. 

Próximos Pasos: Fase 3
Una vez estabilizada la visión, la siguiente fase consistirá en:Extraer la Lógica de Predicción (predict_stock_outage) de app.py hacia services/inventory/prediction.py.Implementar alertas automáticas basadas en los días estimados para el agotamiento del stock.Referencias de Archivos Analizados:services/vision/detector.py: Lógica de orquestación de visión.services/vision/scenario_loader.py: Repositorio de escenarios simulados.services/database/product_db.py: Maestro de productos de la Fase 1.app.py: Punto de entrada y controlador de rutas.