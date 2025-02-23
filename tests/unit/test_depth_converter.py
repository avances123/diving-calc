import pytest
from diving_calc.physics.depth_converter import DepthConverter



def test_depth_converter_surface_pressure():
    converter = DepthConverter.for_fresh_water(altitude=0)
    assert converter.surface_pressure == pytest.approx(1.01325, abs=1e-2)

def test_depth_converter_to_bar():
    converter = DepthConverter.for_fresh_water(altitude=0)
    pressure = converter.to_bar(10)  # Depth of 10 meters
    assert pressure == pytest.approx(2, abs=1e-2)

def test_depth_converter_from_bar():
    converter = DepthConverter.for_fresh_water(altitude=0)
    depth = converter.from_bar(1.993)  # Should correspond to ~10m depth
    assert depth == pytest.approx(10, abs=1e-2)

def test_depth_converter_from_bar_mountains():
    converter = DepthConverter.for_fresh_water(altitude=1000)
    depth = converter.from_bar(2)  # Should correspond to ~10m depth
    assert depth == pytest.approx(11.22, abs=1e-2)

def test_depth_converter_invalid_from_bar():
    converter = DepthConverter.for_fresh_water(altitude=0)
    with pytest.raises(ValueError, match="Lower pressure than altitude isn't convertible to depth."):
        converter.from_bar(0.5)

def test_depth_converter_from_bar_saline():
    converter = DepthConverter.for_salt_water(altitude=0)
    depth = converter.from_bar(2)  # Should correspond to ~10m depth
    assert depth == pytest.approx(9.76, abs=1e-2)

