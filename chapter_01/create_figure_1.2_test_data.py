#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-18
# file: create_figure_1.2_test_data.py
# tested with python 3.7.6
##########################################################################################

import os
import datetime
import numpy as np

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    # PRML - Bishop - Chapter 1 Introduction - Curve Fitting
    # figure 1.2 test data

    ######################################################################################
    # noise settings

    # fix random number seed for reproducibility
    seed_value = 123456789
    np.random.seed(seed_value)

    ##########################################################
    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    ##########################################################
    mu = 0.0
    sigma = 0.3

    # number of test data points
    # Xtest = test data set
    # create N test data points (N = 100)
    N = 100
    xVals = np.linspace(0.0, 1.0, N)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)
    Xtest = np.zeros((N, 2))
    Xtest[:, 0] = xVals
    Xtest[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = f'prml_ch_01_figure_1.2_test_data_PRNG_seed_{seed_value}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), Xtest, fmt = '%.8f')
