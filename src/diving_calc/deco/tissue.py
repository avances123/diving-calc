from diving_calc.deco.compartment import Compartment, CompartmentsZHL16
from diving_calc.physics.pressure_converter import AltitudePressure
from diving_calc.gases.gas import Gas
from dataclasses import dataclass

DEFAULT_COMPARTMENT = Compartment(5.0, 1.1696, 0.5578, 1.88, 1.6189, 0.4770)


@dataclass
class Tissue():
    compartment: Compartment = DEFAULT_COMPARTMENT # si no me dan el compartimento, pillo el 1 del listado
    surface_pressure: float = 1 #AltitudePressure.STANDARD_PRESSURE
    p_n2: float = 0 # Current partial pressure of nitrogen saturated in the compartment in bars.
    p_he: float = 0 # Current partial pressure of helium saturated in the compartment in bars.
    a: float = 0 # Buhlmann a mValue coefficient.
    b: float = 0 # Buhlmann b mValue coefficient.

    def __post_init__(self):
        self.p_n2 = Tissue.inspired_n2_pressure(self.surface_pressure)
        self.update_coefficients()
    
    def update_coefficients(self):
        self.a = ((self.compartment.n2_a * self.p_n2) + (self.compartment.he_a * self.p_he)) / (self.p_total)
        self.b = ((self.compartment.n2_b * self.p_n2) + (self.compartment.he_b * self.p_he)) / (self.p_total)

    def m_value(self, pressure: float) -> float:
        """Returns m-value for the tissue at the given pressure (surface or ambient)."""
        return self.a + pressure / self.b
    
    def gradient_factor(self, ambient_pressure: float) -> float:
        """
        Returns the gradient factor from the original Buhlmann M-value for the tissue 
        at the given pressure.
        The returned number is always greater or equal to 0.
        @param ambientPressure in bars (e.g. surface or ambient).
        """
        surface_m_value = self.m_value(ambient_pressure)
        result = (self.p_total - ambient_pressure) / (surface_m_value - ambient_pressure)
        return max(0, result)

    def saturation_ratio(self, ambient_pressure: float) -> float:
        if(self.p_total < ambient_pressure):
            return self.p_total / ambient_pressure - 1
        return self.gradient_factor(ambient_pressure)
    
             

    @property
    def p_total(self) -> float:
        return self.p_n2 + self.p_he


    @staticmethod
    def inspired_n2_pressure(surface_pressure: float) -> float:
        pressure = Tissue.pressure_in_lungs(surface_pressure)
        p_n2 = Gas.partial_pressure(pressure, Gas.N2_IN_AIR)
        return p_n2

    @staticmethod
    def pressure_in_lungs(ambient_pressure: float) -> float:
        """ Constante para la presión de vapor de agua a 37°C (en bares). """
        water_vapour_pressure = 0.0627
        return ambient_pressure - water_vapour_pressure

class Tissues(list):
    def __init__(self):
        tissues = [Tissue(i) for i in CompartmentsZHL16()]
        super().__init__(tissues)

    # TODO crear los tissues a partir de otros loadtissues para un buceo repetitivo





