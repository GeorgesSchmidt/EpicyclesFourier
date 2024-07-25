import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import tau
from scipy.fftpack import fft, ifft
from matplotlib.gridspec import GridSpec
import matplotlib.animation as animation

from contours import Contours

class Fourier(Contours):
    def __init__(self, path, number=200, order=3) -> None:
        super().__init__(path, number)
        self.x_data = [v[0] for v in self.liss]
        self.y_data = [v[1] for v in self.liss]
        self.angle = np.linspace(0, tau, len(self.liss))
        
        fig = plt.figure(figsize=(25, 10))  # Ajusté la hauteur pour plus d'espace
        gs = GridSpec(2, 3, width_ratios=[3, 3, 1])
        
        self.ax0 = fig.add_subplot(gs[0, 0])
        self.ax1 = fig.add_subplot(gs[0, 1])
        self.ax2 = fig.add_subplot(gs[1, 0])
        self.ax3 = fig.add_subplot(gs[1, 1])
        self.ax4 = fig.add_subplot(gs[:, 2])
        
        ani = animation.FuncAnimation(
            fig, self.anim, frames=np.linspace(0, 0.2, 50), blit=False, interval=50
        )
        plt.show()
        ani.save('Anim_FFT_1.mp4', writer='ffmpeg')
        
    def anim(self, frame):
        # Print the current frame number
        print(f"Animating frame {frame}")
        
        # Calcul des coefficients de Fourier pour x et y
        c_x = self.calcul_coef(self.x_data)
        amp_x, c_x, t_x, nb_x = self.modif_coef(c_x, value=frame)
        v_x = self.inverse_four(c_x)
        
        c_y = self.calcul_coef(self.y_data)
        amp_y, c_y, t_y, nb_y = self.modif_coef(c_y, value=frame)
        v_y = self.inverse_four(c_y)

        # Mise à jour des graphiques
        self.ax0.clear()
        self.ax0.set_title(f'Amplitudes x nb de coef non nuls = {nb_x}')
        self.ax0.axhline(y=t_x, color='r', linestyle='-', linewidth=2)
        self.ax0.plot(amp_x)
        
        self.ax1.clear()
        self.ax1.plot(self.angle, self.x_data, label='Original x')
        self.ax1.plot(self.angle, v_x, label='Reconstructed x')
        self.ax1.set_title('Variation x')
        self.ax1.legend()
        
        self.ax2.clear()
        self.ax2.set_title(f'Amplitudes y nb de coef non nuls = {nb_y}')
        self.ax2.axhline(y=t_y, color='r', linestyle='-', linewidth=2)
        self.ax2.plot(amp_y)
        
        self.ax3.clear()
        self.ax3.plot(self.angle, self.y_data, label='Original y')
        self.ax3.plot(self.angle, v_y, label='Reconstructed y')
        self.ax3.set_title('Variation y')
        self.ax3.legend()
        
        self.ax4.clear()
        self.ax4.plot(self.x_data, self.y_data, label='Original')
        self.ax4.plot(v_x, v_y, label='Reconstructed')
        self.ax4.invert_yaxis()
        self.ax4.set_title('XY Plane')
        self.ax4.legend()
    
    def calcul_coef(self, x):
        N = len(x)
        c = fft(x) / N
        return c
    
    def modif_coef(self, coef, value=0.1):
        amplitudes = np.abs(coef)
        max_amp = max(amplitudes)
        thresh = value * max_amp
        nb = 0
        for ind, c in enumerate(coef):
            amp = np.abs(c)
            if amp < thresh:
                coef[ind] = 0
            else:
                nb += 1
        return amplitudes, coef, thresh, nb
        
    def inverse_four(self, coefficients):
        N = len(coefficients)
        y_reconstructed = ifft(coefficients) * N
        return np.real(y_reconstructed)

if __name__ == '__main__':
    path = 'pi.jpg'
    Fourier(path, number=200, order=10)
