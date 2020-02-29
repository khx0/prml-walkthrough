#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-02-26
# file: curve_fitting_figure_1.4_m_0_fit.py
# tested with python 3.7.6
##########################################################################################

'''
Polynomial curve fitting (of degree m = 0)
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

def p_m0(x, w0):
    '''
    w0 = constant bias / offset term
    '''
    return w0

if __name__ == '__main__':

    # load training data (figure 1.2 curve fitting demo)

    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))

    assert Xt.shape == (10, 2), "Error: Shape assertion failed."

    print("Training data shape =", Xt.shape)

    ######################################################################################
    # polynomial curve fitting
    func = p_m0

    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])
    w0 = popt[0]

    print("Fitting parameter:")
    print(popt)

    # create fitted model
    nModelPoints = 800
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = w0 * np.ones_like(xVals)

    X = np.zeros((nModelPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = '.'.join( filename.split('.')[:-1] ) + '_m_0_fit.txt'
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')
