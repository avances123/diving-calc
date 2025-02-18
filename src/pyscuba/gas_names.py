class GasNames:
    air_name = 'Aire'
    oxygen_name = 'Oxigeno'
    helium_name = 'Helio'


    @staticmethod
    def name_for(fO2: float, fHe: float = 0) -> str:
        simple_o2_in_air = 21

        # Redondeo de los valores
        percent_o2 = int(fO2 * 100)
        percent_he = int(fHe * 100)

        assert 0 <= percent_o2 <= 100, f"Error: {percent_o2} está fuera del rango [0, 100]"
        assert 0 <= percent_he <= 100, f"Error: {percent_he} está fuera del rango [0, 100]"


        if percent_he == 0:
            # Evita overflow de best gas
            if percent_o2 == 100:
                return GasNames.oxygen_name

            if percent_o2 == simple_o2_in_air:
                return GasNames.air_name

            return f"EAN{percent_o2}"

        prefix = "Helitrox" if percent_o2 >= simple_o2_in_air else "Trimix"
        return f"{prefix} {percent_o2}/{percent_he}"

