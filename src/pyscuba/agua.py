from dataclasses import dataclass, field

DENSIDADES = {
    "salina": 1030,    
    "salobre": 1020,
    "dulce": 1000,
}

GRAVEDAD = 9.80665 # m/ s^2
LAPS_RATE = -0.0065  # kelvin/meter




@dataclass
class Agua:
    altitud: int = 0
    densidad: int
    temperatura: float = 288.15 # kelvin = 15°C

    @property
    def profundidad_fromBar(self,):

