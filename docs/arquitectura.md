# 1. Evolución de la Arquitectura

### Monolito Original (Heredado)
En la carpeta Heredado, se observan archivos como InventarioAlfa.py. En un esquema monolítico, un solo archivo suele gestionar la conexión a datos, el cálculo de métricas y la lógica de negocio, lo que dificulta el mantenimiento.

Plaintext+---------------------------------------+
|          ARCHIVO MONOLÍTICO           |
| (DB + Lógica + API + UI todo en uno)  |
+---------------------------------------+
                   |
                   v
      Dificultad para testear y escalar


### Arquitectura Modular Actual (SRP)
La nueva estructura separa las preocupaciones en capas independientes. Si necesitas cambiar la base de datos, solo tocas services/database; si cambias la IA, solo tocas services/vision.Plaintext      

[ Usuario / Cliente ]
               |
      +--------v---------+
      |   Interface      | <--- (Streamlit / Templates)
      +--------+---------+
               |
      +--------v---------+
      |     Routes       | <--- (api_routes.py: Orquestador)
      +--------+---------+
               |
      +--------v---------+
      |    Services      | <--- (Lógica de Negocio Modular)
      |  +------------+  |
      |  |  Database  |  | <--- Lectura/Escritura
      |  +------------+  |
      |  |  Vision    |  | <--- Detección de objetos
      |  +------------+  |
      |  | Inventory  |  | <--- Cálculos y Métricas
      |  +------------+  |
      |  | Prediction |  | <--- ML y Demanda
      |  +------------+  |
      +------------------+


## 2. Descripción de Módulos y Responsabilidades (SRP)
Cada directorio bajo services/ cumple estrictamente con una función:

| Módulo | Única Responsabilidad (SRP) | Archivos Clave |
| :--- | :--- | :--- |
| **database** | Gestión de persistencia. Solo lee/filtra datos, no conoce la lógica de negocio. | `product_db.py`, `db_reader.py` |
| **vision** | Procesamiento de imágenes. Su meta es detectar elementos en un escenario. | `detector.py`, `scenario_loader.py` |
| **inventory** | Lógica financiera y de stock. Calcula valor y genera recomendaciones. | `valuation.py`, `recommender.py` |
| **prediction** | Análisis estadístico y modelos. Predice comportamiento futuro basado en datos. | `stock_predictor.py`, `demand_analyzer.py` |
| **routes** | Interfaz de comunicación (API). Expone servicios al mundo exterior. | `api_routes.py` |
| **interface** | Capa de presentación. Se encarga exclusivamente de la UI. | `demoStreamlit.py` |

| Ventaja | Descripción |
| :--- | :--- |
| **Testabilidad** | Permite realizar **Pruebas Unitarias** aisladas. Puedes testear el cálculo de valor sin activar el módulo de Visión. |
| **Mantenibilidad** | Localización inmediata de errores. Si falla la predicción, el problema está en `services/prediction`. |
| **Escalabilidad** | Permite cambiar la interfaz manteniendo intactos los módulos de `services/` y `routes/`. |