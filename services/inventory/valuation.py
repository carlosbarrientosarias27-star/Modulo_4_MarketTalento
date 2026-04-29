# services/inventory/valuation.py
def calculate_inventory_value(detected_products, all_products_list):
    total_value = 0
    # Creamos mapeo Nombre -> Precio
    price_map = {p['nombre']: p['precio'] for p in all_products_list}
    
    for detected in detected_products:
        precio = price_map.get(detected["nombre"])
        if precio is not None:
            total_value += detected["cantidad"] * precio
            
    return round(total_value, 2)

