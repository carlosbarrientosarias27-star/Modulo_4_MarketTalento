## 8.2.1 — ¿Por qué el código original viola el SRP?
El código original (identificado como InventarioAlfa.py o similares en la carpeta Heredado) viola el Principio de Responsabilidad Única (SRP) porque era una "Clase Dios" o un script monolítico.

- Multitarea: Un solo archivo se encargaba de la conexión a la base de datos, el procesamiento de imágenes (visión artificial), la lógica de negocio del inventario y el cálculo de predicciones.

- Fragilidad: Al modificar la lógica de la base de datos, se corría el riesgo de romper la predicción de stock, ya que todo el código estaba estrechamente acoplado.

- Dificultad de Testeo: No se podían realizar pruebas unitarias aisladas; para probar un cálculo matemático, era necesario instanciar componentes de visión o de base de datos.

## 8.2.2 — Tabla de módulos y responsabilidades

| Módulo | Única responsabilidad asignada | Por qué no se mezcla con otro |
| :--- | :--- | :--- |
| **`product_db.py`** | Gestión del modelo de datos de productos. | Separa la estructura del dato de la forma en que se lee o filtra. |
| **`db_reader.py`** | Lectura y extracción de datos desde la fuente. | Evita que la lógica de negocio dependa de si los datos vienen de SQL, CSV o JSON. |
| **`detector.py`** | Análisis de imágenes para detectar objetos. | Es una tarea pesada que no debe saber nada de bases de datos o interfaces. |
| **`recommender.py`** | Lógica de recomendaciones de reabastecimiento. | Solo procesa reglas de negocio basadas en números; es puramente lógico. |
| **`stock_predictor.py`** | Cálculo de proyecciones de stock futuro. | Utiliza modelos matemáticos independientes de la interfaz de usuario. |
| **`demoStreamlit.py`** | Renderizado de la interfaz de usuario (UI). | Su misión es mostrar datos; no debe contener cálculos ni consultas directas. |

## 8.2.3 — Inventario de uso de IA

| Archivo | Prompt principal utilizado | Cambios realizados por ti |
| :--- | :--- | :--- |
| **`stock_predictor.py`** | "Genera una función en Python para predecir stock usando una media móvil simple basada en una lista de ventas." | Integré la función dentro de la estructura de clases del proyecto y añadí manejo de excepciones para listas vacías. |
| **`test_stock_predictor.py`** | "Crea tests unitarios con pytest para una función de predicción de stock que recibe [parámetros]." | Ajusté los paths de importación y añadí un `fixture` para los datos de prueba comunes. |
| **`demoStreamlit.py`** | "Crea una interfaz básica en Streamlit con un sidebar para filtrar por categoría y una tabla de resultados." | Personalicé el diseño visual (CSS), añadí el logo de la empresa y conecté los selectores con los servicios reales de database. |
| **`ci.yml`** | "Configura un workflow de GitHub Actions para ejecutar pytest en versiones de Python 3.12 y 3.14." | Corregí las dependencias de sistema necesarias para que la librería de visión (OpenCV/PIL) se instalara correctamente en el runner. |

## 8.2.4 — ¿Qué fallo ocurrió en la matriz de versiones Python?
Al observar tu estructura de archivos, se ven archivos compilados .pyc para Python 3.12 y Python 3.14.

El fallo común en este escenario es la incompatibilidad de librerías en versiones experimentales (3.14). Muchas librerías de ciencia de datos o visión artificial (como OpenCV o NumPy) no tienen "wheels" (binarios) estables para versiones de Python tan recientes antes de su lanzamiento oficial definitivo. Esto provoca que el pipeline de CI/CD falle al intentar compilar estas librerías desde el código fuente si faltan dependencias de C++ en el entorno.

## 8.2.5 — ¿Cuándo decidiste NO usar la IA y por qué?
Decidí no usar la IA en los siguientes archivos:

- .gitignore: Lo configuré manualmente. Las IA suelen incluir demasiadas reglas genéricas; yo preferí especificar solo lo que mi proyecto generaba (como .pytest_cache y los .pyc de las versiones 3.12/3.14).

- LICENSE: Se eligió una licencia específica basada en requisitos legales del proyecto que no deben ser delegados a una generación aleatoria.

- requirements.txt: Se redactó a mano tras realizar las pruebas locales para asegurar que las versiones de las librerías fueran exactamente las que hacían que el código funcionara sin conflictos entre la 3.12 y la 3.14.

- Estructura de carpetas: El diseño de la arquitectura (separar services de routes) fue una decisión de diseño arquitectónico humana para asegurar que el proyecto cumpliera con el estándar de la empresa, evitando la estructura a veces "plana" o inconsistente que propone la IA.