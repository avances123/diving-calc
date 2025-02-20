import unittest
import math
from pyscuba.gas import Gas  # Asume que la clase Gas está en un archivo llamado gas.py
from pyscuba.profundidad import Densidad


class TestGas(unittest.TestCase):
    
    def test_gas_valido(self):
        gas = Gas(o2=21, n2=79)
        self.assertEqual(gas.o2, 21)
        self.assertEqual(gas.n2, 79)
        self.assertEqual(gas.he, 0)
        self.assertEqual(repr(gas), "Aire")

    def test_gas_con_he(self):
        gas = Gas(o2=32, he=10)  # n2 debería calcularse automáticamente como 58
        self.assertEqual(gas.o2, 32)
        self.assertEqual(gas.n2, 58)
        self.assertEqual(gas.he, 10)
        self.assertEqual(repr(gas), "Helitrox 32/10")

    def test_gas_nitrox(self):
        gas = Gas(o2=36)  # n2 debería ser 64
        self.assertEqual(gas.o2, 36)
        self.assertEqual(gas.n2, 64)
        self.assertEqual(gas.he, 0)
        self.assertEqual(repr(gas), "Nitrox 36")

    def test_gas_oxigeno_puro(self):
        gas = Gas(o2=100)
        self.assertEqual(gas.o2, 100)
        self.assertEqual(gas.n2, 0)
        self.assertEqual(gas.he, 0)
        self.assertEqual(repr(gas), "Oxígeno")

    def test_error_suma_incorrecta(self):
        with self.assertRaises(ValueError):
            Gas(o2=50, n2=40, he=20)  # Suma 110%, debería lanzar error

    def test_error_o2_fuera_rango(self):
        with self.assertRaises(ValueError):
            Gas(o2=110)  # Error, fuera del rango permitido

    def test_error_he_fuera_rango(self):
        with self.assertRaises(ValueError):
            Gas(o2=50, he=-10)  # Error, he no puede ser negativo

    def test_mod_air(self):
        gas = Gas(o2=21)
        mod = gas.MOD(ppO2=1.4) 
        self.assertAlmostEqual(mod, 56.10, places=2) # aire en agua salada

    def test_mod_nitrox32(self):
        gas = Gas(o2=32)
        mod = gas.MOD(ppO2=1.4)
        self.assertAlmostEqual(mod, 33.41, places=2)

    def test_mod_pure_oxygen(self):
        gas = Gas(o2=100)
        mod = gas.MOD(ppO2=1.6)
        self.assertAlmostEqual(mod, 5.94, places=2)


    def test_mod_different_density(self):
        gas = Gas(o2=21)
        mod = gas.MOD(ppO2=1.4, densidad=Densidad.DULCE)
        self.assertAlmostEqual(mod, 57.78, places=2)

    def test_mod_different_surface_pressure(self):
        gas = Gas(o2=21)
        mod = gas.MOD(ppO2=1.4, presion_superficie=1.1) # Higher surface pressure (altitude < 0)
        self.assertAlmostEqual(mod, 9.20, places=2)


if __name__ == "__main__":
    unittest.main()
