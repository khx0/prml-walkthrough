#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-07
# file: polynomial_least_squares_figure_1.4.py
# tested with python 3.7.6
##########################################################################################

import sys
sys.path.append('../../lib')
import os
import datetime
import numpy as np

from polynomials import polynomial_horner
from polyLeastSquares import polyLeastSquares

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    ######################################################################################
    # load training data (figure 1.2 curve fitting demo)

    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))

    assert Xt.shape == (10, 2), "Error: Shape assertion failed."

    print("Training data shape =", Xt.shape)

    seedValue = 523456789

    ######################################################################################
    # polynomial fitting orders
    jobs = [0, 1, 3, 9]

    for m in jobs:

        # polynomial least squares fitting
        w = polyLeastSquares(m, Xt)
        print("fitted weights =", w)

        # create fitted model
        nModelPoints = 800
        xVals = np.linspace(0.0, 1.0, nModelPoints)
        yVals = polynomial_horner(xVals, *w)
        Xm = np.zeros((nModelPoints, 2))
        Xm[:, 0] = xVals
        Xm[:, 1] = yVals

        ##################################################################################
        # file i/o
        outname = f'prml_ch_01_figure_1.2_training_data_PRNG-seed_{seedValue}_m_{m}_fit.txt'
        np.savetxt(os.path.join(RAWDIR, outname), Xm, fmt = '%.8f')
        ##################################################################################
