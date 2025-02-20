from enum import Enum



class Gravedad:
    """Gravedad estándar en metros por segundo al cuadrado."""
    ESTANDAR = 9.80665

class ConvertidorPresion:
    """Convierte entre unidades de Pascal y Bar."""
    COEFICIENTE = 100000

    @staticmethod
    def pascal_a_bar(pascales: float) -> float:
        """Convierte pascales a bares."""
        return pascales / ConvertidorPresion.COEFICIENTE

    @staticmethod
    def bar_a_pascal(bares: float) -> float:
        """Convierte bares a pascales."""
        return bares * ConvertidorPresion.COEFICIENTE

class PresionAltitud:
    """Calcula la presión a una determinada altitud y viceversa."""
    PRESION_ESTANDAR = 1.01325  # Presión estándar en bares
    PASCAL_ESTANDAR = ConvertidorPresion.bar_a_pascal(PRESION_ESTANDAR)
    
    CONSTANTE_GAS = 8.31432  # J/(mol·K) para aire
    TEMPERATURA = 288.15  # Kelvin (15°C)
    TASA_ENFRIAMIENTO = -0.0065  # Kelvin/metro
    MASA_MOLAR = 0.0289644  # kg/mol
    
    EXPONENTE = (Gravedad.ESTANDAR * MASA_MOLAR) / (CONSTANTE_GAS * TASA_ENFRIAMIENTO)
    EXPONENTE_INVERSO = 1 / EXPONENTE

    @staticmethod
    def presion(altitud: float) -> float:
        """Calcula la presión a una altitud dada en pascales."""
        base = PresionAltitud.TEMPERATURA / (PresionAltitud.TEMPERATURA + PresionAltitud.TASA_ENFRIAMIENTO * altitud)
        return PresionAltitud.PASCAL_ESTANDAR * (base ** PresionAltitud.EXPONENTE)

    @staticmethod
    def altitud(presion_bares: float) -> float:
        presion_pascales = ConvertidorPresion.bar_a_pascal(presion_bares) 
        presion_normalizada = presion_pascales / PresionAltitud.PASCAL_ESTANDAR
        base = presion_normalizada ** PresionAltitud.EXPONENTE_INVERSO
        return (PresionAltitud.TEMPERATURA / base  - PresionAltitud.TEMPERATURA) / PresionAltitud.TASA_ENFRIAMIENTO
