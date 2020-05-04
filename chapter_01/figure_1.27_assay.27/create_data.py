#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-05-04
# file: create_data.py
# tested with python 3.7.6
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

    yVals = 0.4 * norm.pdf(xVals, loc = loc1, scale = np.sqrt(0.004))
    yVals += 0.95 * norm.pdf(xVals, loc = loc2, scale = np.sqrt(0.01))
    X[:, 1] = 0.48 * yVals

    yVals = 0.86 * norm.pdf(xVals, loc = loc3, scale = np.sqrt(0.0075))
    X[:, 2] = yVals

    # save data
    outname = 'prml_ch_01_figure_1.27_p_of_x_given_C_k_conditional_prior_data.npy'
    np.save(os.path.join(RAWDIR, outname), X)

    # Note, that as opposed to figure 1.24 and 1.26 in chapter 1, here
    # the data that we start with is already a conditional distribution
    # p(x | C_k), which is related to the joint distribution as used in 
    # figure 1.24 by the product rule
    # p(x, C_k) = p(x | C_k) * p(C_k).

    ######################################################################################
    ######################################################################################

    # compute normalization of p(x | C_1) and p(x| C_2)
    norm_01 = np.trapz(X[:, 1], X[:, 0])
    norm_02 = np.trapz(X[:, 2], X[:, 0])
    norm = norm_01 + norm_02

    X[:, 1] /= norm_01
    X[:, 2] /= norm_02

    ######################################################################################
    # Marginalization:
    # Having computed the normalization of p(x | C_k) we can directly state the values
    # for the marginalized distribution p(C_k), where k = {1, 2}.
    # Here we find:
    pC1 = norm_01 / norm
    pC2 = norm_02 / norm
    assert np.isclose((pC1 + pC2), 1.0), \
        "Error: Normalization assertion failed."

    '''
    # Next, we also find the probability distribution p(X) by marginalization:
    pX = (X[:, 1] * norm_01 + X[:, 2] * norm_02) / norm
    assert np.isclose(np.trapz(pX, X[:, 0]), 1.0), \
        "Error: Normalization assertion failed."
    ######################################################################################

    # Compute posterior conditional probability distributions

    pC1_given_x = X[:, 1] * pC1 / pX
    pC2_given_x = X[:, 2] * pC2 / pX

    # save data
    data = np.zeros((nVisPoints, 3))
    data[:, 0] = X[:, 0]
    data[:, 1] = pC1_given_x
    data[:, 2] = pC2_given_x

    outname = 'prml_ch_01_figure_1.27_p_of_C_k_given_x_data.npy'
    np.save(os.path.join(RAWDIR, outname), data)
    '''