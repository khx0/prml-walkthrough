#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-22
# file: create_figure_1.2_training_data.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import numpy as np

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':
    
    # PRML - Bishop - Chapter 1 Introduction - Curve Fitting
    # figure 1.2 training data
    
    ######################################################################################
    # noise settings
    
    # fix random number seed for reproducibility
    seedValue = 523456789
    seed = np.random.seed(seedValue)
    
    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    mu = 0.0
    sigma = 0.3
    
    # number of training data points
    # Xtrain = training data set
    # create N training data points (N = 10)
    N = 10
    xtVals = np.linspace(0.0, 1.0, N)
    ytVals = np.sin(2.0 * np.pi * xtVals) + np.random.normal(mu, sigma, xtVals.shape) 
    Xtrain = np.zeros((N, 2))
    Xtrain[:, 0] = xtVals
    Xtrain[:, 1] = ytVals
    
    ######################################################################################
    # file i/o
    outname = 'prml_ch_01_figure_1.2_training_Data_PRNG-seed_{}.txt'.format(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname), Xtrain, fmt = '%.8f')
