import pytest
from diving_calc.gases.gas_mixtures import GasMixtures
from diving_calc.physics.depth_converter import DepthConverter
from diving_calc.physics.pressure_converter import Density


@pytest.fixture
def depth_converter():
    return DepthConverter(Density.SALT, 0) # density and altitude in meters

def test_partial_pressure():
    abs_pressure = 3.0  # Pressure in bars
    volume_fraction = 0.21  # Fraction of oxygen in the mixture
    result = GasMixtures.partial_pressure(abs_pressure, volume_fraction)
    
    assert result == pytest.approx(0.63, abs=1e-2)


def test_mod():
    ppO2 = 1.4  # Partial pressure of oxygen
    fO2 = 0.21  # Fraction of oxygen in the gas
    result = GasMixtures.mod(ppO2, fO2)
    
    assert result == pytest.approx(6.666, abs=1e-2) # ¬ 57m air mod


def test_best_mix(depth_converter):
    pO2 = 1.4  # Partial pressure of oxygen
    depth = 30  # Depth in meters
    result = GasMixtures.best_mix(pO2, depth, depth_converter)
    
    assert result == pytest.approx(0.35, abs=1e-2)


def test_ead():
    # https://en.wikipedia.org/wiki/Equivalent_air_depth#Calculations_in_metres
    fO2 = 0.36  # Fraction of oxygen in the gas mixture
    depth = 2.7  # Depth in bars
    result = GasMixtures.ead(fO2, depth)
    
    assert result == pytest.approx(2.18, abs=1e-2)


def test_ead_meters(depth_converter):
    # https://en.wikipedia.org/wiki/Equivalent_air_depth#Calculations_in_metres
    fO2 = 0.36  # Fraction of oxygen in the gas mixture
    depth = depth_converter.to_bar(27) # 27
    bar = GasMixtures.ead(fO2, depth)
    depth = depth_converter.from_bar(bar) # 19.93
    
    assert depth == pytest.approx(19.93, abs=1e-2) # 20 in theory but due to rounding errors it is 19.93

def test_end():
    current_depth = 4  # Depth in bars
    fN2 = 0.79  # Fraction of nitrogen in the gas mixture
    fO2 = 0.21  # Fraction of oxygen in the gas mixture
    result = GasMixtures.end(current_depth, fN2, fO2)
    
    assert result == pytest.approx(4, abs=1e-2)


def test_end_trimix():
    current_depth = 4  # Depth in bars
    fN2 = 0.39  # Fraction of nitrogen in the gas mixture
    fO2 = 0.21  # Fraction of oxygen in the gas mixture
    result = GasMixtures.end(current_depth, fN2, fO2)
    
    assert result == pytest.approx(2.4, abs=1e-2)

def test_mnd():
    narcotic_depth = 30  # END in bars
    fN2 = 0.39  # Fraction of nitrogen in the gas mixture
    fO2 = 0  # Fraction of oxygen in the gas mixture
    result = GasMixtures.mnd(narcotic_depth, fN2, fO2)
    
    assert result == pytest.approx(76.92, abs=1e-2)


def test_ceiling():
    fO2 = 0.12  # Fraction of oxygen in the gas mixture
    surface_pressure = 1.0  # Surface pressure in bars
    result = GasMixtures.ceiling(fO2, surface_pressure)
    
    assert result == pytest.approx(1.5, abs=1e-2) # with 12% o2 trimix, we have to start breathing at ~ 5m


def test_narcotic_index():
    fN2 = 0.79  # Fraction of nitrogen in the gas mixture
    fO2 = 0.21  # Fraction of oxygen in the gas mixture
    result = GasMixtures.narcotic_index(fN2, fO2)
    
    assert result == pytest.approx(1.0, abs=1e-2)