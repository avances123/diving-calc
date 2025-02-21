from pyscuba.physics.pressure_converter import AltitudePressure, PressureConverter


class AltitudeCalculator:
    def __init__(self, altitude_depth=20, altitude=300):
        self.altitude_depth = altitude_depth
        self._altitude = altitude
        self._pressure = self.to_pressure(self.altitude)

    @property
    def pressure(self):
        return self._pressure

    @property
    def altitude(self):
        return self._altitude

    @property
    def theoretical_depth(self):
        """Expecting the altitudeDepth to be in fresh water meters."""
        # targeting sea level pressure, because tables are calculated to sea level
        ratio = AltitudePressure.STANDARD_PRESSURE / self.pressure
        target_depth = self.altitude_depth * ratio
        return target_depth

    @pressure.setter
    def pressure(self, new_value):
        self._pressure = new_value
        self._altitude = self.to_altitude(new_value)

    @altitude.setter
    def altitude(self, new_value):
        self._altitude = new_value
        self._pressure = self.to_pressure(new_value)

    def to_altitude(self, pressure):
        pascal_pressure = PressureConverter.bar_to_pascal(pressure)
        return AltitudePressure.altitude(pascal_pressure)

    def to_pressure(self, altitude):
        pressure = AltitudePressure.pressure(altitude)
        return PressureConverter.pascal_to_bar(pressure)
