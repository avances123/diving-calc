import pytest
from diving_calc.gases.gas import Gas  # Asegúrate de que el nombre del archivo de la clase sea gas_module.py

# Testando la clase Gas

@pytest.mark.parametrize("o2, he, expected_n2", [
    (0.21, 0, 0.79),  # Caso común con O2 = 21%, He = 0
    (0.3, 0.1, 0.6),  # Caso con mezcla de O2 = 30% y He = 10%
    (0.18, 0.02, 0.8), # Caso con mezcla baja de O2 = 18% y He = 2%
])
def test_post_init(o2, he, expected_n2):
    gas = Gas(o2=o2, he=he)
    assert gas.n2 == pytest.approx(expected_n2, rel=1e-2)

@pytest.mark.parametrize("o2, he, expected_str", [
    (1.0, 0, "Oxigeno 100%"),
    (0.21, 0, "Aire"),
    (0.32, 0, "Nitrox 32"),
    (0.3, 0.1, "Helitrox 30/10"),
    (0.21, 0.2, "Helitrox 21/20")
])
def test_str(o2, he, expected_str):
    gas = Gas(o2=o2, he=he)
    assert gas.__str__() == expected_str

@pytest.mark.parametrize("ppO2, o2, expected_depth", [
    (1.0, 0.21, 4.76),  # Caso con una presión parcial de O2 de 1 atm
    (1.4, 0.21, 6.67),  # Caso con presión parcial de O2 de 1.4 atm
    (0.8, 0.32, 2.5)    # Caso con O2 al 32%
])
def test_mod(ppO2, o2, expected_depth):
    gas = Gas(o2=o2, he=0)
    assert gas.mod(ppO2) == pytest.approx(expected_depth, rel=1e-2)

@pytest.mark.parametrize("o2, expected_narcotic_index", [
    (0.21, 1.0),  # Aire (N2 + O2)
    (0.32, 1.0),  # Nitrox
])
def test_narcotic_index(o2, expected_narcotic_index):
    gas = Gas(o2=o2, he=0)
    assert gas.narcotic_index() == pytest.approx(expected_narcotic_index, rel=1e-2)

@pytest.mark.parametrize("o2, surface_pressure, expected_ceiling", [
    (0.21, 1, 1),   # Aire hay 1 bar de presion en la superficie, puedo respirar a 1 bar de profundiad(desde la superficie)
    (0.14, 1, 1.2857),     # Trimix con 14% de o2 puedo empezar a respirar a partir de 1.3 bar ~ -3m
    (0.14, 0.8, 1.028),     # Trimix con 14% en altura , tengo que tener esta presion para pasar a metros hay que calcularlos con altura
])
def test_ceiling(o2, surface_pressure, expected_ceiling):
    gas = Gas(o2=o2, he=0)
    assert gas.ceiling(surface_pressure) == pytest.approx(expected_ceiling, rel=1e-2)


@pytest.mark.parametrize("current_depth, expected_end", [
    (5, 2.75),   # a 40m con 45% de helio me sale una end de 17.5m
    (4, 2.2),   # a 30m con 45% de helio me sale una end de 12.5m
])
def test_end(current_depth, expected_end):
    gas = Gas(o2=0.21, he=0.45)
    assert gas.end(current_depth) == pytest.approx(expected_end, rel=1e-2)

@pytest.mark.parametrize("depth, expected_ead", [
    (5, 4.3),  # Caso típico para EAD
    (4, 3.44)  # Caso típico para EAD
])
def test_ead(depth, expected_ead):
    gas = Gas(o2=0.32, he=0)
    assert gas.ead(depth) == pytest.approx(expected_ead, rel=1e-2)

@pytest.mark.parametrize("abs_pressure, volume_fraction, expected_partial_pressure", [
    (1, 0.21, 0.21),  # Aire
    (2, 0.32, 0.64),  # Nitrox
    (3, 0.5, 1.5),    # Oxígeno puro
])
def test_partial_pressure(abs_pressure, volume_fraction, expected_partial_pressure):
    assert Gas.partial_pressure(abs_pressure, volume_fraction) == pytest.approx(expected_partial_pressure, rel=1e-2)
