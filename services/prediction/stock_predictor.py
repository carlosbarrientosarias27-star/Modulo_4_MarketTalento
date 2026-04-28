# services/prediction/stock_predictor.py
from .demand_analyzer import calculate_daily_demand

def predict_stock_outage(sales_history, current_stock, product_info=None):
    """Predice cuántos días de vida le quedan al stock actual."""
    
    # Casos borde: sin ventas o sin stock
    if not sales_history or current_stock <= 0:
        return {
            "dias_hasta_agotarse": 0, 
            "cantidad_recomendada": 10, 
            "estado": "AGOTADO" if current_stock <= 0 else "SIN HISTORIAL"
        }
    
    # Invocamos la lógica externa refactorizada
    adjusted_daily = calculate_daily_demand(sales_history)
    
    # Cálculo de días hasta agotarse (máximo 90 días para evitar números infinitos)
    days_until_out = max(0, min(90, round(current_stock / adjusted_daily, 1))) if adjusted_daily > 0 else 999
    
    # Lógica de estados según urgencia
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
        "cantidad_recomendada": round((sum(sales_history)/len(sales_history)) * 10),
        "estado": estado,
        "consumo_promedio_diario": round(adjusted_daily, 2)
    }