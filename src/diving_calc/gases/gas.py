from dataclasses import dataclass, field



@dataclass
class Gas:
    # Constants
    MIN_PPO2 = 0.18
    O2_IN_AIR = 0.209

    # Atributos
    o2: float
    he: float = 0
    n2: float = field(init=False)

    def __post_init__(self):
        self.n2 = 1 - self.o2 - self.he
        if self.o2 + self.he > 1:
            raise ValueError(f"La suma de O2 ({self.o2}) y He ({self.n2}) debe ser menor que 100, pero es {self.o2 + self.n2}")

    def __str__(self):
        simple_O2_in_air = 21
        percent_O2 = round(self.o2 * 100)
        percent_He = round(self.he * 100)

        if percent_He == 0:
            if percent_O2 == 100:
                return "Oxigeno 100%"

            if percent_O2 == simple_O2_in_air:
                return "Aire"

            return f'Nitrox {percent_O2}'

        prefix = 'Helitrox' if percent_O2 >= simple_O2_in_air else 'Trimix'
        return f'{prefix} {percent_O2}/{percent_He}'

    def mod(self, ppO2: float) -> float:
        """        
        :param ppO2: Partial pressure constant.
        :return: Depth in bars.
        """
        return ppO2 / self.o2


    def narcotic_index(self,o2_narcotic = True) -> float:
        """
        Helium has a narcotic factor of 0 while N2 and O2 have a narcotic factor of 1
        
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Narcotic index.
        """
        return self.o2 * int(o2_narcotic) + self.n2


    def ceiling(self, surface_pressure: float) -> float:
        """
        Para el trimix hipoxico, antes de esta profundidad no puedo respirarlo
        """
        ratio = Gas.MIN_PPO2 / self.o2
        bars = ratio * surface_pressure

        # hyperoxic gases have pressure below sea level, which can't be converted to depth
        if bars < surface_pressure:
            return surface_pressure
        return bars


    def mnd(self, narcotic_depth: float) -> float:
        """
        Calculates maximum depth, at which the narcotic effect corresponds to the given narcotic depth.
        Define which gas (nitrogen or oxygen) is narcotic by setting its part to 0.
        Also called maximum narcotic depth.
        
        :param narcotic_depth: END in bars for which you want to calculate the mnd.
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Depth in bars.
        """
        return narcotic_depth / self.narcotic_index()

   
    def end(self, current_depth: float, o2_narcotic = True) -> float:
        """
        Calculates equivalent narcotic depth as the depth which would produce the same narcotic effect when breathing air.
        Define which gas (nitrogen or oxygen) is narcotic by setting its part to 0.
        https://en.wikipedia.org/wiki/Equivalent_narcotic_depth
        
        :param current_depth: Current depth in bars for which you want to calculate the end.
        :param fN2: Fraction of nitrogen in gas mix (0-1).
        :param fO2: Fraction of oxygen in gas mix (0-1).
        :return: Depth in bars. May return pressure lower than surface pressure!
        """
        return current_depth * self.narcotic_index(o2_narcotic)

    
    def ead(self, depth: float) -> float:
        """
        Calculates equivalent air depth for given nitrox gas mix.
        https://en.wikipedia.org/wiki/Equivalent_air_depth

        Profundidad en bares
        No puedo tomar el o2 como narcotico
        """
        return self.end(depth, o2_narcotic=False) / (1-self.O2_IN_AIR)


    @staticmethod
    def partial_pressure(abs_pressure: float, volume_fraction: float) -> float:
        """
        Calculates the partial pressure of a gas component from the volume gas fraction and total pressure.
        """
        return abs_pressure * volume_fraction


