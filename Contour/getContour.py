import cv2
import numpy as np

class Contour:
    def __init__(self, img_path) -> None:
        self.img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if self.img is not None:
            self.get_contour()
            self.get_values()
        
    def get_contour(self):
        img = cv2.bitwise_not(self.img)
        _, bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
        contours, _  = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contour = max(contours, key=cv2.contourArea)
        
    def get_values(self):
        center = self.get_center()
        self.x_list = [v[0] for [v] in self.contour]-np.array(center[0])
        self.y_list = [v[1] for [v] in self.contour]-np.array(center[1])
        
    def get_center(self):
        x = [v[0] for [v] in self.contour]
        y = [v[1] for [v] in self.contour]
        center = [np.mean(x), np.mean(y)]
        return center
        
        