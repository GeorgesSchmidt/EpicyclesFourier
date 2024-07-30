import unittest
import numpy as np
import cv2
from io import BytesIO
from Contour.getContour import Contour

class TestContour(unittest.TestCase):
    def setUp(self):
        # Création d'une image de test avec un contour simple
        self.img = np.zeros((100, 100), dtype=np.uint8)
        cv2.rectangle(self.img, (20, 20), (80, 80), 255, -1)  # Un rectangle blanc sur fond noir

        # Sauvegarde l'image dans un buffer pour utiliser dans les tests
        self.image_path = 'test_image.png'
        cv2.imwrite(self.image_path, self.img)
        
        # Instancie l'objet Contour
        self.contour = Contour(self.image_path)
        
    def test_contour_detection(self):
        # Vérifie si le contour est détecté
        self.assertIsNotNone(self.contour.contour, "Contour should not be None")
        self.assertGreater(len(self.contour.contour), 0, "Contour length should be greater than 0")

    def test_get_values(self):
        # Vérifie que les valeurs x_list et y_list sont correctes
        center = self.contour.get_center()
        x_list = np.array([v[0][0] for v in self.contour.contour]) - center[0]
        y_list = np.array([v[0][1] for v in self.contour.contour]) - center[1]

        np.testing.assert_array_almost_equal(self.contour.x_list, x_list, decimal=1, err_msg="x_list values are incorrect")
        np.testing.assert_array_almost_equal(self.contour.y_list, y_list, decimal=1, err_msg="y_list values are incorrect")

    def test_get_center(self):
        # Vérifie que le centre est calculé correctement
        expected_center = [np.mean([v[0][0] for v in self.contour.contour]), np.mean([v[0][1] for v in self.contour.contour])]
        center = self.contour.get_center()
        np.testing.assert_array_almost_equal(center, expected_center, decimal=1, err_msg="Center calculation is incorrect")

    def tearDown(self):
        import os
        # Nettoie les fichiers temporaires
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

if __name__ == '__main__':
    unittest.main()
