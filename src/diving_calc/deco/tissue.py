from diving_calc.deco.compartment import Compartment, CompartmentsZHL16
from diving_calc.physics.pressure_converter import AltitudePressure
from diving_calc.gases.gas import Gas
from dataclasses import dataclass
from diving_calc.physics.decompression import schreiner_equation, pressure_in_lungs
import numpy as np
from rich import print
import logging
from rich.logging import RichHandler
from typing import Optional


# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,  # Establecer el nivel de logging a DEBUG
    format="%(message)s",  # Formato simple
    handlers=[RichHandler()]
)

# Crear un logger
logger = logging.getLogger("rich")
logger.setLevel(logging.INFO)





DEFAULT_COMPARTMENT = Compartment(5.0, 1.1696, 0.5578, 1.88, 1.6189, 0.4770)

class Tissues(list):
    def __init__(self):
        tissues = [Tissue(i) for i in CompartmentsZHL16()]
        super().__init__(tissues)


@dataclass
class Tissue():
    compartment: Compartment = DEFAULT_COMPARTMENT # si no me dan el compartimento, pillo el 1 del listado
    surface_pressure: float = 1 #AltitudePressure.STANDARD_PRESSURE
    p_n2: float = 0 # Current partial pressure of nitrogen saturated in the compartment in bars.
    p_he: float = 0 # Current partial pressure of helium saturated in the compartment in bars.
    a: float = 0 # Buhlmann a mValue coefficient.
    b: float = 0 # Buhlmann b mValue coefficient.

    @property
    def p_total(self) -> float:
        return self.p_n2 + self.p_he

    def m_value(self, pressure: float) -> float:
        """Returns m-value for the tissue at the given pressure (surface or ambient)."""
        return self.a + pressure / self.b

    def __post_init__(self):
        pressure = pressure_in_lungs(self.surface_pressure)
        self.p_n2 = Gas.partial_pressure(pressure, Gas.N2_IN_AIR)
        self.update_coefficients()
    
    def update_coefficients(self):
        """Para ponderar la cantidad de N2 y He"""
        self.a = ((self.compartment.n2_a * self.p_n2) + (self.compartment.he_a * self.p_he)) / (self.p_total)
        self.b = ((self.compartment.n2_b * self.p_n2) + (self.compartment.he_b * self.p_he)) / (self.p_total)
        self.a *= 0.70
        self.b *= 0.30

        
    def ceiling(self) -> float:
        """Returns the ceiling pressure for this tissue."""
        return (self.p_total - self.a) * self.b



    def presion_tejido(self, presion_ambiente: float, tiempo: float, ratio_descenso: float = 0.0, 
                    f_gas: float = 0.79, half_time: float = None, presion_inicial_tejido: float = 0.0) -> float:
        """
        Calcula la presión parcial de un gas inerte en el tejido usando la ecuación de Schreiner.

        Parámetros:
        - presion_ambiente: Presión ambiente actual (bar).
        - tiempo: Tiempo de exposición (minutos).
        - ratio_descenso: Tasa de cambio de presión (bar/min), 0 si es constante.
        - f_gas: Fracción del gas inerte en la mezcla (ej. 0.79 para N2 en aire, 0.0 si no aplica).
        - half_time: Tiempo medio de saturación del gas en el tejido (min).
        - presion_inicial_tejido: Presión inicial del gas en el tejido (bar).

        Retorna:
        - p_gas: Presión parcial del gas en el tejido después del tiempo dado.
        """
        if half_time is None:
            raise ValueError("Debe proporcionar el tiempo medio de saturación (half_time).")
        
        Pio_gas = pressure_in_lungs(presion_ambiente) * f_gas
        R_gas = ratio_descenso * f_gas
        k = np.log(2) / half_time
        p_gas = schreiner_equation(Pio_gas, R_gas, tiempo, k, presion_inicial_tejido)
        
        return p_gas



    def actualizar(self,presion_inicial: float, tiempo: float, presion_final: float = 0.0):
        # Calculo ratio_descenso
        ratio_descenso = (presion_final - presion_inicial) / tiempo

        if (ratio_descenso > 0):
            logger.debug(f"Bajando de {presion_inicial} bar a {presion_final} bar con un ratio de {ratio_descenso} bar/min")
        elif (ratio_descenso < 0):
            logger.debug(f"Subiendo de {presion_inicial} bar a {presion_final} bar con un ratio de {ratio_descenso} bar/min")

        # Para N2
        self.p_n2 = self.presion_tejido(presion_inicial, tiempo, ratio_descenso, 
                                f_gas=0.79, half_time=self.compartment.n2_half_time, 
                                presion_inicial_tejido=self.p_n2)

        # Para He (en caso de Trimix)
        self.p_he = self.presion_tejido(presion_inicial, tiempo, ratio_descenso, 
                                f_gas=0.0, half_time=self.compartment.he_half_time, 
                                presion_inicial_tejido=self.p_he)

        self.update_coefficients()



if __name__ == "__main__":
    x = Tissue()
    x.actualizar(4,30,4)

