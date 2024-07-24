import cv2
import numpy as np
from math import tau
import matplotlib.pyplot as plt
from scipy import signal


class Contours:
    def __init__(self, path, number=200) -> None:
        self.number = number
        self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.img = cv2.bitwise_not(self.img)
        self.get_contour()
        self.interpolate_contour()
        self.lissage_contour(order=10)
        self.show_result()
        
    def get_contour(self):
        _, bin = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY)
        contours, _  = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contour = max(contours, key=cv2.contourArea)
        color = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(color, self.contour, -1, (0, 0, 255), 2)
        self.put_text(color, len(self.contour))
        title = 'image_originale.png'
        cv2.imwrite(title, color)
        
    def put_text(self, img, nb):
        text = f'nb de points : {nb}'
        p = (10, 50)
        font = 1
        font_scale = 1.0
        color = (255, 255, 255)
        thick = 2
        cv2.putText(img, text, p, font, font_scale, color, thick)

        
        
    def interpolate_contour(self):
        x = [v[0] for [v] in self.contour]
        y = [v[1] for [v] in self.contour]
        angle = np.linspace(0, tau, len(x))
        xvals = np.linspace(0, tau, self.number)
        vx = np.interp(xvals, angle, x)
        vy = np.interp(xvals, angle, y)
        self.contour = list(zip(vx, vy))
        
        
    def lissage_contour(self, order):
        center = self.get_center(self.contour)
        x = [v[0] for v in self.contour]-np.array(center[0])
        y = [v[1] for v in self.contour]-np.array(center[1])
        self.contour = list(zip(x, y))
        vx = self.cyclic_moving_av(x, n=order)
        vy = self.cyclic_moving_av(y, n=order)
        self.liss = list(zip(vx, vy))
       
        
    def get_center(self, cont):
        x = [v[0] for v in cont]
        y = [v[1] for v in cont]
        center = [np.mean(x), np.mean(y)]
        return center
        
    def cyclic_moving_av(self, a, n=3, win_type='boxcar'):
        window = signal.get_window(win_type, n, fftbins=False).reshape((1, n))
        shp_a = a.shape
        b = signal.convolve2d(a.reshape((np.prod(shp_a[:-1], dtype=int), shp_a[-1])),
                              window, boundary='wrap', mode='same')
        return (b / np.sum(window)).reshape(shp_a)

        
    def show_result(self):
        fig = plt.figure(figsize=(15, 5))
        ax0 = fig.add_subplot(131)
        ax0.imshow(self.img, cmap='gray')
        ax1 = fig.add_subplot(132)
        self.plot_contour(self.contour, ax1)
        x = [v[0] for v in self.contour]
        y = [v[1] for v in self.contour]
        ax1.scatter(x, y)
        ax2 = fig.add_subplot(133)
        self.plot_contour(self.liss, ax2)
        plt.show()
        
        
    def plot_contour(self, contour, ax):
        x = [v[0] for v in contour]
        y = [v[1] for v in contour]
        ax.plot(x, y)
        ax.invert_yaxis()
        ax.grid(True)
    
        
        
        
if __name__=='__main__':
    path = 'pi.jpg'
    Contours(path)