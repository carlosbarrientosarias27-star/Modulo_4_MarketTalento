# services/database/product_db.py 

product_database = {
    # --- CATEGORÍA: Refrigerados (Frío) ---
    "Leche Entera": {
        "id": "PROD001", "nombre": "Leche Entera", "categoria": "Refrigerados",
        "precio": 1.20, "unidad": "litro", "stock_minimo": 5,
        "stock_maximo": 30, "tiempo_reposicion": 2,
        "historial_ventas": [3, 4, 5, 2, 6, 4, 5, 3, 4, 6, 5, 4, 3, 5, 4, 6, 3, 5, 4, 5]
    },
    "Yogur Natural": {
        "id": "PROD002", "nombre": "Yogur Natural", "categoria": "Refrigerados",
        "precio": 0.55, "unidad": "unidad", "stock_minimo": 8,
        "stock_maximo": 60, "tiempo_reposicion": 2,
        "historial_ventas": [10, 12, 11, 14, 15, 13, 12, 11, 10, 14, 12, 11, 10, 13, 11, 12, 10, 11, 12, 13]
    },
    "Queso Fresco": {
        "id": "PROD003", "nombre": "Queso Fresco", "categoria": "Refrigerados",
        "precio": 2.80, "unidad": "unidad", "stock_minimo": 4,
        "stock_maximo": 20, "tiempo_reposicion": 3,
        "historial_ventas": [2, 3, 2, 1, 4, 3, 2, 2, 3, 2, 1, 3, 2, 4, 2, 3, 1, 2, 3, 2]
    },
    "Mantequilla": {
        "id": "PROD004", "nombre": "Mantequilla", "categoria": "Refrigerados",
        "precio": 1.95, "unidad": "tarrina", "stock_minimo": 4,
        "stock_maximo": 25, "tiempo_reposicion": 4,
        "historial_ventas": [1, 2, 2, 3, 2, 1, 2, 2, 3, 1, 2, 2, 1, 3, 2, 1, 2, 2, 1, 3]
    },
    "Fiambre Pavo": {
        "id": "PROD005", "nombre": "Fiambre Pavo", "categoria": "Refrigerados",
        "precio": 3.50, "unidad": "paquete", "stock_minimo": 3,
        "stock_maximo": 18, "tiempo_reposicion": 2,
        "historial_ventas": [2, 4, 3, 2, 3, 4, 2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 2, 4, 3, 2]
    },
    "Crema de Leche": {
        "id": "PROD006", "nombre": "Crema de Leche", "categoria": "Refrigerados",
        "precio": 0.90, "unidad": "brik", "stock_minimo": 5,
        "stock_maximo": 35, "tiempo_reposicion": 3,
        "historial_ventas": [4, 5, 4, 6, 5, 4, 5, 4, 6, 5, 4, 5, 4, 6, 5, 4, 5, 4, 6, 5]
    },
    "Huevos M": {
        "id": "PROD007", "nombre": "Huevos M", "categoria": "Refrigerados",
        "precio": 2.50, "unidad": "docena", "stock_minimo": 3,
        "stock_maximo": 20, "tiempo_reposicion": 1,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 4, 2, 3, 2, 4, 3, 2, 3, 2, 4]
    },

    # --- CATEGORÍA: CONSERVAS ---
    "Atún en Aceite": {
        "id": "PROD008", "nombre": "Atún en Aceite", "categoria": "Conservas",
        "precio": 1.60, "unidad": "lata", "stock_minimo": 10,
        "stock_maximo": 80, "tiempo_reposicion": 7,
        "historial_ventas": [5, 7, 6, 8, 5, 7, 6, 5, 8, 7, 6, 5, 7, 6, 8, 5, 7, 6, 5, 8]
    },
    "Tomate Triturado": {
        "id": "PROD009", "nombre": "Tomate Triturado", "categoria": "Conservas",
        "precio": 0.75, "unidad": "bote", "stock_minimo": 12,
        "stock_maximo": 100, "tiempo_reposicion": 7,
        "historial_ventas": [10, 11, 12, 10, 13, 11, 12, 10, 11, 12, 10, 13, 11, 12, 10, 11, 12, 10, 13, 11]
    },
    "Judías Blancas": {
        "id": "PROD010", "nombre": "Judías Blancas", "categoria": "Conservas",
        "precio": 1.10, "unidad": "bote", "stock_minimo": 8,
        "stock_maximo": 60, "tiempo_reposicion": 7,
        "historial_ventas": [4, 5, 4, 6, 4, 5, 4, 6, 4, 5, 4, 6, 4, 5, 4, 6, 4, 5, 4, 6]
    },
    "Aceitunas Verdes": {
        "id": "PROD011", "nombre": "Aceitunas Verdes", "categoria": "Conservas",
        "precio": 1.40, "unidad": "bote", "stock_minimo": 6,
        "stock_maximo": 50, "tiempo_reposicion": 10,
        "historial_ventas": [3, 4, 3, 5, 3, 4, 3, 5, 3, 4, 3, 5, 3, 4, 3, 5, 3, 4, 3, 5]
    },
    "Sardinas en Aceite": {
        "id": "PROD012", "nombre": "Sardinas en Aceite", "categoria": "Conservas",
        "precio": 1.80, "unidad": "lata", "stock_minimo": 8,
        "stock_maximo": 60, "tiempo_reposicion": 7,
        "historial_ventas": [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3]
    },
    "Maíz Dulce": {
        "id": "PROD013", "nombre": "Maíz Dulce", "categoria": "Conservas",
        "precio": 0.95, "unidad": "lata", "stock_minimo": 6,
        "stock_maximo": 50, "tiempo_reposicion": 7,
        "historial_ventas": [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5]
    },

    # --- CATEGORÍA: Bebidas ---
    "Agua Mineral": {
        "id": "PROD014", "nombre": "Agua Mineral", "categoria": "Bebidas",
        "precio": 0.60, "unidad": "botella", "stock_minimo": 15,
        "stock_maximo": 100, "tiempo_reposicion": 3,
        "historial_ventas": [10, 12, 11, 9, 13, 10, 12, 11, 10, 14, 12, 11, 10, 13, 11, 12, 10, 11, 12, 13]
    },
    "Café Molido": {
        "id": "PROD015", "nombre": "Café Molido", "categoria": "Bebidas",
        "precio": 4.50, "unidad": "paquete", "stock_minimo": 3,
        "stock_maximo": 25, "tiempo_reposicion": 5,
        "historial_ventas": [1, 2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 3]
    },
    "Zumo de Naranja UHT": {
        "id": "PROD016", "nombre": "Zumo de Naranja UHT", "categoria": "Bebidas",
        "precio": 1.35, "unidad": "brik", "stock_minimo": 8,
        "stock_maximo": 60, "tiempo_reposicion": 5,
        "historial_ventas": [5, 6, 5, 7, 5, 6, 5, 7, 5, 6, 5, 7, 5, 6, 5, 7, 5, 6, 5, 7]
    },
    "Refresco Cola": {
        "id": "PROD017", "nombre": "Refresco Cola", "categoria": "Bebidas",
        "precio": 1.20, "unidad": "lata", "stock_minimo": 10,
        "stock_maximo": 80, "tiempo_reposicion": 4,
        "historial_ventas": [8, 10, 9, 11, 8, 10, 9, 11, 8, 10, 9, 11, 8, 10, 9, 11, 8, 10, 9, 11]
    },
    "Cerveza 1905": {
        "id": "PROD018", "nombre": "Cerveza 1905", "categoria": "Bebidas",
        "precio": 1.10, "unidad": "botella", "stock_minimo": 6,
        "stock_maximo": 50, "tiempo_reposicion": 5,
        "historial_ventas": [6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9]
    },

    # --- CATEGORÍA: Panadería ---
    "Pan de Molde": {
        "id": "PROD019", "nombre": "Pan de Molde", "categoria": "Panadería",
        "precio": 1.40, "unidad": "paquete", "stock_minimo": 10,
        "stock_maximo": 50, "tiempo_reposicion": 1,
        "historial_ventas": [4, 5, 4, 6, 5, 4, 5, 4, 6, 5, 4, 5, 4, 6, 5, 4, 5, 4, 6, 5]
    },
    "Baguette": {
        "id": "PROD020", "nombre": "Baguette", "categoria": "Panadería",
        "precio": 0.90, "unidad": "unidad", "stock_minimo": 12,
        "stock_maximo": 60, "tiempo_reposicion": 1,
        "historial_ventas": [15, 18, 16, 20, 15, 18, 16, 20, 15, 18, 16, 20, 15, 18, 16, 20, 15, 18, 16, 20]
    },
    "Croissant": {
        "id": "PROD021", "nombre": "Croissant", "categoria": "Panadería",
        "precio": 0.75, "unidad": "unidad", "stock_minimo": 8,
        "stock_maximo": 40, "tiempo_reposicion": 1,
        "historial_ventas": [6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9, 6, 8, 7, 9]
    },

    # --- CATEGORÍA: Despensa / Alimentos Básiccos ---
    "Arroz": {
        "id": "PROD022", "nombre": "Arroz", "categoria": "Alimentos Básicos",
        "precio": 1.80, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 60, "tiempo_reposicion": 4,
        "historial_ventas": [3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 5, 3, 4, 3, 5, 4, 3, 4, 3, 5]
    },
    "Aceite de Oliva": {
        "id": "PROD023", "nombre": "Aceite de Oliva", "categoria": "Despensa",
        "precio": 4.20, "unidad": "litro", "stock_minimo": 8,
        "stock_maximo": 40, "tiempo_reposicion": 4,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 2, 4, 3, 2, 3, 2, 4, 3, 2, 3, 4, 2, 3]
    },
    "Azúcar": {
        "id": "PROD024", "nombre": "Azúcar", "categoria": "Alimentos Básicos",
        "precio": 1.50, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 50, "tiempo_reposicion": 3,
        "historial_ventas": [4, 5, 4, 6, 5, 4, 5, 6, 4, 5, 6, 4, 5, 4, 6, 5, 4, 5, 4, 6]
    },
    "Harina de Trigo": {
        "id": "PROD025", "nombre": "Harina de Trigo", "categoria": "Alimentos Básicos",
        "precio": 1.20, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 60, "tiempo_reposicion": 3,
        "historial_ventas": [3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 5, 3, 4, 3, 5, 4, 3, 4, 3, 5]
    },

    # --- PRODUCTOS ORIGINALES RESTANTES ---
    "Galletas": {
        "id": "PROD026", "nombre": "Galletas", "categoria": "Snacks",
        "precio": 2.30, "unidad": "paquete", "stock_minimo": 12,
        "stock_maximo": 45, "tiempo_reposicion": 2,
        "historial_ventas": [5, 6, 5, 7, 6, 5, 6, 7, 5, 6, 7, 5, 6, 5, 7, 6, 5, 6, 5, 7]
    },
    "Cereal": {
        "id": "PROD027", "nombre": "Cereal", "categoria": "Desayuno",
        "precio": 3.80, "unidad": "caja", "stock_minimo": 6,
        "stock_maximo": 30, "tiempo_reposicion": 5,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 4, 2, 3, 2, 4, 3, 2, 3, 2, 4]
    }
}
