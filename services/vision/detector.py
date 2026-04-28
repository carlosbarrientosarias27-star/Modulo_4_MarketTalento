#services/vision/detector.py
import secrets
from .scenario_loader import load_scenarios

def detect_products(image_path=None):
    print("📸 Analizando imagen para detección de productos...")
    escenarios = load_scenarios()
    escenario = secrets.choice(escenarios)
    print(f"✅ Detección simulada: {escenario['descripcion']}")
    return escenario 

