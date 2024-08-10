# Code pour utiliser les transformées de Fourier en Python. 

Ce repo contient les codes pour utiliser différents codes proposés par les bibliothèques Python telles que numpy, scipy et opencv afin de calculer les transformées de Fourier sur un contour. 

Sur environnement virtuel :  

`pip install opencv-python matplotlib scipy`

Pour les tests :

`python3 -m unittest discover Tests`


# le module principal : showContour.py. 

Ce module utilise ceux présents dans le dossier `Contour` pour afficher sous matplotlib le résultat des différents modules. 

`python3 showContour.py Pictures/pi.jpg`

# Le dossier Contour. 

Ce dossier contient les modules permettant :  

- d'extraire un contour pour le module `getContour.py`. 
- d'interpoler ce contour pour le module `ìnterpolate.py`. 
- de lisser ce contour pour le module `lissage.py`. 

## le module getContour.py

Le module `getContour.py` prend en entrée le chemin d'une image, ici l'image de pi située dans le dossier `Pictures`. 
Il recherche le contour le plus grand dans cette image après lecture de celle-ci en noir et blanc. 
Il est important que l'objet à analyser ai le plus grand des contours dans l'image. 
L'objet doit être blanc sur un fond noir. 
Il décompose ensuite ce contour en x et en y par rapport au centre du contour. 

On remarque que le contour présente plus de 5000 points, ce qui peut ralentir les calculs des transformées de Fourier. 


## le module interolate.py. 

Ce module permet de donner un nombre plus petit (ou plus grand) de points dans le contour. 
Par défaut, on donne 200 points, ce qui donne des temps de calculs résonnables tout en ayant un nombre de points suffisant pour garder la forme.

## le module liss.py. 

ce module permet de lisser un contour. 

meme si les tramsformees de Fourier lissent elles aussi les contours 

ce lissage préalable aide a la compréhension de la décomposition des coordonnées. 






