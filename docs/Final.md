# Memoria Final de Reestructuración de Software

## 1. Diagnóstico Inicial: ¿Qué estaba mal?
El proyecto original, ubicado en la carpeta Heredado/, presentaba los síntomas clásicos de un "Big Ball of Mud" (Gran Bola de Lodo):

- Acoplamiento Excesivo: Los archivos como InventarioAlfa.py mezclaban lógica de acceso a datos, cálculos de negocio y, probablemente, interacción con el usuario.
- Dificultad de Testing: Era imposible probar el algoritmo de predicción sin instanciar la base de datos o cargar modelos de visión.
- Fragilidad: Un cambio en la estructura de los datos (DB) rompía directamente la interfaz de usuario.
- Código Muerto y Duplicidad: Los archivos .pyc en control de versiones y múltiples versiones del mismo script (demoStreamlitV1.py) indicaban falta de un flujo de trabajo limpio.

## 2. La Transformación: ¿Qué se cambió y por qué?
Se implementó una Arquitectura Modular por Dominios de Servicio. A continuación, los pilares del cambio:

### A. Desacoplamiento de Servicios
Se dividió la lógica en cuatro servicios independientes bajo la carpeta services/:

- Database: Capa de abstracción de datos. Si mañana cambias SQL por NoSQL, solo modificas este módulo.
- Vision: Aísla las dependencias pesadas de procesamiento de imágenes.
- Inventory: Lógica pura de negocio (valoración, métricas). Es el "corazón" del sistema.
- Prediction: Encapsula la complejidad estadística y de ML.

### B. Inversión de Control y Rutas
Se introdujo routes/api_routes.py para actuar como el orquestador. La lógica no vive en la interfaz (Streamlit), sino que la interfaz consume los servicios a través de rutas definidas, permitiendo que el sistema sea multiplataforma.

### C. Infraestructura de Calidad (Testing y CI/CD)
Se creó una suite de pruebas en tests/ que espeja la estructura de servicios.

- Beneficio: Permite identificar exactamente qué módulo falló tras un cambio.
- CI/CD: El archivo CI.yml automatiza la validación en cada subida.

## 3. Matriz de Uso de IA y Herramientas
En el desarrollo moderno, la IA no solo escribe código, sino que asiste en la refactorización.

HerramientaUso EspecíficoFase del ProyectoQodo (Codium)Generación de tests unitarios y análisis de calidad de código.Fase 3 y 4 (Calidad)GitHub Copilot / GeminiRefactorización de scripts legados a clases modulares.Fase 1 y 2 (Estructura)PytestEjecución de pruebas y generación de reportes de cobertura (.coverage).Todas las fasesStreamlitPrototipado rápido de la interfaz de usuario.Fase 5 (Presentación)


## 4. Reflexión: La Matriz de Versiones y Entornos
Un detalle crítico en tu estructura es la coexistencia de archivos compilados para distintas versiones de Python (e.g., cpython-312 y cpython-314 en __pycache__).

### ¿Por qué es importante esta observación?

- Inconsistencia de Entorno: La presencia de versiones 3.14 (que es experimental/futura en el contexto de 2024-25) frente a 3.12 sugiere que el proyecto ha pasado por diferentes entornos de ejecución sin una limpieza de caché.
- Riesgo de Despliegue: En producción, estas discrepancias pueden causar errores de segmentación o fallos inesperados si no se estandariza el requirements.txt.
- Lección Aprendida: La arquitectura modular protege la lógica, pero el entorno (Virtualenvs/Docker) protege la ejecución. Se recomienda limpiar los __pycache__ e ignorarlos siempre en el .gitignore.

## 5. ¿Hubo alguna versión Python donde los tests fallaron y en otras no? ¿Por qué? 

En entornos de integración continua, es común que los tests fallen en versiones más recientes (como Python 3.12) mientras pasan en las anteriores (3.10 o 3.11).

### ¿Por qué ocurre? 
Generalmente se debe a la eliminación de módulos obsoletos (deprecated). Por ejemplo, en Python 3.12 se eliminaron definitivamente módulos como distutils, que muchas librerías antiguas usaban. Si el código o sus dependencias no se han actualizado, el test fallará solo en esa versión específica.

- Estado actual: Según la imagen que compartes, todas las versiones (3.10, 3.11 y 3.12) han pasado con éxito (indicado por el check verde ✅), lo que significa que el código es compatible con todo el espectro probado.

## 6. ¿Qué dependencia del requirements.txt causó problemas con alguna versión? 

Aunque no puedo ver tu archivo requirements.txt directamente, históricamente hay un "sospechoso habitual" en las transiciones a versiones recientes de Python:

- Setuptools / Wheel: Si las dependencias no están fijadas con versiones exactas, una actualización en las herramientas de empaquetado puede romper el build.

- Librerías de C (como psycopg2 o pandas): Estas suelen fallar en versiones nuevas de Python si no hay un "binary wheel" disponible todavía para esa versión específica, obligando al sistema a compilar desde el código fuente, lo cual suele fallar si faltan librerías del sistema.

## 7. ¿Cuál es la ventaja de usar fail-fast: false en un equipo de desarrollo?

En la configuración de una matriz de pruebas (como la de la imagen), la opción fail-fast: false es una estrategia clave para la productividad del equipo:

- Visibilidad Completa: Si un test falla en Python 3.10 pero el fail-fast está en true, GitHub detendría inmediatamente los tests de 3.11 y 3.12. Al ponerlo en false, permites que todos los jobs terminen.

- Diagnóstico preciso: Te permite saber si un error es general (falla en todas las versiones) o específico (solo falla en 3.12).

- Ahorro de tiempo: El desarrollador recibe toda la información de una sola vez. No tiene que arreglar un fallo, volver a subir el código y esperar a ver si la siguiente versión de Python también tiene problemas.