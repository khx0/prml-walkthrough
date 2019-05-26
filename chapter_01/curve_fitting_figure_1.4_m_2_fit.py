#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-04-10
# file: curve_fitting_figure_1.4_m_2_fit.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

'''
Polynomial curve fitting (of degree m = 2)
using scipy's curve_fit functionality.
'''

import os
import datetime
import numpy as np
from scipy.optimize import curve_fit

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

def p_m2(x, w0, w1, w2):

    return w0 + w1 * x + w2 * x ** 2

if __name__ == '__main__':

    # load training data (figure 1.2 curve fitting demo)

    # Xt = training data
    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))

    assert Xt.shape == (10, 2), "Error: Shape assertion failed."

    print("Training data shape =", Xt.shape)

    ######################################################################################
    # polynomial curve fitting

    func = p_m2

    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])

    print("Fitting parameter:")
    print(popt)

    # create fitted model

    nModelPoints = 800
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = np.array([popt[0] + popt[1] * x + popt[2] * x ** 2 for x in xVals])

    X = np.zeros((nModelPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = '.'.join( filename.split('.')[:-1] ) + '_m_2_fit.txt'
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')
