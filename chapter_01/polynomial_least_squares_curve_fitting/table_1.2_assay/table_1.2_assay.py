#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-07
# file: table_1.2_assay.py
# tested with python 3.7.6
##########################################################################################

import sys
sys.path.append('../')
import os
import datetime
import numpy as np

from polyLeastSquares import polyLeastSquaresReg

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

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
    outname = f'table_1.2_coefficient_table_PRNG-seed_{seedValue}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.2f')
    ######################################################################################
