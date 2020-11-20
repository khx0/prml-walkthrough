#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-20
# file: curve_fitting_figure_1.4_m_9_fit.py
# tested with python 3.7.6
##########################################################################################

'''
Polynomial curve fitting (of degree m = 9)
using scipy's curve_fit functionality.
'''

import os
import datetime
import numpy as np
from scipy.optimize import curve_fit

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

def p_m9(x, w0, w1, w2, w3, w4, w5, w6, w7, w8, w9):

    return w0 + w1 * x + w2 * x ** 2 + w3 * x ** 3 + w4 * x ** 4 + w5 * x ** 5 + \
           w6 * x ** 6 + w7 * x ** 7 + w8 * x ** 8 + w9 * x ** 9

if __name__ == '__main__':

    # load training data (figure 1.2 curve fitting demo)

    # Xt = training data
    filename = 'prml_ch_01_figure_1.2_training_data_PRNG_seed_523456789.txt'
    assert os.path.isfile(os.path.join(RAWDIR, filename)), "Data file not found."
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))

    assert Xt.shape == (10, 2), "Shape assertion failed."
    print("training data shape =", Xt.shape)

    ######################################################################################
    # polynomial curve fitting

    func = p_m9

    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])

    print("fitting parameter:")
    print(popt)

    # create fitted model
    n_modelpoints = 800
    xVals = np.linspace(0.0, 1.0, n_modelpoints)
    yVals = np.array([popt[0] + popt[1] * x + popt[2] * x ** 2 + popt[3] * x ** 3 + \
        popt[4] * x ** 4 + popt[5] * x ** 5 + popt[6] * x ** 6 + popt[7] * x ** 7 + \
        popt[8] * x ** 8 + popt[9] * x ** 9 for x in xVals])

    X = np.zeros((n_modelpoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = os.path.splitext(filename)[0] + '_m_9_fit.txt'
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')
