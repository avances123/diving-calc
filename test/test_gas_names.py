import unittest
from pyscuba.gas_names import GasNames

class TestGasNames(unittest.TestCase):

    def test_name_for(self):
        test_cases = [
            (1.0, 0.0, "Oxigeno"),   # 100% O2 → "Oxigeno"
            (0.21, 0.0, "Aire"),      # 21% O2 → "Aire"
            (0.32, 0.0, "EAN32"),     # 32% O2 → "EAN32"
            (0.18, 0.35, "Trimix 18/35"), # 18% O2, 35% He → "Trimix 18/35"
            (0.30, 0.20, "Helitrox 30/20"), # 30% O2, 20% He → "Helitrox 30/20"
            (0.21, 0.30, "Helitrox 21/30"), # 30% O2, 20% He → "Helitrox 30/20"
        ]

        for fO2, fHe, expected in test_cases:
            with self.subTest(fO2=fO2, fHe=fHe, expected=expected):
                self.assertEqual(GasNames.name_for(fO2, fHe), expected)

    def test_invalid_o2(self):
        with self.assertRaises(AssertionError):
            GasNames.name_for(-0.1, 0.0)  # O2 negativo

        with self.assertRaises(AssertionError):
            GasNames.name_for(1.1, 0.0)  # O2 mayor a 100%

    def test_invalid_he(self):
        with self.assertRaises(AssertionError):
            GasNames.name_for(0.21, -0.1)  # He negativo

        with self.assertRaises(AssertionError):
            GasNames.name_for(0.21, 1.1)  # He mayor a 100%

if __name__ == '__main__':
    unittest.main()
