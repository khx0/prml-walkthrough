
@ figure 1.23:
It does not say so in the text, but Bishop used $\sigma = 0.5$ for the
Gaussian distributions underlying this example.

@ figure 1.24:
The three colors used in this figure are the same colors as before using
a different alpha value.
For me alpha = 0.5 seemed to be quite close to the print version of the book.

pColors = {'green': '#00FF00', # neon green
           'red':   '#FF0000', # standard red
           'blue':  '#0000FF'} # standard blue

Plotting Defaults

linewidth = 0.5 pt

Spyder Integration

Python 3.7.0 Compatibility

Unit test and independent class implementation of the poly_horner function,
plus correct credits.

Use pytest for unit testing.

Agenda:
* switch to today = strftime from python's datetime module
* switch to np.save / np.load using *.npy
* outsource a plotting library containing all subroutines and all color and linewidht settings; create style templates for this purpose.
* Sandbox the whole python environment (either using an appropriate conda yaml file or by dockerizing the entire framework)
Make sure the plot production is thus robust against software platform changes.
* Add polynomal class (using Horner scheme)
* Add polynomal least square fit class
* Add unit tests for both cases
* Add unit test to check that the polynomial least squares with reg
is identical to the polynomial least squares without reg when lambda = 0
