# ============================================================
# codigoInicio.py - SISTEMA DE INVENTARIO INTELIGENTE
# Versión unificada para alumnos - SIN creación automática de archivos
# ============================================================
# Los alumnos deben refactorizar este código en módulos separados
# NO genera archivos automáticamente al ejecutarse
# ============================================================
from flask import Flask
from routes.api_routes import api_bp  # Importamos solo el Blueprint

app = Flask(__name__)

# Registramos el Blueprint para que Flask sepa dónde están las rutas
app.register_blueprint(api_bp)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("📦 SISTEMA DE INVENTARIO INTELIGENTE - VERSIÓN UNIFICADA")
    print("=" * 60)
    print("🌐 Servidor disponible en: http://localhost:5020")
    print("📝 Presiona Ctrl+C para detener")
    print("=" * 60)
    app.run(debug=False, port=5020, host='0.0.0.0', threaded=True) 