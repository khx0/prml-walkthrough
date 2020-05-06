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
    # create data for figure 1.27
    ##############################################

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

    # For p(x| C_2) I found a parametrization using a normal distribution, which is
    # a properly normalized class conditional prior density p(x | C_k) as it should be.
#     yVals = 0.86 * norm.pdf(xVals, loc = loc3, scale = np.sqrt(0.0075))
#     X[:, 2] = yVals
    yVals = norm.pdf(xVals, loc = loc3, scale = np.sqrt(0.01))
    X[:, 2] = yVals

    # compute normalization of p(x | C_1) and p(x| C_2)
    norm_01 = np.trapz(X[:, 1], X[:, 0])
    norm_02 = np.trapz(X[:, 2], X[:, 0])
    norm = norm_01 + norm_02
    assert np.isclose(norm_02, 1.0), "Error: Normaliztion condition not satisfied."

    # save data
    outname = 'prml_ch_01_figure_1.27_p_of_x_given_C_k_conditional_prior_data.npy'
    np.save(os.path.join(RAWDIR, outname), X)

    ######################################################################################
    # Comment 2
    # Normally, prior conditional probability distributions such as the here considered
    # p(x | C_k)'s are properly normalized probability distributions.
    # This can be easily seen from the following argument:
    # p(C_k) = \int p(x,C_k) dx = \int p(x | C_k) p(C_k) dx = p(C_k) * \int p(x | C_k) dx
    # Here the first equality is the standard marginalization, and then we simply used 
    # the product rule of probability. From this line above we can cross out the p(C_k) 
    # and arrive at
    # \int p(x | C_k) dx = 1, which is the normalization condition for p(x | C_k).
    ######################################################################################
    # However, I only managed to find a parametrization for p(x | C_2) which looks like
    # shown in the book and which is at the same time normalized.
    # I also tried to mimick p(x | C_1) by a sum of two scaled normal distributions, 
    # but did not find parameters such that the resulting distribution looks like the one 
    # shown in figure 1.27 (left) and which is at the same time a normalized distribution.
    # Hence, I used parameters to obtain a distribution, which looks roughly like the one
    # shown in the book but which is not (yet) normalized. 
    # For visualization I simply plot this in figure 1.27 (left) and hence save the
    # non-normalized version of p(x | C_1) above. 
    # For the further derivations, below I will first normalize these distributions, which
    # forms the starting point for the calculation of the conditional posterior
    # distributions, as shown in figure 1.27 (right).
    ######################################################################################

    X[:, 1] /= norm_01
    # X[:, 2] /= norm_02 # p(x| C_2) is already normalized 
                         # (only un-comment if X[:, 2] is not normalized)

    ######################################################################################
    # Compute p(C_k) and p(x):
    # If we had started with the joint distribution, we could have determined p(C_k)
    # directly by marginalization, as done in the assay of figure 1.26.
    # Having only information about the class conditional prior distributions p(x | C_k)'s
    # we additionally must make an assumption about the class prior's themselves.
    # Here we will make the ad hoc decision to set them equal, i.e. use
    # p(C_1) = p(C_2) = 0.5.

    pC1 = pC2 = 0.5
    assert np.isclose((pC1 + pC2), 1.0), \
        "Error: Normalization assertion failed."

    #################################################################
    # TODO: also still consider this variant below as an alternative.
    # pC1 = norm_01 / norm
    # pC2 = norm_02 / norm
#     print(norm_01)
#     print(norm_02)
#     print(norm)
    #################################################################

    # Next, we also find the probability distribution p(x). Once again, if we had the
    # full joint p(x, C_k) we could directly compute p(x) by marginalization.
    # But with the knowledge of the p(C_k) it is also not really more complicated.
    # We use:
    # $p(X) = \sum_k p(X, C_k) = \sum_k p(X | C_k) * p(C_k)$
    # This is simply what we do below:

    pX = pC1 * X[:, 1] + pC2 * X[:, 2]
    assert np.isclose(np.trapz(pX, X[:, 0]), 1.0), \
        "Error: Normalization assertion failed."

    ######################################################################################
    # Compute posterior conditional probability distributions p(C_k | x):
    # Here we simply use Bayes theorem once more:
    # p(C_k | x) = p(x | C_k) * p(C_k) / p(x) where k = {1, 2}
    ######################################################################################

    pC1_given_x = X[:, 1] * pC1 / pX
    pC2_given_x = X[:, 2] * pC2 / pX

    ######################################################################################
    # Normalization of the posterior conditional distribution p(C_k | x):
    # Note that also the posterior conditional distributions are properly normalized.
    # This can easily be seen by marginalizing the joint distribution p(X, C_k) in the 
    # following way:
    # $\sum_k p(x, C_k) = p(x) = \sum_k p(C_k | x) * p(x)$
    # We can rewrite this line as
    # $p(x) = p(x) \sum_k p(C_k | x)$, where we can cancel p(x) to obtain the desired 
    # normalization condition, i.e. that
    # $\sum_k p(C_k | x) = 1 $
    # Note that in figure 1.27 (right) we plot p(C_k | x) as a function of x, 
    # i.e. as a function of the conditioned variable x. However, p(C_k | x) is only a 
    # properly normalized distribution as a function of C_k. 
    # In figure 1.26 this corresponds to vertically summing the values p(C_k | x) for each
    # given x, so that the sum of these two values here must equal 1 for each value x. 
    # We explicitly test this below.
    ######################################################################################

    for i in range(len(X[:, 0])):
        assert np.isclose(pC1_given_x[i] + pC2_given_x[i], 1.0), \
            'Error: Normalization of p(C_k | x) violated.'

    # save data
    data = np.zeros((nVisPoints, 3))
    data[:, 0] = X[:, 0]
    data[:, 1] = pC1_given_x
    data[:, 2] = pC2_given_x

    outname = 'prml_ch_01_figure_1.27_p_of_C_k_given_x_data.npy'
    np.save(os.path.join(RAWDIR, outname), data)
