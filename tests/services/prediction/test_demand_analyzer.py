import pytest
from services.prediction.demand_analyzer import calculate_daily_demand

def test_demanda_diaria_basica():
    """Prueba el cálculo del promedio simple cuando hay pocos datos."""
    historial = [10, 10, 10]
    resultado = calculate_daily_demand(historial)
    # Con 3 datos, solo calcula el promedio simple: (10+10+10)/3 = 10
    assert resultado == 10

def test_demanda_con_tendencia_ascendente():
    """Prueba el ajuste por tendencia cuando las ventas recientes aumentan."""
    # Promedio general: 10
    # Promedio últimos 5 días: 20
    # Factor de tendencia: 20/10 = 2. Resultado esperado: 10 * 2 = 20
    historial = [10, 10, 10, 10, 10, 20, 20, 20, 20, 20]
    resultado = calculate_daily_demand(historial)
    assert resultado == 20

def test_demanda_sin_historial():
    """Prueba que devuelva 0 si la lista de ventas está vacía."""
    resultado = calculate_daily_demand([])
    assert resultado == 0

def test_demanda_un_solo_dia():
    """Prueba el cálculo con un único dato en el historial."""
    resultado = calculate_daily_demand([5])
    assert resultado == 5