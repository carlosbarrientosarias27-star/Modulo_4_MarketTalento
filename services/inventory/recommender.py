# services/inventory/recommender.py

def generate_recommendations(products_needing_attention):
    recommendations = []
    for product in products_needing_attention:
        producto = product["producto"]
        stock_actual = product["stock_actual"]
        stock_minimo = product.get("stock_minimo", 5)
        if stock_actual == 0:
            rec = f"🔄 Reponer urgentemente {producto}. Stock agotado."
        else:
            rec = f"📦 Reponer {stock_minimo * 2 - stock_actual} unidades de {producto}. Stock bajo."
        recommendations.append({"producto": producto, "recomendacion": rec, "prioridad": "ALTA" if stock_actual == 0 else "MEDIA"})
    return recommendations