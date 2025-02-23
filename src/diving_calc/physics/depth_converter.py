
from diving_calc.physics.pressure_converter import Density, Gravity, AltitudePressure, PressureConverter


class DepthConverter:
    def __init__(self, density: float, altitude: float):
        """
        Necesitamos:
        Densidad del agua en kg/m3
        Fuerza de la gravedad en m/s2
        Altitud en m
        """
        self.density = density
        self.altitude = altitude
        self._gravity = Gravity.STANDARD
        self._surface_pressure = PressureConverter.pascal_to_bar(AltitudePressure.pressure(altitude))

    @property
    def surface_pressure(self) -> float:
        """ Devuelve la presion en bares de la altitud a la que estemos"""
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

    def to_atm(self, depth: float) -> float:
        """Calculates absolute pressure (in atm) for given depth in meters."""
        return PressureConverter.bar_to_atm(self.to_bar(depth))

    def from_bar(self, bars: float) -> float:
        """Calculates depth (in meters) from given atmospheric pressure in bars."""
        if bars < self._surface_pressure:
            raise ValueError("Lower pressure than altitude isn't convertible to depth.")

        weight_density = self.density * self._gravity
        pressure = PressureConverter.bar_to_pascal(bars - self._surface_pressure)
        return pressure / weight_density
        
    def depth_at_altitude(self, depth: float): # in fact, is depth at sea level
        """Devuelve la profundidad como si estuvieras a nivel del mar"""
        ratio = AltitudePressure.STANDARD_PRESSURE / self._surface_pressure
        target_depth = depth * ratio
        return target_depth