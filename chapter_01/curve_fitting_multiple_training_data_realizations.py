#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-09-09
# file: curve_fitting_multiple_training_data_realizations.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
##########################################################################################

import sys
sys.path.append('../lib')
import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib.ticker import FuncFormatter

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

from scipy.optimize import curve_fit

from polynomials import polynomial_horner

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)
os.makedirs(RAWDIR, exist_ok = True)

def createTrainingData(N, mu, sigma):
    # Xt = training data set
    xtVals = np.linspace(0.0, 1.0, N)
    ytVals = np.sin(2.0 * np.pi * xtVals) + np.random.normal(mu, sigma, xtVals.shape)
    # create N training data points (N = 10)
    Xt = np.zeros((N, 2))
    Xt[:, 0] = xtVals
    Xt[:, 1] = ytVals
    return Xt

def polynomialCurveFitting(mOrder, Xt):

    res = np.zeros((len(mOrder), 2))

    for m in mOrder:

        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))

        # curve fitting
        popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)

        yPredict = polynomial_horner(Xt[:, 0], *popt)

        # compute sum of squares deviation
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))

        RMS = np.sqrt(2.0 * sum_of_squares_error / N)

        res[m, 0] = m
        res[m, 1] = RMS

    return res

if __name__ == '__main__':

    tries_list = [50]

    # parameters for each training data batch of sample size N
    N = 10
    mu = 0.0
    sigma = 0.3

    maxOrder = 10
    # polynomial curve fitting
    mOrder = np.arange(0, maxOrder, 1).astype('int')

    # fixed test data for all training realizations    
    test_file = 'prml_ch_01_figure_1.2_test_data_PRNG-seed_123456789.txt'
    X = np.genfromtxt(os.path.join(RAWDIR, test_file))
    assert X.shape == (100, 2), "Error: Shape assertion failed."
    
    print(X.shape)

    # number of independent training data realizations
    for tries in tries_list:

        # fix random seed for reproducibility
        np.random.seed(123456789)

        XFull = np.zeros((maxOrder, tries + 1))
        XFull[:, 0] = mOrder # fill independent axis

        for i in range(tries):

            # create training data
            Xt = createTrainingData(N, mu, sigma)
            assert Xt.shape[0] == N, "Error: Xt.shape[0] == N assertion failed."
            Et = polynomialCurveFitting(mOrder, Xt)
            XFull[:, i + 1] = Et[:, 1]
        

    
        '''

        XSummary = np.zeros((maxOrder, 3))
        XSummary[:, 0] = np.arange(0, maxOrder, 1).astype('int')

        for i in range(maxOrder):
            XSummary[i, 1] = np.mean(XFull[i, 1:])
            XSummary[i, 2] = np.std(XFull[i, 1:])

        # global plot settings
        xFormat = [-0.5, 9.5, 0.0, 9.1, 3.0, 1.0]
        yFormat = [0.0, 1.00, 0.0, 1.05, 0.5, 0.5]

        outname = r'prml_ch_01_figure_1.5_training_error_only_average' + \
            '_y_error_bar_n_{}'.format(tries)

        # call the plotting function
        outname = Plot_Avg(titlestr = '',
                           X = XFull,
                           Y = XSummary,
                           outname = outname,
                           outdir = OUTDIR,
                           pColors = pColors,
                           grid = False,
                           drawLegend = True,
                           xFormat = xFormat,
                           yFormat = yFormat,
                           mode = 'y_error_bar')

        xFormat = [0.0, 9.5, 0.0, 9.1, 3.0, 1.0]

        outname = r'prml_ch_01_figure_1.5_training_error_only_average' + \
            '_y_error_continuous_n_{}'.format(tries)

        # call the plotting function
        outname = Plot_Avg(titlestr = '',
                           X = XFull,
                           Y = XSummary,
                           outname = outname,
                           outdir = OUTDIR,
                           pColors = pColors,
                           grid = False,
                           drawLegend = True,
                           xFormat = xFormat,
                           yFormat = yFormat,
                           mode = 'y_error_continuous')

        '''
