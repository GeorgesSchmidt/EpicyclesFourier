import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import tau

from contours import Contours

class DFT2D(Contours):
    def __init__(self, path, number=200) -> None:
        super().__init__(path, number)
        self.order = [5, 5]
        self.create_image()
        self.create_mask()
        self.calcul_DFT()
        
    def create_image(self):
        x = [v[0] for v in self.liss]
        y = [v[1] for v in self.liss]
        vx = self.normalise_data(x)
        vy = self.normalise_data(y)
        line = []
        self.image = np.zeros((100, 100), dtype=np.uint8)
        for x, y in zip(vx, vy):
            p = [x*100, y*100]
            line.append(p)
        line = np.array(line).astype(int)
        tot = []
        tot.append(line)
        cv2.fillPoly(self.image, tot, (255))
        
        
        
    def create_mask(self):
        h, w = self.image.shape
        mid_h = h//2
        mid_w = w//2
        ord_x, ord_y = self.order
        self.mask = np.zeros((h, w, 2), float)
        x0, x1 = mid_w-ord_x, mid_w+ord_x
        y0, y1 = mid_h-ord_y, mid_h+ord_y
        self.mask[y0:y1, x0:x1] = 1
        
    def calcul_DFT(self):
        float_image = self.image.astype(np.float32) / 255.0
        shift_image = self.calculCoef2D(float_image)
        ifft = shift_image*self.mask
        result_image = self.getImageWithCoef(ifft)
        
        fig = plt.figure(figsize=(15, 5))
        ax0 = fig.add_subplot(131)
        ax0.imshow(self.image, cmap='gray')
        
        ax1 = fig.add_subplot(132, projection='3d')
        ax1.set_title(f'order DFT = {self.order}')
        self.plot_mag(ifft, ax1)
        self.plot_mask(ax1)
        
        ax2 = fig.add_subplot(133)
        ax2.set_title('result')
        ax2.imshow(result_image, cmap='gray')
        #plt.show()
        title = f'Pictures/image_DFT_{self.order}.png'
        plt.savefig(title)
        
    def plot_mat(self, mat, ax, color='black'):
        h, w = mat.shape

        for i in range(h):
            x, y, z = [], [], []
            for j in range(w):
                v = mat[i][j]
                x.append(j)
                y.append(i)
                z.append(v)
            ax.plot3D(x, y, z, linewidth=0.3, color=color)
    
        
    def plot_mask(self, ax):
        h, w = self.mask.shape[:2]
        mid_h = h//2
        mid_w = w//2
        ord_x, ord_y = self.order
        x0, x1 = mid_w-ord_x, mid_w+ord_x
        y0, y1 = mid_h-ord_y, mid_h+ord_y
        x = [x0, x1, x1, x0, x0]
        y = [y0, y0, y1, y1, y0]
        z = [0, 0, 0, 0, 0]
        ax.plot3D(y, x, z, color='black', linewidth=2)
        
        
        
    def normalise_data(self, data):
        min_vals = np.min(data, axis=0)
        max_vals = np.max(data, axis=0)
        self.dim = [min_vals, max_vals]
        normalized_data = (data - min_vals) / (max_vals - min_vals)
        return normalized_data
    
    def calculCoef2D(self, img):
        dft_result = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
        shift = np.fft.fftshift(dft_result)
        return shift
    
    def getImageWithCoef(self, coef):
        fft_ifft_shift = np.fft.ifftshift(coef)
        result = cv2.idft(fft_ifft_shift, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
        
        return result
    
    def plot_mag(self, shift, ax):
        mat = cv2.magnitude(shift[:,:,0], shift[:,:,1])
        h, w = mat.shape
        
        for i in range(h):
            x, y, z = [], [], []
            for j in range(w):
                v = mat[i][j]
                x.append(i)
                y.append(j)
                z.append(v)
            ax.plot3D(x, y, z)

        
        
if __name__ == '__main__':
    path = 'pi.jpg'
    DFT2D(path, number=200)