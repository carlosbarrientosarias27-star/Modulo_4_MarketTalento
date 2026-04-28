import pytest
from services.vision.scenario_loader import load_scenarios

def test_load_scenarios_es_lista():
    """Verifica que la función devuelva una lista de escenarios."""
    escenarios = load_scenarios()
    assert isinstance(escenarios, list)
    assert len(escenarios) > 0

def test_load_scenarios_estructura_datos():
    """Verifica que cada escenario tenga una descripción y una lista de productos."""
    escenarios = load_scenarios()
    for escenario in escenarios:
        assert "descripcion" in escenario
        assert "productos" in escenario
        assert isinstance(escenario["productos"], list)

def test_load_scenarios_contenido_productos():
    """Verifica que los productos dentro de los escenarios tengan los campos requeridos."""
    escenarios = load_scenarios()
    # Probamos el primer producto del primer escenario
    primer_producto = escenarios[0]["productos"][0]
    
    assert "nombre" in primer_producto
    assert "cantidad" in primer_producto
    assert "confianza" in primer_producto
    assert isinstance(primer_producto["cantidad"], int)

def test_verificar_escenario_especifico():
    """Verifica la existencia del escenario de stock bajo (Nevera comercial)."""
    escenarios = load_scenarios()
    nombres_escenarios = [e["descripcion"] for e in escenarios]
    
    assert any("Nevera comercial - Stock bajo" in desc for desc in nombres_escenarios)