#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-20
# file: curve_fitting_figure_1.5_batch.py
# tested with python 3.7.6
##########################################################################################

import sys
sys.path.append('../lib')
import os
import datetime
import numpy as np

from scipy.optimize import curve_fit

from polynomials import polynomial_horner

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    # load training data (figure 1.5 curve fitting demo)
    training_file = 'prml_ch_01_figure_1.2_training_data_PRNG_seed_523456789.txt'
    assert os.path.isfile(os.path.join(RAWDIR, training_file)), "Data file not found."
    Xt = np.genfromtxt(os.path.join(RAWDIR, training_file))

    assert Xt.shape == (10, 2), "Shape assertion failed."

    N = Xt.shape[0]
    print("training data shape =", Xt.shape)
    print("number of training data points N = ", N)

    # load test data
    test_file = 'prml_ch_01_figure_1.2_test_data_PRNG_seed_123456789.txt'
    X = np.genfromtxt(os.path.join(RAWDIR, test_file))

    assert X.shape == (100, 2), "Shape assertion failed."

    Ntest = X.shape[0]
    print("test data shape =", X.shape)
    print("no. of test data points Ntest = ", Ntest)

    ######################################################################################

    # polynomial curve fitting

    m_order = np.arange(0, 10, 1).astype('int')
    # m_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    res = np.zeros((len(m_order), 3))

    for m in m_order:

        print("m = ", m)
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        print(w)
        print(w.shape)

        # curve fitting
        popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)

        yPredict = polynomial_horner(Xt[:, 0], *popt)

        # test data set prediction
        yPredictTest = polynomial_horner(X[:, 0], *popt)

        # compute sum of squares deviation
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))
        sum_of_squares_error_test = 0.5 * np.sum(np.square(yPredictTest - X[:, 1]))

        RMS = np.sqrt(2.0 * sum_of_squares_error / N)
        RMS_test = np.sqrt(2.0 * sum_of_squares_error_test / Ntest)

        res[m, 0] = m
        res[m, 1] = RMS
        res[m, 2] = RMS_test

    ######################################################################################
    # file i/o
    outname = 'prml_ch_01_figure_1.5_data.txt'
    np.savetxt(os.path.join(RAWDIR, outname),res, fmt = '%.8f')
