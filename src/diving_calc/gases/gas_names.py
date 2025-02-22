class GasNames:
    air_name = 'Air'
    oxygen_name = 'Oxygen'

    @staticmethod
    def name_for(fO2: float, fHe: float = 0) -> str:
        simple_O2_in_air = 21
        percent_O2 = round(fO2 * 100)
        percent_He = round(fHe * 100)

        if percent_O2 <= 0:
            return ''

        if percent_He <= 0:
            # Prevent best gas overflow
            if percent_O2 >= 100:
                return GasNames.oxygen_name

            if percent_O2 == simple_O2_in_air:
                return GasNames.air_name

            return f'EAN{percent_O2}'

        prefix = 'Helitrox' if percent_O2 >= simple_O2_in_air else 'Trimix'
        return f'{prefix} {percent_O2}/{percent_He}'
