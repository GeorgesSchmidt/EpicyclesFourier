import unittest
import numpy as np
from scipy import signal

from Contour.lissage import Liss

class TestLiss(unittest.TestCase):
    def setUp(self):
        # Crée une instance de Liss avec un ordre spécifique
        self.liss = Liss(order=5)
        
        # Données de test : un tableau simple
        self.a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        # Recalculons les résultats attendus
        window_size = 5
        window = signal.get_window('boxcar', window_size, fftbins=False)
        window = window.reshape((1, window_size))
        shp_a = self.a.shape
        b = signal.convolve2d(self.a.reshape((np.prod(shp_a[:-1], dtype=int), shp_a[-1])),
                              window, boundary='wrap', mode='same')
        self.expected_result_boxcar = (b / np.sum(window)).reshape(shp_a)

    def test_cyclic_moving_av_boxcar(self):
        # Vérifie le lissage avec la fenêtre 'boxcar'
        result = self.liss.cyclic_moving_av(self.a, win_type='boxcar')
        np.testing.assert_array_almost_equal(result, self.expected_result_boxcar, decimal=1, err_msg="Boxcar window smoothing is incorrect")

    def test_window_types(self):
        # Teste différents types de fenêtres
        for win_type in ['boxcar', 'hamming', 'hann', 'bartlett']:
            result = self.liss.cyclic_moving_av(self.a, win_type=win_type)
            self.assertEqual(result.shape, self.a.shape, f"Result shape should match input shape for window type {win_type}")

    def test_order(self):
        # Teste avec différentes valeurs d'ordre
        for order in [3, 5, 7]:
            liss = Liss(order=order)
            result = liss.cyclic_moving_av(self.a, win_type='boxcar')
            self.assertEqual(result.shape, self.a.shape, f"Result shape should match input shape for order {order}")

    def test_edge_case(self):
        # Teste un cas de bord avec des données simples et des fenêtres spécifiques
        a_edge = np.array([1])
        expected_result_edge = np.array([1])
        result_edge = self.liss.cyclic_moving_av(a_edge, win_type='boxcar')
        np.testing.assert_array_almost_equal(result_edge, expected_result_edge, decimal=1, err_msg="Edge case smoothing is incorrect")

if __name__ == '__main__':
    unittest.main()