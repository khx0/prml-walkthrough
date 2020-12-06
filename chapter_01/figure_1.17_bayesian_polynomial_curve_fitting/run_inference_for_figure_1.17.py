#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-12-06
# file: run_inference_for_figure_1.17.py
# tested with python 3.7.6
##########################################################################################

import os
import datetime
import numpy as np

from BayesianPolyCurveFit import BayesianPolyCurveFit

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    # PRML - Bishop - Chapter 1 Introduction - Bayesian Polynomial Curve Fitting

    ######################################################################################
    # input file i/o

    seed_value = 523456789
    filename = f'prml_ch_01_figure_1.2_training_Data_PRNG_seed_{seed_value}.txt'

    data = np.genfromtxt(os.path.join(RAWDIR, filename))
    assert data.shape[1] == 2, "Shape assertion failed."
    print("data.shape =", data.shape)
    n_datapoints = data.shape[0]

    X, T = data[:, 0], data[:, 1] # using the Bishop naming convention

    ######################################################################################
    # set (hyper-) parameters for this problem
    alpha = 5.0e-3
    beta = 11.1
    M = 9 # order of polynomial
    xSupport = np.linspace(0.0, 1.0, 301)

    res = BayesianPolyCurveFit(xSupport, X, T, alpha, beta, M)

    ######################################################################################
    # output file i/o
    outname = f'prml_ch_01_figure_1.17_bayesianPolyCurveFit_M_{M}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.8f')
