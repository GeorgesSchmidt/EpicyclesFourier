# EpicyclesFourier

Code to draw Fourier epicycles and implement Fourier transforms in Python.

This repository only includes code to implement various approaches to Fourier transforms using the scipy and numpy modules.

It does not include any mathematical background or explanations.

### THE README PRESENTED HERE INCLUDES GIF ANIMATIONS. PLEASE WAIT FOR IT TO LOAD, THIS MAY TAKE A FEW SECONDS ###

# installation. 

In a virtual environment :  

`pip install opencv-python matplotlib scipy`

# The contours.py Module. 

This module allows you to find the contour of an object in an image. It contains the base class Contours.

OpenCV is used to find this contour after a slight transformation of the image:

The image must be binary (black or white, not grayscale).
The object should be white on a black background.
If we display the contour on the image, it looks like this:  

![Contours Image](Pictures/image_originale.png)

On the one hand, the contour has many points, which will slow down the computation time for the Fourier coefficients, and on the other hand, the contour is not smooth.

The `contours.py` module will interpolate the contour to reduce the number of points (in this case, 200) using the np.interp function and smooth the curve with the signal method from scipy.  

![Contours Image](Pictures/resultat_contour.png)

# The epicycles.py Module

The Epicycle class inherits from Contours, so you can run the program directly through this module.

This program calculates the Fourier coefficients needed for the epicycles and then starts the matplotlib animation.

To calculate these coefficients, you first need to decompose the x and y coordinates of the contour points.

![Contours Image](Pictures/epicycles.png)


By changing the order, i.e., the number of coefficients, you might over-smooth the resulting curve.

Try using a smaller order (e.g., 3).

The program then starts the matplotlib animation to observe the epicycles.

![Animation epicyles](Pictures/animation_readme.gif)

# Using an FFT: The transformeeFourier.py Module

If the goal of the program is to mathematically approximate the contour, the Fast Fourier Transform (FFT) is more appropriate because it is much faster at calculating the coefficients.

To calculate an FFT, scipy offers the fft method to compute the Fourier coefficients and ifft to calculate the inverse and thus recover the curve from the calculated coefficients.

The calculated coefficients are complex numbers. We can then display their amplitudes and set a threshold below which all coefficients will be zero.

With as many coefficients as points, the resulting curve perfectly matches the original curve.

However, even with fewer coefficients (up to a certain limit), the resulting curve remains representative of the original curve.

![Animation epicyles](Pictures/animation_readme_fft.gif)

# Using a 2D-DFT on Images: The imageFourier.py Module

This type of modeling is widely used in image processing. It allows you to compute the Fourier transform on a matrix.

The image provided should be black and white.

In our case, the image contains only black or white pixels.

By applying a 2D-DFT, provided by OpenCV, we compute the spectral image, represented here in 3D, which is the representation of the amplitudes of the Fourier coefficients found.

We then apply a mask, represented by a black rectangle of a given size, where all coefficients outside this mask will be set to zero.

If the mask is as large as the image:

![Contours Image](<Pictures/image_DFT_[50, 50].png>)

If the mask is twice as small:

![alt text](<Pictures/image_DFT_[25, 25].png>)

If the mask is 10 times smaller:

![alt text](<Pictures/image_DFT_[5, 5].png>)







