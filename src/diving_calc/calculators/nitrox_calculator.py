from diving_calc.physics.depth_converter import DepthConverter
from diving_calc.gases.gas import Gas

class NitroxCalculator:
    def __init__(self, depth_converter = DepthConverter.for_salt_water(0), o2_in_air: float = Gas.O2_IN_AIR):
        self.depth_converter = depth_converter
        self.o2_in_air = o2_in_air

    def __repr__(self):
        return f'Nitrox Calculator: Density: {self.depth_converter.density}, Altitude: {self.depth_converter.altitude}'

    def ead(self, gas: Gas, depth: float) -> float:
        """
        Calcula la profundidad equivalente de aire para una mezcla nitrox dada.

        :param percent_O2: Porcentaje de oxígeno en el gas.
        :param depth: Profundidad actual en metros.
        :return: Profundidad equivalente de aire en metros.
        """
        bars = self.depth_converter.to_bar(depth)
        result = gas.ead(bars)

        if result <= self.depth_converter.surface_pressure:
            return 0

        result_meters = self.depth_converter.from_bar(result)
        return result_meters

    def best_mix(self, pO2: float, depth: float) -> float:
        """
        Calcula la mejor mezcla nitrox para una profundidad dada.

        :param pO2: Presión parcial a la que quiero el mix.
        :param depth: Profundidad actual en metros.
        :return: Porcentaje de oxígeno en la mezcla requerida.
        """

        bar = self.depth_converter.to_bar(depth)
        result = pO2 / bar
        return min(result, 1)



    # MOD en metros
    def mod(self, gas: Gas, ppO2: float) -> float:
        """
        Calcula la profundidad máxima operativa en metros para una mezcla dada.

        :param ppO2: Presión parcial constante.
        :param percent_O2: Porcentaje de oxígeno en el gas.
        :return: Profundidad en metros.
        """
        result = gas.mod(ppO2)
        result = self.depth_converter.from_bar(result)
        return result

    def partial_pressure(self, fO2: float, depth: float) -> float:
        """
        Calcula la presión parcial para una mezcla dada a una profundidad determinada.

        :param fO2: Porcentaje de oxígeno en el gas.
        :param depth: Profundidad actual en metros.
        :return: Presión parcial.
        """
        bar = self.depth_converter.to_bar(depth)
        result = GasMixtures.partial_pressure(bar, fO2) / 100
        return result
