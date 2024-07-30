import cv2
import numpy as np
from math import tau
from scipy import signal

class Liss:
    def __init__(self, order=5) -> None:
        self.order = order
        
    
    def cyclic_moving_av(self, a, win_type='boxcar'):
        window = signal.get_window(win_type, self.order, fftbins=False).reshape((1, self.order))
        shp_a = a.shape
        b = signal.convolve2d(a.reshape((np.prod(shp_a[:-1], dtype=int), shp_a[-1])),
                              window, boundary='wrap', mode='same')
        return (b / np.sum(window)).reshape(shp_a)