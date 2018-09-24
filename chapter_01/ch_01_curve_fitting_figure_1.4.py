#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-24
# file: ch_01_curve_fitting_figure_1.4.py
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

def p_m0(x, w0):
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
    
    # create fitted model
    
    nModelPoints = 800
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = np.array([popt[0] for x in xVals])
    
    X = np.zeros((nModelPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # file i/o
    
    outname = '.'.join( filename.split('.')[:-1] ) + '_m0_fit.txt'
    
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')

    
    
    
    
