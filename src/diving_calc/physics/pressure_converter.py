from math import pow


class Density:
    """
    Water density values at standard conditions (0°C / 32°F).
    """
    FRESH = 1000.0  # 1000 kg/m3
    BRACKISH = 1020.0  # EN13319 - 1020 kg/m3
    SALT = 1030.0  # 1030 kg/m3

class Gravity:
    """
    Standard gravity in meters per second squared (m/s^2).
    """
    STANDARD = 9.80665

class PressureConverter:

    @staticmethod
    def pascal_to_bar(pascals: float) -> float:
        return pascals / 100000.0

    @staticmethod
    def bar_to_pascal(bars: float) -> float:
        return bars * 100000.0


    @staticmethod
    def bar_to_atm(bars: float) -> float:
        return bars * 0.986923

    @staticmethod
    def atm_to_bar(atm: float) -> float:
        return atm * 1.01325

    @staticmethod
    def pascal_to_atm(pascals: float) -> float:
        return PressureConverter.bar_to_atm(PressureConverter.pascal_to_bar(pascals))

    @staticmethod
    def atm_to_pascal(atm: float) -> float:
        return PressureConverter.bar_to_pascal(PressureConverter.atm_to_bar(atm))



class AltitudePressure:
    """
    Atmospheric pressure calculations based on altitude.
    """
    STANDARD_PRESSURE = 1.01325  # Standard pressure in bars
    STANDARD_PASCALS = PressureConverter.bar_to_pascal(STANDARD_PRESSURE)

    # Constants from barometric formula
    GAS_CONSTANT = 8.31432  # J/(mol·K) for air
    TEMPERATURE = 288.15  # Kelvin = 15°C
    LAPSE_RATE = -0.0065  # Kelvin per meter
    MOLAR_MASS = 0.0289644  # kg/mol

    EXPONENT = (Gravity.STANDARD * MOLAR_MASS) / (GAS_CONSTANT * LAPSE_RATE)
    INVERTED_EXPONENT = 1 / EXPONENT

    @staticmethod
    def pressure(altitude: float) -> float:
        """Calculates pressure at a given altitude in pascals."""
        base = AltitudePressure.TEMPERATURE / (AltitudePressure.TEMPERATURE + AltitudePressure.LAPSE_RATE * altitude)
        return AltitudePressure.STANDARD_PASCALS * pow(base, AltitudePressure.EXPONENT)

    @staticmethod
    def altitude(pressure: float) -> float:
        """Returns altitude in meters based on atmospheric pressure."""
        if pressure >= AltitudePressure.STANDARD_PASCALS:
            return 0
        
        pressure_normalized = pressure / AltitudePressure.STANDARD_PASCALS
        base = pow(pressure_normalized, AltitudePressure.INVERTED_EXPONENT)
        return (AltitudePressure.TEMPERATURE / base - AltitudePressure.TEMPERATURE) / AltitudePressure.LAPSE_RATE
