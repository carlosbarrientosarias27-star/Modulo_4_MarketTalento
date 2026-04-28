# services/database/db_filter.py 
from .product_db import product_database

def get_sales_history(product_name, days=20):
    product = product_database.get(product_name)
    if product:
        return product["historial_ventas"][-days:] if days > 0 else product["historial_ventas"]
    return []

def get_by_category(category):
    return [p for p in product_database.values() if p["categoria"] == category]