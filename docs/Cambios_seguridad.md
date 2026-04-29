# 🛡️ Registro de Cambios de Seguridad (Refactorización)
Este documento detalla las mejoras de seguridad implementadas tras el análisis estático de código realizado el 28 de abril de 2026. Se han corregido vulnerabilidades críticas detectadas por la herramienta Bandit.

## 1. Desactivación del Modo Depuración (Flask Debug Mode)
Archivo: app.py

- Cambio: Se cambió debug=True a debug=False.

- Justificación: El modo debug de Flask activa una consola interactiva en caso de error que permite la ejecución de código arbitrario (RCE) en el servidor. En un entorno de producción o compartido, esto es una vulnerabilidad de severidad Alta (B201).

## 2. Generación Segura de Escenarios
Archivo: services/vision/detector.py

 - Cambio: Sustitución de la librería random por secrets.

 - Justificación: La librería estándar random es predecible (pseudo-aleatoria). Aunque en un simulador de inventario el riesgo es bajo, se implementó secrets.choice() para cumplir con los estándares de seguridad CWE-330 (B311), asegurando que la selección de escenarios sea criptográficamente fuerte.

## 3. Mitigación de Exposición de Interfaz (Nota)
Archivo: app.py

 - Configuración: host='0.0.0.0'

 - Observación: Se mantiene el bind a todas las interfaces para permitir el acceso desde contenedores (Docker) o máquinas virtuales en el laboratorio, pero se recomienda cambiar a 127.0.0.1 en entornos de desarrollo locales estrictos para evitar accesos no autorizados desde la red local (B104).