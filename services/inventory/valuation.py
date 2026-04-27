# services/inventory/valuation.py
def calculate_inventory_value(detected_products, product_database):
    total_value = 0
    for detected in detected_products:
        product_info = product_database.get(detected["nombre"])
        if product_info and "precio" in product_info:
            total_value += detected["cantidad"] * product_info["precio"]
    return round(total_value, 2)

