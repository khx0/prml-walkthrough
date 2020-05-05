#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-05-05
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

    ######################################################################################
    # Comment 1
    # Note, that as opposed to figure 1.24 and 1.26 in chapter 1, here
    # the data that we start with is already a conditional (prior) distribution
    # p(x | C_k), which is related to the joint distribution as used in 
    # figure 1.24 by the product rule of probability
    # p(x, C_k) = p(x | C_k) * p(C_k).
    # All information about the problem is fully contained in the full joint distribution,
    # such that all quantities can easily be derived from this.
    # Since we here start from prior conditional distributions, we have to make
    # additional assumptions about the prior class probabilities p(C_k) in order to derive
    # at posterior quantities. We did not have to do this in figure 1.24 assay since we
    # there started from the full joint probability distribution p(x, C_k).
    # Make sure that you appreciate this subtle difference by starting from a different
    # quantity to begin with.
    ######################################################################################

    ######################################################################################
    # Comment 2
    # Normally prior conditional probability distributions, sucht as the here considered
    # p(x | C_k)'s are properly normalized probability distributions.
    # This can be easily seen from the following argument:
    # p(C_k) = \int p(x,C_k) dx = \int p(x | C_k) p(C_k) dx = p(C_k) * \int p(x | C_k) dx
    # Here the first equality is the standard marginalization, and then we simply used 
    # the product rule of probability. From this line above we can cross out the p(C_k) 
    # and arrive at
    # \int p(x | C_k) dx = 1, which is the normalization condition for p(x | C_k).
    ######################################################################################
    # However, as shown in the left part of figure 1.27, theses densities (at least in the
    # way how I tried to model them) are not normalized densities. To reproduce the 
    # results as they look in figure 1.27 (left), I simply save the data for the plotting 
    # of the left figure unnormalized. Here I modelled that data by visual inspection by 
    # a scaled sum of manually adjusted normal distributions, as can be seen in this 
    # script. For the further derivations below I will first normalize these 
    # distributions, which form the starting point for the calculation of the conditional 
    # posterior distributions, as shown in figure 1.27 (right).
    ######################################################################################











    
    '''

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
        
    print(norm_01)
    print(norm_02)
    print(norm)

    

    # TODO, try if this also works with p(C_1) = p(C_2) = 0.5 here and plot the results.



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