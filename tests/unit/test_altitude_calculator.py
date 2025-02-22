import pytest
from diving_calc.calculators.altitude_calculator import AltitudeCalculator
from diving_calc.physics.pressure_converter import PressureConverter, AltitudePressure

def test_theoretical_depth():
    # Test básico para comprobar el cálculo de la profundidad teórica
    calculator = AltitudeCalculator(altitude_depth=20, altitude=300)
    expected_depth = 20 * (AltitudePressure.STANDARD_PRESSURE / calculator.pressure)
    assert calculator.theoretical_depth == pytest.approx(expected_depth, rel=1e-6)

def test_set_altitude():
    # Test para cambiar la altitud y comprobar que se calcula correctamente la presión
    calculator = AltitudeCalculator(altitude_depth=20, altitude=300)
    calculator.altitude = 500
    expected_pressure = calculator.to_pressure(500)
    assert calculator.pressure == pytest.approx(expected_pressure, rel=1e-6)

def test_set_pressure():
    # Test para cambiar la presión y comprobar que se calcula correctamente la altitud
    calculator = AltitudeCalculator(altitude_depth=20, altitude=300)
    calculator.pressure = 2.0  # Ejemplo de presión en bares
    expected_altitude = calculator.to_altitude(2.0)
    assert calculator.altitude == pytest.approx(expected_altitude, rel=1e-6)

def test_altitude_calculator_initialization():
    # Test para comprobar la correcta inicialización de la clase
    calculator = AltitudeCalculator(altitude_depth=30, altitude=400)
    assert calculator.altitude == 400
    assert calculator.altitude_depth == 30
    assert calculator.pressure == pytest.approx(calculator.to_pressure(400), rel=1e-6)

