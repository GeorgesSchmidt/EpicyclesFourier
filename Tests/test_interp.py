import unittest
import numpy as np
from Contour.interpolate import Interpolate


class TestInterpolate(unittest.TestCase):
    def setUp(self):
        # Crée une instance de Interpolate avec un nombre spécifique de points
        self.interpolator = Interpolate(number=100)
        
        # Données de test : une liste simple de valeurs et leurs angles associés
        self.values = np.array([0, 1, 4, 9, 16])
        self.expected_length = 100  # Nombre de points après interpolation

    def test_interpol_length(self):
        # Vérifie que la longueur des valeurs interpolées est correcte
        interpolated_values = self.interpolator.interpol(self.values)
        self.assertEqual(len(interpolated_values), self.expected_length, "Interpolated values length should match the number specified")

    def test_interpol_range(self):
        # Vérifie que les valeurs interpolées sont dans la plage attendue
        interpolated_values = self.interpolator.interpol(self.values)
        self.assertTrue(np.all(interpolated_values >= 0) and np.all(interpolated_values <= 16),
                        "Interpolated values should be within the range of original values")

    def test_interpol_values(self):
        # Vérifie que les valeurs interpolées sont raisonnables pour les données simples
        interpolated_values = self.interpolator.interpol(self.values)
        # Les valeurs attendues pour des données simples peuvent être vérifiées avec des résultats connus ou des valeurs approximatives.
        # Ici, on fait juste un exemple de vérification de certaines propriétés.
        self.assertTrue(np.all(np.diff(interpolated_values) >= 0), "Interpolated values should be in increasing order")

if __name__ == '__main__':
    unittest.main()
