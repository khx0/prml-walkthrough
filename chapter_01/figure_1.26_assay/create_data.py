#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-05-06
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
    # create data for figure 1.24 and figure 1.26
    ##############################################

    nVisPoints = 3000
    X = np.zeros((nVisPoints, 3))
    xVals = np.linspace(-1.5, 8.5, nVisPoints) # define the x-domain on which we operate
    X[:, 0] = xVals

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    # location (mean(s)) of the normal distribution(s) used in this example
    loc1 = 1.6
    loc2 = 3.5
    xHat_pos = loc2
    x0_pos = 2.4

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

    ######################################################################################
    # In this way, as set up here, the data contained in X describes the full information
    # about the joint distribution p(x,C_k), which is a properly normalized
    # probability distribution.
    # The normalization condition for the joint distribution in this case reads
    # $\mathcal{N} = \sum_k \int p(x,C_k) dx = 1$, where the integral over x runs over the
    # full x domain.
    ######################################################################################

    # check normalization
    _norm = np.trapz(X[:, 1], X[:, 0]) + np.trapz(X[:, 2], X[:, 0])
    assert np.isclose(_norm, 1.0), "Error: Normalization condition of joint distribution failed."

    # save data
    outname = 'prml_ch_01_figure_1.24_p_of_x_and_C_k_joint_data.npy'
    np.save(os.path.join(RAWDIR, outname), X)

    ######################################################################################
    # Marginalization:
    # Having computed the normalization of the joint distribution p(x, C_k), 
    # we can directly state the values for the marginalized distribution p(C_k), 
    # where k = {1, 2}.
    # Here we find:
    pC1 = norm_01 / norm
    pC2 = norm_02 / norm
    # Check for normalization of the marginalized class (prior) probability p(C_k).
    assert np.isclose((pC1 + pC2), 1.0), \
        "Error: Normalization assertion failed."

    # Next, we also compute the probability distribution p(X) by marginalization:
    pX = X[:, 1] + X[:, 2]
    # Check for normalization of the marginalized distribution p(X).
    assert np.isclose(np.trapz(pX, X[:, 0]), 1.0), \
        "Error: Normalization assertion failed."
    ######################################################################################

    # Compute posterior conditional probability distributions:

    ######################################################################################
    # Computing the desired posterior conditional distributions can be done easily having
    # the joint distribution available. E.g. for p(C_1| x), we simply do the following:
    # For a given, arbitrary but fixed value of x, we simply get this wanted value as the
    # ratio
    # p(C_1| x) = p(x, C_1) / ( p(x, C_1) + p(x, C_2) ).
    # Since this is valid for any x, we can compute this in a vectorized form as
    # p(C_1 | x) = p(x, C_1) / p(x), since p(x) = p(x,C_1) + p(x,C_2).
    # This is what we use below to compute the targeted conditional posteriors.
    # This obviously works analogously for p(C_2 | x).
    ######################################################################################
    # Alternatively we could confirm the same result invoking Bayes theorem.
    # First we would start from the product-rule of probability theory, which states
    # p(X,Y) = p(X|Y) * p(Y). With this relation, we can rewrite 
    # p(x | C_1) = p(x, C_1) / p(C_1). Eventually we are looking for p(C_1 | x). According
    # to Bayes theorem, we have
    # p(x, C_1) / p(C_1) = p(x | C_1) = p(C_1 | x) * p(x) / p(C_1).
    # Isolating the left and right hand side of the above equation for p(C_1 | x) gives
    # p(C_1 | x) = p(x, C_1) / p(x).
    ######################################################################################
    # In words: We can compute the posterior conditional distribution p(C_1 | X) by
    # dividing the joint distribution p(X, C_1) through the marginalized
    # distribution p(X).
    # In general:
    # $p(C_k | X) = p(X, C_k) / p(X)$
    ######################################################################################

    pC1_given_x = X[:, 1] / pX
    pC2_given_x = X[:, 2] / pX

    ######################################################################################
    # Normalization of the posterior conditional distribution p(C_k | X):
    # Note that also the posterior conditional distributions are properly normalized.
    # This can easily be seen by marginalizing the joint distribution p(X, C_k) in the 
    # following way:
    # $\sum_k p(X, C_k) = p(X) = \sum_k p(C_k | X) * p(X)$
    # We can rewrite this line as
    # $p(X) = p(X) \sum_k p(C_k | X)$, where we can cancel p(X) to obtain the desired 
    # normalization condition, i.e. that
    # $\sum_k p(C_k | X) = 1 $
    # Note that in figure 1.26 we plot p(C_k | X) as a function of X, i.e. as a function
    # of the conditioned variable X. However, p(C_k | X) is only a properly normalized
    # distribution as a function of C_k. In figure 1.26 this corresponds to vertically
    # summing the values p(C_k | X) for each given x, so that the sum of these two values
    # here must equal 1 for each x.
    ######################################################################################

    # save data
    data = np.zeros((nVisPoints, 3))
    data[:, 0] = X[:, 0]
    data[:, 1] = pC1_given_x
    data[:, 2] = pC2_given_x

    outname = 'prml_ch_01_figure_1.26_p_of_C_k_given_x_conditional_posterior_data.npy'
    np.save(os.path.join(RAWDIR, outname), data)
