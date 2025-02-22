import pytest
from diving_calc.gases.standard_gases import StandardGases, Gas, GasNames

def test_nitrox_names():
    """Test para obtener los nombres de los gases de nitrox."""
    expected_nitrox_names = [
        GasNames.air_name, 'EAN32', 'EAN36', 'EAN38', 'EAN50', GasNames.oxygen_name
    ]
    nitrox_names = StandardGases.nitrox_names()
    assert nitrox_names == expected_nitrox_names, f"Expected {expected_nitrox_names}, got {nitrox_names}"

def test_all_names():
    """Test para obtener todos los nombres de los gases."""
    expected_all_names = [
        GasNames.air_name, 'EAN32', 'EAN36', 'EAN38', 'EAN50', GasNames.oxygen_name,
        'Helitrox 35/25', 'Helitrox 25/25', 'Helitrox 21/35', 'Trimix 18/45', 'Trimix 15/55',
        'Trimix 12/60', 'Trimix 10/70'
    ]
    all_names = StandardGases.all_names()
    assert all_names == expected_all_names, f"Expected {expected_all_names}, got {all_names}"

def test_by_name_nitrox():
    """Test para buscar un gas por su nombre (caso de nitrox)."""
    gas = StandardGases.by_name('EAN32')
    assert gas == StandardGases.ean32, "EAN32 gas not found correctly."

def test_by_name_trimix():
    """Test para buscar un gas por su nombre (caso de trimix)."""
    gas = StandardGases.by_name('Trimix 18/45')
    assert gas == StandardGases.trimix1845, "Trimix 18/45 gas not found correctly."

def test_by_name_invalid():
    """Test para buscar un gas con un nombre no válido."""
    gas = StandardGases.by_name('NonExistentGas')
    assert gas is None, "Non-existent gas should return None."

def test_by_name_regex_ean():
    """Test para la búsqueda por nombre usando expresión regular para EAN."""
    gas = StandardGases.by_name('EAN50')
    assert gas == StandardGases.ean50, "EAN50 gas not found correctly."

def test_by_name_regex_trimix():
    """Test para la búsqueda por nombre usando expresión regular para trimix."""
    gas = StandardGases.by_name('Trimix 10/70')
    assert gas == StandardGases.trimix1070, "Trimix 10/70 gas not found correctly."

def test_by_name_case_insensitive():
    """Test para la búsqueda por nombre sin tener en cuenta mayúsculas/minúsculas."""
    gas = StandardGases.by_name('ean50')
    assert gas == StandardGases.ean50, "EAN50 gas should be found case insensitively."

def test_by_name_empty():
    """Test para búsqueda por un nombre vacío."""
    gas = StandardGases.by_name('')
    assert gas is None, "Empty name should return None."
