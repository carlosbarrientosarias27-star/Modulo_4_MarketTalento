# services/prediction/stock_predictor.py
from .demand_analyzer import calculate_daily_demand

def predict_stock_outage(sales_history, current_stock, product_info=None):
    if not sales_history or current_stock <= 0:
        return {"dias_hasta_agotarse": 0, "cantidad_recomendada": 10, "estado": "AGOTADO" if current_stock <= 0 else "SIN HISTORIAL"}
    
    avg_daily_sales = sum(sales_history) / len(sales_history)
    if len(sales_history) >= 5:
        recent_avg = sum(sales_history[-5:]) / 5
        trend_factor = recent_avg / avg_daily_sales if avg_daily_sales > 0 else 1
        adjusted_daily = avg_daily_sales * trend_factor
    else:
        adjusted_daily = avg_daily_sales
    
    days_until_out = max(0, min(90, round(current_stock / adjusted_daily, 1))) if adjusted_daily > 0 else 999
    
    if days_until_out <= 2:
        estado = "CRÍTICO ⚠️"
    elif days_until_out <= 5:
        estado = "BAJO ⚠️"
    elif days_until_out <= 10:
        estado = "MODERADO ℹ️"
    else:
        estado = "ADEQUADO ✅"
    
    return {
        "dias_hasta_agotarse": days_until_out,
        "cantidad_recomendada": round(avg_daily_sales * 10),
        "estado": estado,
        "consumo_promedio_diario": round(adjusted_daily, 2)
    }