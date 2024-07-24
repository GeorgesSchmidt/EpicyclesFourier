import cv2
import matplotlib.pyplot as plt
import numpy as np 
from math import tau
from scipy.integrate import quad_vec
from tqdm import tqdm # for progress bar
import matplotlib.animation as animation 

from contours import Contours
class Epicycles(Contours):
    def __init__(self, path, number, order) -> None:
        super().__init__(path, number)
        self.order = order
        self.x_list = np.array([v[0] for v in self.liss]).astype(float)
        self.y_list = np.array([v[1] for v in self.liss]).astype(float)
        self.xlim_data = [np.min(self.x_list)*2, np.max(self.x_list)*2]
        self.ylim_data = [np.min(self.y_list)*2, np.max(self.y_list)*2]
        self.t_list = np.linspace(0, tau, len(self.x_list))
        print("datas", len(self.x_list))
        
        self.calcul_coeficients()
        self.plot_epicycles()
        self.showEpicycles()
        
    def f(self, t, t_list, x_list, y_list):
        "produit un nombre complexe (re + im j)"
        return np.interp(t, t_list, x_list + 1j * y_list)

    def calcul_coeficients(self):
        print("generating coefficients ...")
        # lets compute fourier coefficients from -order to order
        pbar = tqdm(total=(self.order * 2 + 1))

        self.c = []
        # we need to calculate the coefficients from -order to order
        for n in range(-self.order, self.order + 1):
            coef = 1 / tau * quad_vec(lambda t: self.f(t, self.t_list, self.x_list, self.y_list) * np.exp(-n * t * 1j), 0, tau, limit=100,
                                      full_output=1)[0]
            self.c.append(coef)
            pbar.update(1)
        pbar.close()
        print("completed generating coefficients.")
        self.c = np.array(self.c)

    def sort_coeff(self, coeffs):
        new_coeffs = []
        new_coeffs.append(coeffs[self.order])
        for i in range(1, self.order + 1):
            new_coeffs.extend([coeffs[self.order + i], coeffs[self.order - i]])
        return np.array(new_coeffs)
    
    def make_frame(self, i, time, coeffs):
        global pbar
        t = time[i]
       

        # exponential term to be multiplied with coefficient
        # this is responsible for making rotation of circle
        exp_term = np.array([np.exp(n * t * 1j) for n in range(-self.order, self.order + 1)])
        

        # sort the terms of fourier expression
        coeffs = self.sort_coeff(coeffs * exp_term)  # coeffs*exp_term makes the circle rotate.
        # coeffs itself gives only direction and size of circle
        # split into x and y coefficients
        x_coeffs = np.real(coeffs)
        y_coeffs = np.imag(coeffs)
        #print('x coef = ', x_coeffs)

        # center points for fisrt circle
        center_x, center_y = 0, 0

        # make all circles i.e epicycle
        for i, (x_coeff, y_coeff) in enumerate(zip(x_coeffs, y_coeffs)):
            # calculate radius of current circle
            r = np.linalg.norm([x_coeff, y_coeff])  # similar to magnitude: sqrt(x^2+y^2)

            # draw circle with given radius at given center points of circle
            # circumference points: x = center_x + r * cos(theta), y = center_y + r * sin(theta)
            theta = np.linspace(0, tau, num=50)  # theta should go from 0 to 2*PI to get all points of circle
            x, y = center_x + r * np.cos(theta), center_y + r * np.sin(theta)
            self.circles[i].set_data(x, y)

            # draw a line to indicate the direction of circle
            x, y = [center_x, center_x + x_coeff], [center_y, center_y + y_coeff]
            self.circle_lines[i].set_data(x, y)

            # calculate center for next circle
            center_x, center_y = center_x + x_coeff, center_y + y_coeff

        x, y = [0, center_x, center_x], [center_y, center_y, 0]
        self.lines[i].set_data(x, y)

        # center points now are points from last circle
        # these points are used as drawing points
        self.draw_x.append(center_x)
        self.draw_y.append(center_y)

        # draw the curve from last point
        self.drawing.set_data(self.draw_x, self.draw_y)

        # draw the real curve
        self.orig_drawing.set_data(self.x_list, self.y_list)


    def showEpicycles(self):
        self.draw_x, self.draw_y = [], []

        fig, ax = plt.subplots()

        # different plots to make epicycle
        # there are -order to order numbers of circles
        self.circles = [ax.plot([], [], 'r-')[0] for i in range(-self.order, self.order + 1)]
        #lines des coordonnées
        self.lines = [ax.plot([], [], 'g-')[0] for i in range(-self.order, self.order + 1)]
        # circle_lines are radius of each circles
        self.circle_lines = [ax.plot([], [], 'b-')[0] for i in range(-self.order, self.order + 1)]
        # drawing is plot of final drawing
        self.drawing, = ax.plot([], [], 'k-', linewidth=2)

        # original drawing
        self.orig_drawing, = ax.plot([], [], 'g-', linewidth=0.5)

        # to fix the size of figure so that the figure does not get cropped/trimmed
        ax.set_xlim(self.xlim_data[0], self.xlim_data[1])
        ax.set_ylim(self.ylim_data[0], self.ylim_data[1])

        ax.grid(False)
        #dessin des axes d'origine
        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')

        # to have symmetric axes
        ax.set_aspect('equal')

        
        time = np.linspace(0, tau, num=self.number)

        anim = animation.FuncAnimation(fig, self.make_frame, frames=self.number, fargs=(time, self.c), interval=100)
        ax.invert_yaxis()
        plt.show()
        
    def plot_epicycles(self):
        vx = []
        vy = []
        
        for t in self.t_list:
            exp_term = np.array([np.exp(n * t * 1j) for n in range(-self.order, self.order + 1)])
            coeffs = self.c*exp_term
            coeffs = self.sort_coeff(coeffs)
            x_coeffs = np.real(coeffs)
            y_coeffs = np.imag(coeffs)
            center_x, center_y = 0, 0
            for i, (x, y) in enumerate(zip(x_coeffs, y_coeffs)):
                center_x += x
                center_y += y
            vx.append(center_x)
            vy.append(center_y)

        fig = plt.figure(figsize=(15, 5))
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.plot(self.x_list, self.y_list, 'b')
        ax1.plot(vx, vy, 'r')
        ax1.invert_yaxis()

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(self.x_list, 'b')
        ax2.plot(vx, 'r')
        ax2.set_title('variation en x')

        ax3 = fig.add_subplot(2, 2, 4)
        ax3.plot(self.y_list, 'b')
        ax3.plot(vy, 'r')
        ax3.set_title('variation en y')
        plt.show()
        #plt.savefig('epicycles.png')
        
        
if __name__=='__main__':
    path = 'pi.jpg'
    Epicycles(path, number=200, order=10)