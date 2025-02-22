import re
from typing import Optional, Dict

class Gas:
    def __init__(self, o2_fraction: float, he_fraction: float):
        self.o2_fraction = o2_fraction
        self.he_fraction = he_fraction

class GasNames:
    air_name = 'Air'
    oxygen_name = 'Oxygen'

class StandardGases:
    # Hyperoxic
    oxygen = Gas(1, 0)  # 0 - 6 m, deco only
    ean50 = Gas(0.5, 0)  # 0 - 21 m, deco only
    ean38 = Gas(0.38, 0)  # 0 - 24.2 m
    ean36 = Gas(0.36, 0)  # 0 - 26.1 m
    ean32 = Gas(0.32, 0)  # 0 - 30.6 m
    trimix3525 = Gas(0.35, 0.25)  # 0 - 27.1 m, deco only
    trimix2525 = Gas(0.25, 0.25)  # 0 - 42 m

    # Normoxic
    air = Gas(0.209, 0)  # 0 - 52.2 m
    trimix2135 = Gas(0.21, 0.35)  # 0 - 51.9 m
    trimix1845 = Gas(0.18, 0.45)  # 0 - 62.2 m

    # Hypoxic
    trimix1555 = Gas(0.15, 0.55)  # 2 - 76.6 m
    trimix1260 = Gas(0.12, 0.6)  # 5 - 98.3 m
    trimix1070 = Gas(0.1, 0.7)  # 8 - 120 m

    # Regular expressions for gas names
    names_regex = re.compile(r'[EAN](?P<fO2>\d{2})|(?P<fO2b>\d{2})\/(?P<fHe>\d{2})', re.IGNORECASE)

    # Mapping gas names to Gas instances
    _gas_map: Dict[str, Gas] = {
        GasNames.air_name: air,
        'EAN32': ean32,
        'EAN36': ean36,
        'EAN38': ean38,
        'EAN50': ean50,
        GasNames.oxygen_name: oxygen,
        'Helitrox 35/25': trimix3525,
        'Helitrox 25/25': trimix2525,
        'Helitrox 21/35': trimix2135,
        'Trimix 18/45': trimix1845,
        'Trimix 15/55': trimix1555,
        'Trimix 12/60': trimix1260,
        'Trimix 10/70': trimix1070,
    }

    @staticmethod
    def nitrox_names() -> list[str]:
        """Gets names of all predefined gases with 0 % helium (nitrox) only."""
        return list(StandardGases._gas_map.keys())[:6]

    @staticmethod
    def all_names() -> list[str]:
        """Gets names of all predefined gases including both nitrox and trimix gases."""
        return list(StandardGases._gas_map.keys())

    @staticmethod
    def by_name(name: str) -> Optional[Gas]:
        """Case insensitive search. If nothing found returns None."""
        found_key = next(
            (k for k in StandardGases._gas_map if k.lower() == name.lower()), None
        )

        if found_key:
            return StandardGases._gas_map[found_key]

        match = StandardGases.names_regex.match(name)

        if match:
            if match.group('fO2'):
                parsed_o2 = int(match.group('fO2')) / 100
                if parsed_o2 > 0:
                    return Gas(parsed_o2, 0)

            if match.group('fO2b') and match.group('fHe'):
                trim_o2 = int(match.group('fO2b')) / 100
                trim_he = int(match.group('fHe')) / 100
                if trim_o2 > 0 and trim_he > 0:
                    return Gas(trim_o2, trim_he)

        return None
