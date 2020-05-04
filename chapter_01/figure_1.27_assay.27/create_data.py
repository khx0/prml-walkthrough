#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-05-04
# file: create_data.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.1
##########################################################################################

import os
import datetime
import numpy as np

from scipy.stats import norm

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    ##############################################
    # PRML Bishop Chapter 1 Introduction
    # create data for figure 1.27
    ##############################################

    nVisPoints = 3000
    X = np.zeros((nVisPoints, 3))
    xVals = np.linspace(-1.5, 1.5, nVisPoints)
    X[:, 0] = xVals

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    # location (mean) of the normal distributions used in this example
    loc1 = 0.2
    loc2 = 0.5
    loc3 = 0.7







    yVals = 0.59 * norm.pdf(xVals, loc = loc1, scale = np.sqrt(0.33))
    yVals += 0.2 * norm.pdf(xVals, loc = loc2, scale = np.sqrt(0.24))
    X[:, 1] = yVals

    yVals = 0.80 * norm.pdf(xVals, loc = loc2, scale = np.sqrt(0.36))
    X[:, 2] = yVals

    # compute normalization of p(x, C_1) and p(x, C_2)
    norm_01 = np.trapz(X[:, 1], X[:, 0])
    norm_02 = np.trapz(X[:, 2], X[:, 0])
    norm = norm_01 + norm_02

    X[:, 1] /= norm
    X[:, 2] /= norm

    # save data
    outname = 'prml_ch_01_figure_1.24_p_of_x_and_C_k_data.npy'
    np.save(os.path.join(RAWDIR, outname), X)

    ######################################################################################
    # Marginalization:
    # Having computed the normalization of p(x, C_k) we can directly state the values
    # for the marginalized distribution p(C_k), where k = {1, 2}.
    # Here we find:
    pC1 = norm_01 / norm
    pC2 = norm_02 / norm
    assert np.isclose((pC1 + pC2), 1.0), \
        "Error: Normalization assertion failed."

    # Next, we also find the probability distribution p(X) by marginalization:
    pX = X[:, 1] + X[:, 2]
    assert np.isclose(np.trapz(pX, X[:, 0]), 1.0), \
        "Error: Normalization assertion failed."
    ######################################################################################

    # Compute posterior conditional probability distributions

    pC1_given_x = X[:, 1] / pX
    pC2_given_x = X[:, 2] / pX

    # save data
    data = np.zeros((nVisPoints, 3))
    data[:, 0] = X[:, 0]
    data[:, 1] = pC1_given_x
    data[:, 2] = pC2_given_x

    outname = 'prml_ch_01_figure_1.26_p_of_C_k_given_x_data.npy'
    np.save(os.path.join(RAWDIR, outname), data)
