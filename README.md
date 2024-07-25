# EpicyclesFourier

Code pour dessiner les épicycles de Fourier. 

# installation. 

Dans un environnement virtuel :  

`pip install opencv-python matplotlib scipy`

# le module contours.py. 

Ce module permet de rechercher le contour de l'objet d'une image. Il contient la classe mère Contours. 

OpenCV permet de trouver ce contour après une légère transformation de l'image :
l'image doit être binaire (noir ou blanc et non pas en variation de gris). 
l'objet doit être blanc sur un fond noir. 

Si l'on affiche le contour sur l'image, on observe cela :

![Contours Image](Pictures/image_originale.png)

D'une part le contour présente beaucoup de points ce qui ralentira le temps de calcul des coeficients de Fourier et, d'autre part, le contour n'est pas lisse. 

Le module `contours.py` va interpoler le contour de manière à lui donner un nombre de points plus petit (ici 200) avec la fonction `np.interp` et lisser la courbe avec la méthode `signal de scipy`. 

![Contours Image](Pictures/resultat_contour.png)

# Le module epicycles.py. 

La classe Epicycle hérite de Contours, on peux donc lancer le programme directement par ce module. 

Ce programme calcule les coeficients de Fourier nécessaires aux épicyles puis lance l'animation matplotlib. 

Pour calculer ces coeficients, il faut préalablement décomposer les coordonnées x et y des points du contours. 

![Contours Image](Pictures/epicycles.png)


En changeant l'ordre, c'est-à-dire le nombre de coeficients, on risque de trop lisser la courbe résultante. 

A essayer avec un ordre plus petit (ex 3). 

Le programme lance ensuite l'animation matplotlib pour observer les épicycles. 

![Animation epicyles](Pictures/animation_readme.gif)

# Utiliser une FFT : le module transformeeFourier.py

Si l'objectif du programme est d'approcher mathématiquement le contour, la Fast Fourier Transform (FFT) est plus appropriée car beaucoup plus rapide dans le calcul des coeficients. 

Pour calculer une FFT, scipy propose la méthode fft pour calculer les coeficients de Fourier et ifft pour calculer l'inverse et donc récupérer la courbe à partir des coeficients calculés. 

Les coeficients calculés sont des nombres complexes. On peut alors afficher leurs amplitudes et proposer un seuil sous lequel tous les coeficients seront nuls. 

Avec autant de coeficients que de points, la courbe résultante est parfaitement collée à la courbe originale. 

Pour autant, avec moins de coeficients (jusqu'à une ceraine limite), la courbe résultante est toujours représentative de la courbe originale. 

![Animation epicyles](Pictures/animation_readme_fft.gif)






