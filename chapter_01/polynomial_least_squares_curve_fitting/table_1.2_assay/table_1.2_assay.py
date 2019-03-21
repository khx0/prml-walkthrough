#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-21
# file: table_1.2_assay.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import sys
sys.path.append('../')
import os
import datetime
import numpy as np

from polyLeastSquares import polyLeastSquaresReg

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)

if __name__ == '__main__':
    
    # PRML Bishop chapter 1 Introduction - Curve Fitting - table 1.2 assay
    
    ######################################################################################
    # create training data
    nTrain = 10
    mu = 0.0
    sigma = 0.3
    seedValue = 523456789
    np.random.seed(seedValue)
    
    xVals = np.linspace(0.0, 1.0, nTrain)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape) 
    Xt = np.zeros((nTrain, 2))
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals
    ######################################################################################
    
    # polynomial fitting degree
    m = 9
    regVals = [0.0, np.exp(-7.0), np.exp(0.0)]
    
    res = np.zeros((len(regVals), m + 1))
    
    for i, regVal in enumerate(regVals):
        
        # polynomial curve fitting (learning the model)
        w = polyLeastSquaresReg(m, Xt, regVal)        
        res[i, :] = w
    
    ######################################################################################
    # file i/o
    outname = 'table_1.2_coefficient_table_PRNG-seed_%d.txt' %(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.2f')
    ######################################################################################
