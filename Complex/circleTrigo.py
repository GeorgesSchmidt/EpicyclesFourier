import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from math import tau
from matplotlib.animation import PillowWriter

class Circle:
    def __init__(self, x_list, y_list) -> None:
        self.x = x_list
        self.y = y_list
        self.t_list = np.linspace(0, tau, 200)
        self.anim_circle()
        
    def anim_circle(self):
        
        fig = plt.figure(figsize=(15, 5))
        self.ax0 = fig.add_subplot(131)
        self.ax1 = fig.add_subplot(132)
        self.ax2 = fig.add_subplot(133)
    
        anim = animation.FuncAnimation(fig, self.update, frames=len(self.t_list), interval=100, repeat=True)
        # writer = PillowWriter(fps=10)  # FPS peut être ajusté pour contrôler la vitesse du GIF
        # anim.save("nombre_complexes.gif", writer=writer)

        plt.show()
        
    def update(self, i):
        # Met à jour le premier graphique
        self.ax0.cla()
        self.ax0.set_title('cosinus ou x')
        self.ax0.plot(self.t_list, self.x, label='Cosinus')
        self.ax0.axhline(y=0, color='black', linestyle='-')
        self.ax0.plot([self.t_list[i], self.t_list[i]], [0, self.x[i]], 'r-')
        self.ax0.set_xlabel(r'$2\pi$')
        self.ax0.set_ylabel(r'$x$')
        
        
        # Met à jour le deuxième graphique
        self.ax1.cla()
        self.ax1.set_title("sinus ou y")
        self.ax1.plot(self.t_list, self.y, label='Sinus')
        self.ax1.axhline(y=0, color='black', linestyle='-')
        self.ax1.plot([self.t_list[i], self.t_list[i]], [0, self.y[i]], 'r-')
        self.ax1.set_xlabel(r'$t$')
        self.ax1.set_xlabel(r'$2\pi$')
        self.ax1.set_ylabel(r'$y$')
        
        
        # Met à jour le troisième graphique
        self.ax2.cla()
        value = round(self.t_list[i], 2)
        label = fr'$e^{{\alpha = {value}}} = a. \cos(\alpha = {value}) + i.b. \sin(\alpha = {value})$'
        self.ax2.set_title(label)
        self.ax2.plot(self.x, self.y, label='Cercle')
        self.ax2.grid(True)
        self.ax2.axhline(y=0, color='black', linestyle='-')
        self.ax2.axvline(x=0, color='black', linestyle='-')
        self.ax2.plot([0, self.x[i]], [0, self.y[i]], 'ro-')
        self.ax2.invert_yaxis()
        self.ax2.set_xlabel(r'$x$')
        self.ax2.set_ylabel(r'$y$')
        
def main():
    angle = np.linspace(0, tau, 200)
    x, y = [], []
    for a in angle:
        vx = np.cos(a)
        vy = np.sin(a)
        x.append(vx)
        y.append(vy)
    Circle(x_list=x, y_list=y)
    
    x = np.load('../Datas/x_list.npy')
    y = np.load('../Datas/y_list.npy')
    Circle(x_list=x, y_list=y)
        

if __name__ == '__main__':
    main()
