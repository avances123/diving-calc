import pytest
from diving_calc.physics.depth_converter import DepthConverter
from diving_calc.gases.gas import Gas
from diving_calc.calculators.nitrox_calculator import NitroxCalculator  # Asegúrate de que el nombre del archivo sea nitrox_calculator.py

# Parametrizamos diferentes combinaciones de altitud y salinidad
@pytest.mark.parametrize("altitude, density, depth, expected_ead", [
    (0, DepthConverter.for_salt_water(0).density, 10, 12),  # A nivel del mar, agua salada
    (1000, DepthConverter.for_salt_water(1000).density, 20, 24),  # A 1000m, agua salada
    (2000, DepthConverter.for_brackish_water(2000).density, 30, 30),  # A 2000m, agua salobre
    (3000, DepthConverter.for_fresh_water(3000).density, 15, 18),  # A 3000m, agua dulce
])
def test_ead_with_altitude_and_water_type(altitude, density, depth, expected_ead):
    depth_converter = DepthConverter(density=density, altitude=altitude)
    gas = Gas(o2=0.32, he=0)  # Nitrox 32
    calculator = NitroxCalculator(depth_converter=depth_converter)
    assert calculator.ead(gas, depth) == pytest.approx(expected_ead, rel=1e-2)

@pytest.mark.parametrize("altitude, density, pO2, depth, expected_best_mix", [
    (0, DepthConverter.for_salt_water(0).density, 1.4, 10, 0.32),  # A nivel del mar, agua salada
    (1000, DepthConverter.for_salt_water(1000).density, 1.0, 20, 0.5),   # A 1000m, agua salada
    (2000, DepthConverter.for_brackish_water(2000).density, 0.8, 30, 0.32),  # A 2000m, agua salobre
    (3000, DepthConverter.for_fresh_water(3000).density, 1.0, 25, 0.4),  # A 3000m, agua dulce
])
def test_best_mix_with_altitude_and_water_type(altitude, density, pO2, depth, expected_best_mix):
    depth_converter = DepthConverter(density=density, altitude=altitude)
    calculator = NitroxCalculator(depth_converter=depth_converter)
    assert calculator.best_mix(pO2, depth) == pytest.approx(expected_best_mix, rel=1e-2)

@pytest.mark.parametrize("altitude, density, gas_o2, ppO2, depth, expected_mod", [
    (0, DepthConverter.for_salt_water(0).density, 0.32, 1.4, 10, 20),  # A nivel del mar, agua salada
    (1000, DepthConverter.for_salt_water(1000).density, 0.21, 1.4, 20, 10),  # A 1000m, agua salada
    (2000, DepthConverter.for_brackish_water(2000).density, 0.32, 1.4, 30, 20),  # A 2000m, agua salobre
    (3000, DepthConverter.for_fresh_water(3000).density, 0.5, 1.4, 25, 8),    # A 3000m, agua dulce
])
def test_mod_with_altitude_and_water_type(altitude, density, gas_o2, ppO2, depth, expected_mod):
    gas = Gas(o2=gas_o2, he=0)
    depth_converter = DepthConverter(density=density, altitude=altitude)
    calculator = NitroxCalculator(depth_converter=depth_converter)
    assert calculator.mod(gas, ppO2) == pytest.approx(expected_mod, rel=1e-2)