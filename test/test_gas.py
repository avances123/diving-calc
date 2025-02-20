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


if __name__ == "__main__":
    unittest.main()
