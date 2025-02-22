from enum import Enum
from math import pow
from diving_calc.physics.pressure_converter import Density, Gravity, AltitudePressure, PressureConverter, Salinity

class DepthOptions:
    def __init__(self, altitude: float, salinity: Salinity):
        """Defines depth calculation options."""
        self.altitude = altitude
        self.salinity = salinity

class DepthConverterFactory:
    def __init__(self, options: DepthOptions):
        """Creates a factory instance for depth converters."""
        self.options = options

    def create(self):
        """Creates a new instance of depth converter based on provided salinity."""
        if self.options.salinity == Salinity.SALT:
            return DepthConverter.for_salt_water(self.options.altitude)
        elif self.options.salinity == Salinity.BRACKISH:
            return DepthConverter.for_brackish_water(self.options.altitude)
        else:
            return DepthConverter.for_fresh_water(self.options.altitude)

class DepthConverter:
    def __init__(self, density: float, altitude: float):
        """Initializes depth converter with density and altitude."""
        self.density = density
        self._gravity = Gravity.STANDARD
        pressure_in_pascals = AltitudePressure.pressure(altitude)
        self._surface_pressure = PressureConverter.pascal_to_bar(pressure_in_pascals)

    @property
    def surface_pressure(self) -> float:
        return self._surface_pressure

    @staticmethod
    def for_salt_water(altitude: float = 0) -> "DepthConverter":
        return DepthConverter(Density.SALT, altitude)

    @staticmethod
    def for_brackish_water(altitude: float = 0) -> "DepthConverter":
        return DepthConverter(Density.BRACKISH, altitude)

    @staticmethod
    def for_fresh_water(altitude: float = 0) -> "DepthConverter":
        return DepthConverter(Density.FRESH, altitude)

    @staticmethod
    def simple() -> "DepthConverter":
        """Creates a depth converter configured for training calculations."""
        converter = DepthConverter(Density.FRESH, 0)
        converter._surface_pressure = 1
        converter._gravity = 10
        return converter

    def to_bar(self, depth: float) -> float:
        """Calculates absolute pressure (in bars) for given depth in meters."""
        weight_density = self.density * self._gravity
        return PressureConverter.pascal_to_bar(depth * weight_density) + self._surface_pressure

    def from_bar(self, bars: float) -> float:
        """Calculates depth (in meters) from given atmospheric pressure in bars."""
        if bars < self._surface_pressure:
            raise ValueError("Lower pressure than altitude isn't convertible to depth.")

        weight_density = self.density * self._gravity
        pressure = PressureConverter.bar_to_pascal(bars - self._surface_pressure)
        return pressure / weight_density
