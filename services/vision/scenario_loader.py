#services/vision/scenario_loader.py
def load_scenarios():
    return [
        {"descripcion": "Estantería de supermercado - Stock moderado", "productos": [
            {"nombre": "Leche Entera", "cantidad": 8, "confianza": 0.92},
            {"nombre": "Huevos M", "cantidad": 5, "confianza": 0.88},
            {"nombre": "Pan de Molde", "cantidad": 3, "confianza": 0.85},
            {"nombre": "Agua Mineral", "cantidad": 12, "confianza": 0.95},
            {"nombre": "Café Molido", "cantidad": 6, "confianza": 0.90}
        ]},
        {"descripcion": "Almacén de tienda - Stock alto", "productos": [
            {"nombre": "Arroz", "cantidad": 25, "confianza": 0.94},
            {"nombre": "Leche Entera", "cantidad": 18, "confianza": 0.91},
            {"nombre": "Huevos M", "cantidad": 22, "confianza": 0.89},
            {"nombre": "Agua Mineral", "cantidad": 30, "confianza": 0.96},
            {"nombre": "Café Molido", "cantidad": 15, "confianza": 0.87}
        ]},
        {"descripcion": "Nevera comercial - Stock bajo", "productos": [
            {"nombre": "Yogur", "cantidad": 4, "confianza": 0.83},
            {"nombre": "Queso", "cantidad": 2, "confianza": 0.80},
            {"nombre": "Mantequilla", "cantidad": 3, "confianza": 0.82},
            {"nombre": "Zumo", "cantidad": 5, "confianza": 0.86},
            {"nombre": "Fiambre", "cantidad": 1, "confianza": 0.78}
        ]}
    ]