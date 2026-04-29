# 🏪 MODULO_4_MARKETTALENTO

Sistema inteligente de análisis y gestión de inventario con capacidades de visión artificial, predicción de demanda y recomendaciones automáticas.

---

## 📁 Estructura del Proyecto

```
MODULO_4_MARKETTALENTO/
├── .github/
│   └── workflows/
│       └── CI.yml                  # Pipeline de integración continua
├── docs/                           # Documentación del proyecto
│   ├── arquitectura.md
│   ├── Cambios_seguridad.md
│   ├── Fase1_cambios_database.md
│   ├── Fase2_cambios_vision.md
│   ├── Fase3_cambios_inventory.md
│   ├── Fase4_cambios_prediction.md
│   ├── Fase5_InicioSreamlit.md
│   ├── Final.md
│   └── Identificar_Estructura.md
├── Heredado/                       # Código heredado de versiones anteriores
│   ├── EndPoint_Api.py
│   └── InventarioAlfa.py
├── interface/                      # Interfaces Streamlit
│   ├── demoStreamlit.py
│   └── demoStreamlitV1.py
├── Memoria Final/
│   └── Memoria Final.md
├── routes/                         # Rutas de la API
│   ├── __init__.py
│   └── api_routes.py
├── services/                       # Lógica de negocio
│   ├── database/                   # Capa de datos
│   │   ├── __init__.py
│   │   ├── db_filter.py
│   │   ├── db_reader.py
│   │   └── product_db.py
│   ├── inventory/                  # Gestión de inventario
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── recommender.py
│   │   └── valuation.py
│   ├── prediction/                 # Predicción de demanda
│   │   ├── __init__.py
│   │   ├── demand_analyzer.py
│   │   └── stock_predictor.py
│   └── vision/                    # Visión artificial
│       ├── __init__.py
│       ├── detector.py
│       └── scenario_loader.py
├── static/                         # Archivos estáticos
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── templates/
│   └── index.html
├── tests/                          # Suite de pruebas
│   ├── routes/
│   │   └── test_api_routes.py
│   └── services/
│       ├── database/
│       │   ├── test_db_filter.py
│       │   ├── test_db_reader.py
│       │   └── test_product_db.py
│       ├── inventory/
│       │   ├── test_metrics.py
│       │   ├── test_recommender.py
│       │   └── test_valuation.py
│       ├── prediction/
│       │   ├── test_demand_analyzer.py
│       │   └── test_stock_predictor.py
│       └── vision/
│           ├── test_detector.py
│           └── test_scenario_loader.py
├── app.py                          # Punto de entrada principal
├── conftest.py                     # Configuración de pytest
├── Inventario.md
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🚀 Características Principales

- **📊 Gestión de Base de Datos**: Lectura, filtrado y consulta de productos desde la capa de datos.
- **📦 Inventario Inteligente**: Cálculo de métricas, valoración y recomendaciones automáticas de reposición.
- **🔮 Predicción de Demanda**: Análisis de demanda histórica y predicción de stock futuro.
- **👁️ Visión Artificial**: Detección de productos y carga de escenarios visuales.
- **🌐 API REST**: Endpoints estructurados con FastAPI para integración externa.
- **🖥️ Interfaz Streamlit**: Dashboard interactivo para visualización y control.
- **✅ Testing Completo**: Suite de pruebas unitarias para todos los módulos.
- **⚙️ CI/CD**: Pipeline automatizado con GitHub Actions.

---

## 🛠️ Instalación

### Prerrequisitos

- Python 3.10, 3.11, 3.12
- pip

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/MODULO_4_MARKETTALENTO.git
   cd MODULO_4_MARKETTALENTO
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Uso

### Iniciar la API

```bash
python app.py
```

La API estará disponible en `http://localhost:8000`.

### Iniciar la interfaz Streamlit

```bash
streamlit run interface/demoStreamlit.py
```

---

## 🧪 Tests

Ejecutar la suite completa de pruebas:

```bash
pytest
```

Con reporte de cobertura:

```bash
pytest --cov=services --cov=routes --cov-report=term-missing
```

Ejecutar tests de un módulo concreto:

```bash
pytest tests/services/inventory/
pytest tests/services/prediction/
pytest tests/services/vision/
```

---

## 📡 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET`  | `/`      | Página principal |
| `GET`  | `/api/products` | Listado de productos |
| `GET`  | `/api/inventory/metrics` | Métricas de inventario |
| `GET`  | `/api/inventory/recommendations` | Recomendaciones de reposición |
| `GET`  | `/api/prediction/demand` | Análisis de demanda |
| `GET`  | `/api/prediction/stock` | Predicción de stock |
| `POST` | `/api/vision/detect` | Detección de productos por imagen |

> Consulta la documentación interactiva en `http://localhost:8000/docs` tras iniciar la aplicación.

---

## 🧩 Módulos

### 🗄️ Database (`services/database/`)

| Archivo | Descripción |
|---------|-------------|
| `db_reader.py` | Lectura y carga de datos desde la base de datos |
| `db_filter.py` | Filtrado y consultas avanzadas |
| `product_db.py` | Modelo y operaciones CRUD de productos |

### 📦 Inventory (`services/inventory/`)

| Archivo | Descripción |
|---------|-------------|
| `metrics.py` | Cálculo de métricas de inventario (rotación, valor, etc.) |
| `recommender.py` | Motor de recomendaciones de reposición |
| `valuation.py` | Valoración económica del inventario |

### 🔮 Prediction (`services/prediction/`)

| Archivo | Descripción |
|---------|-------------|
| `demand_analyzer.py` | Análisis histórico de demanda |
| `stock_predictor.py` | Predicción de niveles de stock futuros |

### 👁️ Vision (`services/vision/`)

| Archivo | Descripción |
|---------|-------------|
| `detector.py` | Detección de productos mediante visión artificial |
| `scenario_loader.py` | Carga y gestión de escenarios visuales |

---

## 📄 Documentación

La carpeta `docs/` contiene la documentación de cada fase del desarrollo:

- **Fase 1** — Cambios en base de datos
- **Fase 2** — Integración de visión artificial
- **Fase 3** — Módulo de inventario
- **Fase 4** — Sistema de predicción
- **Fase 5** — Inicio con Streamlit
- **Arquitectura** — Diseño general del sistema
- **Cambios de seguridad** — Medidas de seguridad implementadas

---

## 🔄 CI/CD

El pipeline de GitHub Actions (`.github/workflows/CI.yml`) ejecuta automáticamente:

1. Instalación de dependencias
2. Análisis de cobertura de tests
3. Validación de estilo de código

---

## 📋 Requisitos

Ver [`requirements.txt`](requirements.txt) para la lista completa de dependencias.

---

## 📝 Licencia

Este proyecto está bajo la licencia especificada en el archivo [`LICENSE`](LICENSE).

---

## 👥 Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y añade tests
4. Asegúrate de que todos los tests pasan (`pytest`)
5. Abre un Pull Request describiendo los cambios