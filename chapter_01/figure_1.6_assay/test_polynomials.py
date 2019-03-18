#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-18
# file: test_polynomials.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import sys
import os
import datetime
import numpy as np

from polynomials import polynomial_horner

'''
Test invocation:
$python3 -m pytest
'''

def test_01():
    
    coeff = np.array([1.0])
    x = np.array([0.0])
    
    print(polynomial_horner(x, *coeff))

if __name__ == '__main__':

    test_01()
    
    # test the two different function calls as below
    
    # test vectorized function calls
    
    
    '''
    ######################################################################################
    # global parameters
    nTrain = 15
    
    mu = 0.0
    sigma = 0.3
    
    ######################################################################################
    # create training data
    Xt = np.zeros((nTrain, 2))
    xVals = np.linspace(0.0, 1.0, nTrain)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals
    
    ######################################################################################
    # polynomial curve fitting (learning the model)
    m = 9
    w = np.ones((m + 1,))
    popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)
    
    
    # create fitted model
    nModelPoints = 800
    Xm = np.zeros((nModelPoints, 2))
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = np.zeros_like(xVals)
    
    
    yVals = np.array([polynomial_horner(x, *popt) for x in xVals])
    '''