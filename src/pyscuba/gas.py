from dataclasses import dataclass, field
from pyscuba.presion import PresionAltitud, Gravedad, ConvertidorPresion
from pyscuba.profundidad import Densidad
from enum import Enum


@dataclass
class Gas:
    o2: float
    he: float = 0
    n2: float = None
    
    def __post_init__(self):
        if self.n2 is None:  # Si no se proporciona, calcularlo
            self.n2 = 100 - self.o2 - self.he
        
        total = self.o2 + self.n2 + self.he
        if not (0 <= self.o2 <= 100):
            raise ValueError(f"El porcentaje de O2 ({self.o2}%) debe estar entre 0 y 100")
        if not (0 <= self.n2 <= 100):
            raise ValueError(f"El porcentaje de N2 ({self.n2}%) debe estar entre 0 y 100")
        if not (0 <= self.he <= 100):
            raise ValueError(f"El porcentaje de He ({self.he}%) debe estar entre 0 y 100")
        if total != 100:
            raise ValueError(f"La suma de los gases ({total}%) debe ser exactamente 100%")

    def __repr__(self):
        simple_o2_in_air = 21
        
        # Redondeo de los valores
        percent_o2 = int(self.o2)
        percent_he = int(self.he)
 
        if percent_he == 0:
            # Evita overflow de best gas
            if percent_o2 == 100:
                return 'Oxígeno'
 
            if percent_o2 == simple_o2_in_air:
                return 'Aire'
 
            return f"Nitrox {percent_o2}"
 
        prefix = "Helitrox" if percent_o2 >= simple_o2_in_air else "Trimix"
        return f"{prefix} {percent_o2}/{percent_he}"
 
    def mod(self, ppO2) -> int:
        return ppO2 / (self.o2 / 100) # divido el 1.4 por 0.21
        
        

