#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-22
# file: curve_fitting_figure_1.4_m_9_fit.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

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

def p_m9(x, w0, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    return w0 + w1 * x + w2 * x ** 2 + w3 * x ** 3 + w4 * x ** 4 + w5 * x ** 5 + \
           w6 * x ** 6 + w7 * x ** 7 + w8 * x ** 8 + w9 * x ** 9

if __name__ == '__main__':
    
    # load training data (figure 1.2 curve fitting demo)
    
    # Xt = training data
    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))
    
    assert Xt.shape == (10, 2), "Error: Shape assertion failed."
    
    print("Training data shape =", Xt.shape)
    
    ######################################################################################
    # polynomial curve fitting
    
    func = p_m9
    
    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])
    
    print("Fitting parameter:")
    print(popt)
    
    # create fitted model
    
    nModelPoints = 800
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = np.array([popt[0] + popt[1] * x + popt[2] * x ** 2 + popt[3] * x ** 3 + \
        popt[4] * x ** 4 + popt[5] * x ** 5 + popt[6] * x ** 6 + popt[7] * x ** 7 + \
        popt[8] * x ** 8 + popt[9] * x ** 9 for x in xVals])
    
    X = np.zeros((nModelPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    ######################################################################################
    # file i/o
    outname = '.'.join( filename.split('.')[:-1] ) + '_m_9_fit.txt'
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')
