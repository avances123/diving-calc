from pyscuba.presion import Gravedad, ConvertidorPresion, PresionAltitud
from enum import Enum

class Salinidad(Enum):
    """Tipos de densidad de agua salina utilizados para distinguir conversores de profundidad."""
    DULCE = 1      # 1000 kg/m3
    SALOBRE = 2    # EN13319 - 1020 kg/m3
    SALADA = 3     # 1030 kg/m3

class Densidad:
    """Valores de densidad del agua en condiciones estándar."""
    DULCE = 1000     # 1000 kg/m3 a 0C / 32F
    SALOBRE = 1020   # EN13319 - 1020 kg/m3 a 0C / 32F
    SALADA = 1030    # 1030 kg/m3 a 0C / 32F

class ConvertidorProfundidad:
    """Convierte entre profundidad y presión absoluta en agua según el tipo de salinidad."""

    def __init__(self, densidad: float, altitud: float):
        # Calculamos la presión superficial en pascales a partir de la altitud proporcionada
        presion_en_pascales = PresionAltitud.presion(altitud)
        self._presion_superficial = ConvertidorPresion.pascal_a_bar(presion_en_pascales)
        self._gravedad = Gravedad.ESTANDAR
        self.densidad = densidad

    @property
    def presion_superficial(self):
        return self._presion_superficial

    @staticmethod
    def para_agua_salada(altitud: float = 0):
        """Crea una nueva instancia del convertidor de profundidad para agua salada."""
        return ConvertidorProfundidad(Densidad.SALADA, altitud)

    @staticmethod
    def para_agua_salobre(altitud: float = 0):
        """Crea una nueva instancia del convertidor de profundidad para agua salobre."""
        return ConvertidorProfundidad(Densidad.SALOBRE, altitud)

    @staticmethod
    def para_agua_dulce(altitud: float = 0):
        """Crea una nueva instancia del convertidor de profundidad para agua dulce."""
        return ConvertidorProfundidad(Densidad.DULCE, altitud)

    @staticmethod
    def simple():
        """Crea una nueva instancia del convertidor de profundidad para agua dulce con gravedad estándar de 10 m/s²."""
        convertidor = ConvertidorProfundidad(Densidad.DULCE, 0)
        convertidor._presion_superficial = 1
        convertidor._gravedad = 10
        return convertidor

    def a_bar(self, profundidad: float) -> float:
        """Calcula la presión absoluta en bares para una profundidad dada (en metros)."""
        densidad_peso = self.densidad * self._gravedad
        return ConvertidorPresion.pascal_a_bar(profundidad * densidad_peso) + self._presion_superficial

    def desde_bar(self, bares: float) -> float:
        """Calcula la profundidad (en metros) a partir de la presión (en bares)."""
        if bares < self._presion_superficial:
            raise ValueError('La presion es mas baja que la altitud, no se puede convertir a profundidad.')
        
        densidad_peso = self.densidad * self._gravedad
        presion = ConvertidorPresion.bar_a_pascal(bares - self._presion_superficial)
        return presion / densidad_peso


class FabricaConvertidorProfundidad:
    """Crea instancias de convertidores de profundidad según el tipo de salinidad."""

    def __init__(self, altitud: float, salinidad: Salinidad):
        self.opciones = {'altitud': altitud, 'salinidad': salinidad}

    def crear(self):
        """Crea una nueva instancia de convertidor de profundidad según la salinidad proporcionada."""
        if self.opciones['salinidad'] == Salinidad.SALADA:
            return ConvertidorProfundidad.para_agua_salada(self.opciones['altitud'])
        elif self.opciones['salinidad'] == Salinidad.SALOBRE:
            return ConvertidorProfundidad.para_agua_salobre(self.opciones['altitud'])
        else:
            return ConvertidorProfundidad.para_agua_dulce(self.opciones['altitud'])


# Ejemplo de uso
if __name__ == "__main__":
    altitud = 0  # A nivel del mar
    salinidad = Salinidad.SALADA  # Agua salada

    # Crear un convertidor de profundidad para agua salada
    convertidor = FabricaConvertidorProfundidad(altitud, salinidad).crear()

    # Calcular la presión en 10 metros de profundidad
    profundidad = 10
    presion = convertidor.a_bar(profundidad)
    print(f'La presion a {profundidad} metros de profundidad es {presion} bares.')

    # Calcular la profundidad para una presión de 2 bares
    presion_a_convertir = 2
    profundidad_calculada = convertidor.desde_bar(presion_a_convertir)
    print(f'La profundidad correspondiente a {presion_a_convertir} bares es {profundidad_calculada} metros.')
