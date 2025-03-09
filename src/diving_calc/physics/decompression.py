import numpy as np


def schreiner_equation(Pio, R, t, k, Po):
    """
    schreiner_equation

    Calcula la presión de gas inerte en un tejido usando la ecuación de Schreiner.

    Parámetros:
    - Pio: Presión parcial inicial del gas inerte en el tejido (bar).
    - R: Tasa de cambio de presión del gas inerte (bar/min).
    - t: Tiempo de inmersión en minutos.
    - k: Constante de desaturación del tejido (min⁻¹).
    - Po: Presión ambiente inicial (bar).

    Retorna:
    - P: Presión parcial del gas inerte en el tejido después del tiempo t.
    """
    return Pio + R * (t - 1/k) - (Pio - Po - R/k) * np.exp(-k * t)

    # Ejemplo de uso
    Pio = 0.79  # Presión parcial inicial del N2 en el cuerpo (bar) (asumiendo aire: 0.79 * 1 bar)
    R = 3.0 / 10  # Cambio de presión en bar/min (ejemplo: 30m/min ≈ 3 bar/min)
    t = 2  # Tiempo de descenso en minutos
    k = np.log(2) / 5  # Constante de desaturación para un tejido con T1/2 = 5 min
    Po = 1.0  # Presión ambiente inicial (bar)

    P = schreiner_equation(Pio, R, t, k, Po)
    print(f"Presión parcial del gas inerte después del descenso: {P:.3f} bar")
        
    
def pressure_in_lungs(ambient_pressure: float) -> float:
    """ Constante para la presión de vapor de agua a 37°C (en bares). """
    water_vapour_pressure = 0.0627
    return ambient_pressure - water_vapour_pressure