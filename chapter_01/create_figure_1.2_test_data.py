#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-01-04
# file: create_figure_1.2_test_data.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import os
import datetime
import numpy as np

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
    
    # PRML - Bishop - Chapter 1 Introduction - Curve Fitting
    # figure 1.2 test data
    
    ######################################################################################
    # noise settings
    
    # fix random number seed for reproducibility
    seedValue = 123456789
    seed = np.random.seed(seedValue)
    
    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    mu = 0.0
    sigma = 0.3
    
    # number of test data points
    # Xtest = test data set
    # create N test data points (N = 100)
    N = 100
    Xtest = np.zeros((N, 2))
    xVals = np.linspace(0.0, 1.0, N)
    yVals = np.array([np.sin(2.0 * np.pi * x) + np.random.normal(mu, sigma) 
                      for x in xVals])
    Xtest[:, 0] = xVals
    Xtest[:, 1] = yVals
    
    ######################################################################################
    # file i/o
    
    outname = 'prml_ch_01_figure_1.2_test_data_PRNG-seed_{}.txt'.format(seedValue)
    
    np.savetxt(os.path.join(RAWDIR, outname), Xtest, fmt = '%.8f')
