import unittest

from app.domain.units import UnitError, compatible, convert


class UnitTests(unittest.TestCase):
    def test_energy_conversion(self):
        self.assertAlmostEqual(convert(1, "kWh", "MJ"), 3.6)
        self.assertTrue(compatible("kWh", "MJ"))

    def test_mass_conversion(self):
        self.assertAlmostEqual(convert(1, "t", "kg"), 1000)

    def test_incompatible_units_fail(self):
        self.assertFalse(compatible("kg", "kWh"))
        with self.assertRaises(UnitError):
            convert(1, "kg", "kWh")

