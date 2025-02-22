import pytest
import math
from diving_calc.physics.depth_converter import DepthConverter
from diving_calc.gases.gas_mixtures import GasMixtures
from diving_calc.calculators.nitrox_calculator import NitroxCalculator
from diving_calc.physics.pressure_converter import Density


@pytest.fixture
def depth_converter():
    return DepthConverter(Density.SALT, 0) # density and altitude in meters


@pytest.fixture
def nitrox_calculator(depth_converter):
    return NitroxCalculator(depth_converter)


@pytest.mark.parametrize("percent_O2, depth, expected", [
    (32, 30, 24.38),  # Ejemplo típico de Nitrox 32% a 30m
    (36, 25, 18.31),  # Nitrox 36% a 25m
    (21, 40, 39.93),  # Aire normal (O2 21%) a 40m debería dar 40m
    (50, 18, 7.68),  # Nitrox 50% a 18m
])
def test_ead(nitrox_calculator, percent_O2, depth, expected):
    result = nitrox_calculator.ead(percent_O2, depth)
    assert result == pytest.approx(expected, abs=1e-2)


@pytest.mark.parametrize("pO2, depth, expected", [
    (1.4, 30, 34.62),  # Presión parcial de 1.4 a 30m
    (1.6, 21, 51.04),  # Máximo recomendado en recreativo
])
def test_best_mix(nitrox_calculator, pO2, depth, expected):
    result = nitrox_calculator.best_mix(pO2, depth)
    assert result == pytest.approx(expected, abs=1e-2)


@pytest.mark.parametrize("ppO2, percent_O2, expected", [
    (1.4, 32, 33.28),  # MOD con Nitrox 32% es 33.28
    (1.6, 50, 21.64),  # MOD con Nitrox 50% es 21.64
])
def test_mod(nitrox_calculator, ppO2, percent_O2, expected):
    result = nitrox_calculator.mod(ppO2, percent_O2)
    assert result == pytest.approx(expected, abs=1e-2)


@pytest.mark.parametrize("fO2, depth, expected", [
    (32, 30, 1.29),  # Presión parcial de O2 con Nitrox 32% a 30m
    (36, 25, 1.27),  # Presión parcial con Nitrox 36% a 25m
    (50, 21, 1.56),  # Presión parcial con Nitrox 50% a 21m
])
def test_partial_pressure(nitrox_calculator, fO2, depth, expected):
    result = nitrox_calculator.partial_pressure(fO2, depth)
    assert result == pytest.approx(expected, abs=1e-2)