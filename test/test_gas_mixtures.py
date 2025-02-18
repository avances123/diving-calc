import unittest
from math import isclose
from pyscuba.gas_mixtures import GasMixtures, DepthConverter

class TestGasMixtures(unittest.TestCase):

    def setUp(self):
        self.depth_converter = DepthConverter()

    def test_partial_pressure(self):
        abs_pressure = 1.0
        volume_fraction = 0.79
        result = GasMixtures.partial_pressure(abs_pressure, volume_fraction)
        self.assertAlmostEqual(result, 0.79, places=2)

    def test_mod(self):
        pp_o2 = 0.4
        f_o2 = 0.21
        result = GasMixtures.mod(pp_o2, f_o2)
        self.assertAlmostEqual(result, 1.90476, places=5)

    def test_best_mix(self):
        p_o2 = 1.4
        depth = 40
        result = GasMixtures.best_mix(p_o2, depth, self.depth_converter)
        self.assertAlmostEqual(result, 0.35, places=2)

    def test_ead(self):
        f_o2 = 0.3
        depth = 40
        result = GasMixtures.ead(f_o2, depth)
        self.assertAlmostEqual(result, 26.6667, places=4)

    def test_end(self):
        current_depth = 30
        f_n2 = 0.79
        f_o2 = 0.21
        result = GasMixtures.end(current_depth, f_n2, f_o2)
        self.assertAlmostEqual(result, 30, places=2)

    def test_mnd(self):
        narcotic_depth = 40
        f_n2 = 0.79
        f_o2 = 0.21
        result = GasMixtures.mnd(narcotic_depth, f_n2, f_o2)
        self.assertAlmostEqual(result, 40, places=2)

    def test_ceiling(self):
        f_o2 = 0.3
        surface_pressure = 1.0
        result = GasMixtures.ceiling(f_o2, surface_pressure)
        self.assertAlmostEqual(result, 3.3333, places=4)

    def test_narcotic_index(self):
        f_n2 = 0.79
        f_o2 = 0.21
        result = GasMixtures.narcotic_index(f_n2, f_o2)
        self.assertEqual(result, 1.0)

if __name__ == '__main__':
    unittest.main()

