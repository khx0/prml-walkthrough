#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-27
# file: table_1.1_assay
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import sys
import time
import datetime
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

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

def poly_horner(x, *coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result*x + coeff[i]
    return result

def poly_horner2(x, coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result*x + coeff[i]
    return result

if __name__ == '__main__':
    
    # PRML Bishop chapter 1 Introduction - Curve Fitting - table 1.1 assay
    
    ######################################################################################
    # global parameters
    nTrain = 10

    # noise settings
    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    mu = 0.0
    sigma = 0.3
    
    # fix random number seed for reproducibility
    # seedValue = 123456789 gives a nice figure like fig. 1.5 in the book
    seedValue = 123456789
    seed = np.random.seed(seedValue)
    
    ######################################################################################
    # create training data
    Xt = np.zeros((nTrain, 2))
    xVals = np.linspace(0.0, 1.0, nTrain)
    yVals = np.array([np.sin(2.0 * np.pi * x) + np.random.normal(mu, sigma) 
                      for x in xVals])
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals
    
    ######################################################################################
    # polynomial curve fitting (learning the model)
        
    mOrder = np.array([0, 1, 3, 9])
    
    outname = 'table_1.1_data_PRNG-seed_%d.txt' %(seedValue)
    
    f = open(os.path.join(RAWDIR, outname), 'w')
        
    for m in mOrder:
        
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        
        # curve fitting
        popt, pcov = curve_fit(poly_horner, Xt[:, 0], Xt[:, 1], p0 = w)
        
        line = ''
        for i in range(len(popt)):
            line += '%.2f \t' %(popt[i])
        line += '\n'
        f.write(line)
        
    f.close()
    
    ######################################################################################
    # file i/o
    
    # np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.8f')
    
    
    
