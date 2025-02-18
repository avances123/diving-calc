class DepthConverter:
    def to_bar(self, depth):
        # Aquí iría la implementación para convertir la profundidad en barras
        return 1 + (depth / 10)  # Este es un ejemplo de conversión, ajusta según sea necesario
        

class GasMixtures:
    # Fracción relativa de oxígeno en el aire a nivel del mar
    o2_in_air = 0.209
    n2_in_air = 1 - o2_in_air

    # Define la fracción mínima de oxígeno en la mezcla de gases respirables
    min_pp_o2 = 0.18

    # Máximo valor recomendado de profundidad narcótica equivalente
    max_end = 30

    @staticmethod
    def partial_pressure(abs_pressure: float, volume_fraction: float) -> float:
        """
        Calcula la presión parcial de un componente de gas a partir de la fracción de volumen del gas y la presión total.
        
        :param abs_pressure: La presión total P en bares (típicamente 1 bar de presión atmosférica + x bares de presión del agua).
        :param volume_fraction: La fracción de volumen del componente de gas (típicamente 0.79 para el 79%) medida como porcentaje en decimal.
        :return: La presión parcial del componente de gas en bares absolutos.
        """
        return abs_pressure * volume_fraction

    @staticmethod
    def mod(pp_o2: float, f_o2: float) -> float:
        """
        Calcula la máxima profundidad operativa para una mezcla dada.
        
        :param pp_o2: Presión parcial constante.
        :param f_o2: Fracción de oxígeno en el gas.
        :return: Profundidad en bares.
        """
        return pp_o2 / f_o2

    @staticmethod
    def best_mix(p_o2: float, depth: float, depth_converter: DepthConverter) -> float:
        """
        Calcula la mejor mezcla de nitrox para una profundidad dada.
        
        :param p_o2: Presión parcial constante.
        :param depth: Profundidad actual en metros.
        :param depth_converter: Convertidor utilizado para traducir la presión.
        :return: Fracción de oxígeno en el gas requerido (0-1).
        """
        bar = depth_converter.to_bar(depth)
        result = p_o2 / bar
        return 1 if result > 1 else result

    @staticmethod
    def ead(f_o2: float, depth: float, o2_in_air: float = o2_in_air) -> float:
        """
        Calcula la profundidad equivalente al aire para una mezcla de nitrox dada.
        
        :param f_o2: Fracción de oxígeno en la mezcla de gas (0-1).
        :param depth: Profundidad actual en bares.
        :param o2_in_air: Fracción teórica o predeterminada de oxígeno en el aire.
        :return: Profundidad en bares. ¡Puede devolver una presión menor que la presión superficial!
        """
        f_n2 = 1 - f_o2  # Aquí solo estamos interesados en la toxicidad del nitrógeno
        n2_in_air = 1 - o2_in_air
        return GasMixtures.end(depth, f_n2) / n2_in_air

    @staticmethod
    def end(current_depth: float, f_n2: float, f_o2: float = 0) -> float:
        """
        Calcula la profundidad narcótica equivalente, que sería la profundidad que produciría el mismo efecto narcótico al respirar aire.
        
        :param current_depth: Profundidad actual en bares para la cual deseas calcular el END.
        :param f_n2: Fracción de nitrógeno en la mezcla de gas (0-1).
        :param f_o2: Fracción de oxígeno en la mezcla de gas (0-1).
        :return: Profundidad en bares. ¡Puede devolver una presión menor que la presión superficial!
        """
        narc_index = GasMixtures.narcotic_index(f_o2, f_n2)
        return current_depth * narc_index

    @staticmethod
    def mnd(narcotic_depth: float, f_n2: float, f_o2: float = 0) -> float:
        """
        Calcula la profundidad máxima, a la cual el efecto narcótico corresponde a la profundidad narcótica dada.
        
        :param narcotic_depth: END en bares para el cual deseas calcular el MND.
        :param f_n2: Fracción de nitrógeno en la mezcla de gas (0-1).
        :param f_o2: Fracción de oxígeno en la mezcla de gas (0-1).
        :return: Profundidad en bares.
        """
        narc_index = GasMixtures.narcotic_index(f_o2, f_n2)
        return narcotic_depth / narc_index

    @staticmethod
    def ceiling(f_o2: float, surface_pressure: float) -> float:
        """
        Calcula la profundidad mínima a la cual el gas es respirable.
        
        :param f_o2: Fracción de oxígeno en la mezcla de gas (0-1).
        :param surface_pressure: Presión superficial en bares.
        :return: Profundidad en bares.
        """
        ratio = GasMixtures.min_pp_o2 / f_o2
        bars = ratio * surface_pressure

        # Los gases hiperóxicos tienen una presión por debajo del nivel del mar, lo cual no se puede convertir a profundidad
        if bars < surface_pressure:
            return surface_pressure

        return bars

    @staticmethod
    def narcotic_index(f_n2: float, f_o2: float = 0) -> float:
        """
        Calcula el índice narcótico, que depende de la fracción de nitrógeno y oxígeno.
        
        :param f_n2: Fracción de nitrógeno en la mezcla de gas (0-1).
        :param f_o2: Fracción de oxígeno en la mezcla de gas (0-1).
        :return: Índice narcótico.
        """
        return f_o2 + f_n2
