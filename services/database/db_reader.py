#services/database/db_reader.py
from .product_db import product_database

def get_product_info(product_name):
    return product_database.get(product_name, None)

def get_all_products():
    return list(product_database.values())