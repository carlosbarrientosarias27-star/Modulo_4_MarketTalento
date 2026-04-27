# services/inventory/metrics.py
from .recommender import generate_recommendations

def calculate_inventory_metrics(detected_products, product_database):
    total_products = len(detected_products)
    total_units = sum(p["cantidad"] for p in detected_products)
    
    critical_products = []
    low_stock_products = []
    adequate_products = []
    
    for detected in detected_products:
        product_name = detected["nombre"]
        current_stock = detected["cantidad"]
        product_info = product_database.get(product_name)
        
        if product_info:
            min_stock = product_info.get("stock_minimo", 5)
            if current_stock == 0:
                critical_products.append({"producto": product_name, "stock_actual": current_stock, "stock_minimo": min_stock, "estado": "AGOTADO ❌"})
            elif current_stock < min_stock:
                low_stock_products.append({"producto": product_name, "stock_actual": current_stock, "stock_minimo": min_stock, "estado": "BAJO ⚠️"})
            else:
                adequate_products.append({"producto": product_name, "stock_actual": current_stock, "stock_minimo": min_stock, "estado": "ADEQUADO ✅"})
    
    return {
        "resumen": {
            "total_productos": total_products,
            "total_unidades": total_units,
            "productos_criticos": len(critical_products),
            "productos_bajos": len(low_stock_products),
            "productos_adecuados": len(adequate_products),
        },
        "recomendaciones": generate_recommendations(critical_products + low_stock_products)
    }