from pyscuba.physics.depth_converter import DepthConverter
from pyscuba.gases.gas_mixtures import GasMixtures
import math




class NitroxCalculator:
    def __init__(self, depth_converter: DepthConverter, o2_in_air: float = GasMixtures.o2_in_air):
        self.depth_converter = depth_converter
        self.o2_in_air = o2_in_air

    def ead(self, percent_O2: float, depth: float) -> float:
        """
        Calcula la profundidad equivalente de aire para una mezcla nitrox dada.

        :param percent_O2: Porcentaje de oxígeno en el gas.
        :param depth: Profundidad actual en metros.
        :return: Profundidad equivalente de aire en metros.
        """
        fO2 = percent_O2 / 100
        bars = self.depth_converter.to_bar(depth)
        result = GasMixtures.ead(fO2, bars, self.o2_in_air)

        if result <= self.depth_converter.surface_pressure:
            return 0

        result_meters = self.depth_converter.from_bar(result)
        return result_meters

    def best_mix(self, pO2: float, depth: float) -> float:
        """
        Calcula la mejor mezcla nitrox para una profundidad dada.

        :param pO2: Presión parcial constante.
        :param depth: Profundidad actual en metros.
        :return: Porcentaje de oxígeno en la mezcla requerida.
        """
        result = GasMixtures.best_mix(pO2, depth, self.depth_converter) * 100
        return result

    def mod(self, ppO2: float, percent_O2: float) -> float:
        """
        Calcula la profundidad máxima operativa para una mezcla dada.

        :param ppO2: Presión parcial constante.
        :param percent_O2: Porcentaje de oxígeno en el gas.
        :return: Profundidad en metros.
        """
        fO2 = percent_O2 / 100
        result = GasMixtures.mod(ppO2, fO2)
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
