#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-25
# file: ch_01_curve_fitting_figure_1.5_batch.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import sys
import time
import datetime
import os
import math
import numpy as np

from scipy.optimize import curve_fit

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)

def poly_horner(x, coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result*x + coeff[i]
    return result

if __name__ == '__main__':
    
    # load training data (figure 1.2 curve fitting demo)
    
    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))
    
    assert Xt.shape == (10, 2), "Error: Shape assertion failed."
    
    print("Training data shape =", Xt.shape)
    
    ######################################################################################
    
    # polynomial curve fitting
    
    mOrder = np.arange(0, 10, 1)
    
    print mOrder
    
    m = mOrder[1]
    
    w = np.zeros((m + 1,))
    
    func = lambda x : poly_horner(x, w)
    
    p0 = np.ones((m + 1, 1))
    
    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])
    
    
    
    '''
    
    popt, pcov = curve_fit(func, Xt[:, 0], Xt[:, 1])
    
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
    
    outname = '.'.join( filename.split('.')[:-1] ) + '_m9_fit.txt'
    
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')

    '''
    
    
    
