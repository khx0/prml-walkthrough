#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-20
# file: curve_fitting_figure_1.5_batch_training_data_only.py
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

    ######################################################################################
    # polynomial curve fitting

    m_order = np.arange(0, 10, 1).astype('int')
    # m_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    fitparameter_file = 'prml_ch_01_curve_fitting_parameter_results.txt'

    f = open(os.path.join(RAWDIR, fitparameter_file), 'w')

    line = '\t M = 0 \t M = 1 \t M = 3 \t M = 9 \n'
    f.write(line)

    res = np.zeros((len(m_order), 2))

    for m in m_order:

        print("m = ", m)
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        print(w)
        print(w.shape)

        # curve fitting
        popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)

        yPredict = polynomial_horner(Xt[:, 0], *popt)

        # compute sum of squares deviation
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))

        RMS = np.sqrt(2.0 * sum_of_squares_error / N)

        res[m, 0] = m
        res[m, 1] = RMS

    ######################################################################################
    # file i/o
    f.close()
    outname = 'prml_ch_01_figure_1.5_training_error.txt'
    np.savetxt(os.path.join(RAWDIR, outname),res, fmt = '%.8f')
