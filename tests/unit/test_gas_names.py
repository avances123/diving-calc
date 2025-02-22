import pytest
from diving_calc.gases.gas_names import GasNames

# Test para la mezcla de aire
def test_air_name():
    assert GasNames.name_for(0.21) == 'Air'

# Test para oxígeno puro
def test_oxygen_name():
    assert GasNames.name_for(1.0) == 'Oxygen'

# Test para una mezcla EAN (enriched air nitrox) con 32% de oxígeno
def test_ean32():
    assert GasNames.name_for(0.32) == 'EAN32'

# Test para una mezcla Helitrox con 32% de oxígeno y 50% de helio
def test_helitrox():
    assert GasNames.name_for(0.32, 0.50) == 'Helitrox 32/50'

# Test para una mezcla Trimix con 18% de oxígeno y 50% de helio
def test_trimix():
    assert GasNames.name_for(0.18, 0.50) == 'Trimix 18/50'

# Test para una mezcla Trimix con 18% de oxígeno y 0% de helio
def test_trimix_no_helium():
    assert GasNames.name_for(0.18, 0) == 'EAN18'

# Test para un gas sin oxígeno ni helio
def test_no_oxygen_or_helium():
    assert GasNames.name_for(0, 0) == ''

# Test para mezcla de oxígeno al 100%
def test_pure_oxygen():
    assert GasNames.name_for(1.0, 0) == 'Oxygen'

# Test para un gas con fracción de helio igual a cero
def test_gas_with_no_helium():
    assert GasNames.name_for(0.21, 0) == 'Air'

