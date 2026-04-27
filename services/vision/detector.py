#services/vision/detector.py
import random
from .scenario_loader import load_scenarios

def detect_products(image_path=None):
    print("📸 Analizando imagen para detección de productos...")
    escenarios = load_scenarios()
    escenario = random.choice(escenarios)
    print(f"✅ Detección simulada: {escenario['descripcion']}")
    return escenario 

