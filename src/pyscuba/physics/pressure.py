from enum import Enum


class Salinity(Enum):
    # 1000 kg/m3
    fresh = 1
    # EN13319 - 1020 kg/m3
    brackish = 2
    # 1030 kg/m3
    salt = 3


class Density:
    """
    1000kg / m3 at 0C / 32F (standard conditions for measurements).
    """
    fresh = 1000

    """
    Brackish water density EN13319 - 1020kg / m3 at 0C / 32F (standard conditions for measurements).
    """
    brackish = 1020

    """
    1030kg / m3 at 0C / 32F (standard conditions for measurements).
    """
    salt = 1030


class Gravity:
    """
    Standard gravity sample rates in meters per second per second (m/s2)
    """
    standard = 9.80665


class PressureConverter:
    coefficient = 100000 # 100000 pascals = 1 bar.

    @staticmethod
    def pascal_to_bar(pascals):
        """
        Calculates the pascal to bar derived unit. 100000 pascals = 1 bar.
        
        :param pascals: The pascal SI derived unit.
        :return: Bar derived unit of pressure from pascal.
        """
        return pascals / PressureConverter.coefficient

    @staticmethod
    def bar_to_pascals(bars):
        """
        Calculates the bar to pascal derived unit. 100000 pascals = 1 bar.
        
        :param bars: The bar derived unit.
        :return: Pascal derived unit of pressure from bars.
        """
        return bars * PressureConverter.coefficient


class AltitudePressure:
    standard = 1.01325
    standard_pascals = PressureConverter.bar_to_pascals(standard)

    # Constants for the barometric formula
    gas_constant = 8.31432  # J/(mol·K) for air
    temperature = 288.15  # kelvin = 15°C
    laps_rate = -0.0065  # kelvin/meter
    molar_mass = 0.0289644  # kg/mol
    exponent = (Gravity.standard * molar_mass) / (gas_constant * laps_rate)
    inverted_exponent = 1 / exponent

    @staticmethod
    def pressure(altitude):
        """
        Calculates pressure at altitude in pascals
        
        :param altitude: Positive number in meters representing the altitude
        :return: The pressure in pascals at the given altitude
        """
        base = AltitudePressure.temperature / (AltitudePressure.temperature + AltitudePressure.laps_rate * altitude)
        return AltitudePressure.standard_pascals * base ** AltitudePressure.exponent

    @staticmethod
    def altitude(pressure):
        """
        Returns altitude in meters calculated from atmospheric pressure.
        Returns 0 if pressure is lower than standard pressure.

        :param pressure: The pressure in pascals.
        :return: The calculated altitude in meters.
        """
        if pressure >= AltitudePressure.standard_pascals:
            return 0

        pressure_normalized = pressure / AltitudePressure.standard_pascals
        base = pressure_normalized ** AltitudePressure.inverted_exponent
        return (AltitudePressure.temperature / base - AltitudePressure.temperature) / AltitudePressure.laps_rate
