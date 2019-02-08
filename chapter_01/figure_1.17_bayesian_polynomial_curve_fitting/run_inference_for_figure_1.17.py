#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-08
# file: bayesian_polynomial_curve_fitting.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import numpy as np

from bayesianPolyCurveFit import bayesianPolyCurveFit

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
    
    # PRML - Bishop - Chapter 1 Introduction - Bayesian Polynomial Curve Fitting
        
    ######################################################################################
    # input file i/o
    
    seedValue = 523456789
    filename = 'prml_ch_01_figure_1.2_training_Data_PRNG-seed_{}.txt'.format(seedValue)
    
    data = np.genfromtxt(os.path.join(RAWDIR, filename))
    assert data.shape[1] == 2, "Error: Shape assertion failed."
    print("data.shape =", data.shape)
    nDatapoints = data.shape[0]
    
    X, T = data[:, 0], data[:, 1] # using the Bishop naming convention
    
    ######################################################################################
    # set (hyper-) parameters for this problem
    alpha = 5.0e-3
    beta = 11.1
    M = 9 # order of polynomial
    xSupport = np.linspace(0.0, 1.0, 301)
    
    res = bayesianPolyCurveFit(xSupport, X, T, alpha, beta, M)
    
    ######################################################################################
    # output file i/o
    
    outname = 'prml_ch_01_figure_1.17_bayesianPolyCurveFit_M_{}.txt'.format(M)
    
    np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.8f')
