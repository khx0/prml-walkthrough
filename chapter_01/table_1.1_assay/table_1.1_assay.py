#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-07
# file: table_1.1_assay
# tested with python 3.7.6
##########################################################################################

import sys
sys.path.append('../../lib')
import os
import datetime
import numpy as np

from scipy.optimize import curve_fit

from polynomials import polynomial_horner

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

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
    xVals = np.linspace(0.0, 1.0, nTrain)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)
    Xt = np.zeros((nTrain, 2))
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals

    ######################################################################################
    # polynomial curve fitting (learning the model)

    mOrder = np.array([0, 1, 3, 9])

    outname = f'table_1.1_data_PRNG-seed_{seedValue}.txt'

    with open(os.path.join(RAWDIR, outname), 'w') as f:

        for m in mOrder:

            # create coefficient vector (containing all fit parameters)
            w = np.ones((m + 1,))

            # curve fitting
            popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)

            line = ''
            for i in range(len(popt)):
                line += '%.2f \t' %(popt[i])
            line += '\n'
            f.write(line)
