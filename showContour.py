import cv2
import matplotlib.pyplot as plt
from math import tau
import numpy as np
import argparse

from Contour.getContour import Contour
from Contour.interpolate import Interpolate
from Contour.lissage import Liss



class ShowCont:
    def __init__(self, Cont) -> None:
        self.x_list = Cont.x_list
        self.y_list = Cont.y_list
        self.angle = np.linspace(0, tau, len(self.x_list))
        self.plot()
        
    def plot(self):
        fig = plt.figure(figsize=(10, 6))

        ax1 = fig.add_subplot(2, 2, 1)  
        ax2 = fig.add_subplot(2, 2, 3)  
        ax3 = fig.add_subplot(1, 2, 2) 
        
        ax1.plot(self.angle, self.x_list)
        ax1.set_title('décomposition x')
        ax1.invert_yaxis()
        
        
        ax2.plot(self.angle, self.y_list)
        ax2.set_title('décomposition y')
        ax2.invert_yaxis()
        
        ax3.plot(self.x_list, self.y_list)
        ax3.set_title(f'contour : {len(self.x_list)} points')
        ax3.invert_yaxis()
        
        plt.show()
        
def main(path):
    cont = Contour(path)
    ShowCont(cont)
    
    interp = Interpolate(number=200)
    cont.x_list = interp.interpol(cont.x_list)
    cont.y_list = interp.interpol(cont.y_list)
    ShowCont(cont)
    
    liss = Liss(order=5)
    cont.x_list = liss.cyclic_moving_av(cont.x_list)
    cont.y_list = liss.cyclic_moving_av(cont.y_list)
    ShowCont(cont)
    
        
if __name__=='__main__':
    path = 'Pictures/pi.jpg'
    parser = argparse.ArgumentParser(description='Process image contours.')
    parser.add_argument('path', type=str, default=path, help='Chemin vers le fichier image')
    args = parser.parse_args()
    main(args.path)
    
    
    