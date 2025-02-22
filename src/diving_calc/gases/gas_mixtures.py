from math import pow
from diving_calc.physics.depth_converter import DepthConverter

class GasMixtures:
    # Relative partial pressure of oxygen in air at surface
    o2_in_air = 0.209
    nitrox_in_air = 1 - o2_in_air

    # Defines minimum fraction of oxygen in gas mixture of breathable gas
    min_ppO2 = 0.18

    # Maximum recommended value of equivalent narcotic depth
    max_end = 30

    @staticmethod
    def partial_pressure(abs_pressure: float, volume_fraction: float) -> float:
        """
        Calculates the partial pressure of a gas component from the volume gas fraction and total pressure.
        
        :param abs_pressure: The total pressure P in bars (typically 1 bar of atmospheric pressure + x bars of water pressure).
        :param volume_fraction: The volume fraction of gas component (typically 0.79 for 79%) measured as percentage in decimal.
        :return: The partial pressure of gas component in bar absolute.
        """
        return abs_pressure * volume_fraction

    @staticmethod
    def mod(ppO2: float, fO2: float) -> float:
        """
        Calculates Maximum operation depth for given mix.
        
        :param ppO2: Partial pressure constant.
        :param fO2: Fraction of Oxygen in gas.
        :return: Depth in bars.
        """
        return ppO2 / fO2

    @staticmethod
    def best_mix(pO2: float, depth: float, depth_converter: DepthConverter) -> float:
        """
        Calculates best mix of nitrox gas for given depth.
        
        :param pO2: Partial pressure constant.
        :param depth: Current depth in meters.
        :param depth_converter: Converter used to translate the pressure.
        :return: Fraction of oxygen in required gas (0-1).
        """
        bar = depth_converter.to_bar(depth)
        result = pO2 / bar
        return min(result, 1)

    @staticmethod
    def ead(fO2: float, depth: float, o2_in_air: float = o2_in_air) -> float:
        """
        Calculates equivalent air depth for given nitrox gas mix.
        https://en.wikipedia.org/wiki/Equivalent_air_depth
        
        :param fO2: Fraction of Oxygen in gas mix (0-1).
        :param depth: Current depth in bars.
        :param o2_in_air: Theoretical/default fraction of oxygen content in air.
        :return: Depth in bars. May return pressure lower than surface pressure!
        """
        fN2 = 1 - fO2  # here we are interested only in nitrogen toxicity
        nitrox_in_air = 1 - o2_in_air
        return GasMixtures.end(depth, fN2) / nitrox_in_air

    @staticmethod
    def end(current_depth: float, fN2: float, fO2: float = 0) -> float:
        """
        Calculates equivalent narcotic depth as the depth which would produce the same narcotic effect when breathing air.
        Define which gas (nitrogen or oxygen) is narcotic by setting its part to 0.
        https://en.wikipedia.org/wiki/Equivalent_narcotic_depth
        
        :param current_depth: Current depth in bars for which you want to calculate the end.
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Depth in bars. May return pressure lower than surface pressure!
        """
        narc_index = GasMixtures.narcotic_index(fO2, fN2)
        return current_depth * narc_index

    @staticmethod
    def mnd(narcotic_depth: float, fN2: float, fO2: float = 0) -> float:
        """
        Calculates maximum depth, at which the narcotic effect corresponds to the given narcotic depth.
        Define which gas (nitrogen or oxygen) is narcotic by setting its part to 0.
        Also called maximum narcotic depth.
        
        :param narcotic_depth: END in bars for which you want to calculate the mnd.
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Depth in bars.
        """
        narc_index = GasMixtures.narcotic_index(fO2, fN2)
        return narcotic_depth / narc_index

    @staticmethod
    def ceiling(fO2: float, surface_pressure: float) -> float:
        """
        Calculates minimum depth at which the gas is breathable.
        
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :param surface_pressure: surface pressure in bars.
        :return: Depth in bars.
        """
        ratio = GasMixtures.min_ppO2 / fO2
        bars = ratio * surface_pressure

        # hyperoxic gases have pressure below sea level, which can't be converted to depth
        if bars < surface_pressure:
            return surface_pressure
        return bars

    @staticmethod
    def narcotic_index(fN2: float, fO2: float = 0) -> float:
        """
        Helium has a narcotic factor of 0 while N2 and O2 have a narcotic factor of 1
        
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Narcotic index.
        """
        return fO2 + fN2
