import numpy as np
from math import tau

class Interpolate:
    def __init__(self, number=200):
        self.number = number
    
    def interpol(self, values):
        angle = np.linspace(0, tau, len(values))
        xvals = np.linspace(0, tau, self.number)
        return np.interp(xvals, angle, values)
        