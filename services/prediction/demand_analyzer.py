# services/prediction/demand_analyzer.py

def calculate_daily_demand(sales_history):
    """Calcula la demanda diaria ajustada por tendencias recientes."""
    if not sales_history: 
        return 0
    
    # 1. Promedio general de ventas
    avg_daily_sales = sum(sales_history) / len(sales_history)
    
    # 2. Ajuste por tendencia si hay suficientes datos (últimos 5 días)
    if len(sales_history) >= 5:
        recent_avg = sum(sales_history[-5:]) / 5
        trend_factor = recent_avg / avg_daily_sales if avg_daily_sales > 0 else 1
        return avg_daily_sales * trend_factor
    
    return avg_daily_sales