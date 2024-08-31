import matplotlib.pyplot as plt
import numpy as np
from math import tau

class Complex:
    def __init__(self, x_list, y_list) -> None:
        self.angle = np.linspace(0, np.pi, len(x_list))
        self.x = x_list
        self.y = y_list
        
        self.analyse_value(self.y)
        
    def analyse_value(self, value):
        max_ind = np.argmax(value)
        min_ind = np.argmin(value)
        plt.plot(self.angle, value)
        plt.axhline(y=0, color='black', linestyle='-')
        plt.plot([self.angle[max_ind], self.angle[max_ind]], [0, value[max_ind]], 'r-')
        plt.plot([self.angle[min_ind], self.angle[min_ind]], [0, value[min_ind]], 'b-')
        plt.show()
    
def main():
    x = np.load('../Datas/x_list.npy')
    y = np.load('../Datas/y_list.npy')
    Complex(x_list=x, y_list=y)
    
if __name__=='__main__':
    main()