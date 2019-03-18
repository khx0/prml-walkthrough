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

import time
import numpy as np

from polynomials import polynomial_horner

'''
Unit test invocation:
Run this test script by calling in this scripts containing directory.
$python -m pytest
where python is your desired python interpreter.
'''

def test_01():
    
    coeff = np.array([1.0])
    # ==> f(x) = 1.0
    
    res = polynomial_horner(0.0, *coeff)
    assert np.isclose(res, 1.0)
    
    res = polynomial_horner(0.1, *coeff)
    assert np.isclose(res, 1.0)
    
    res = polynomial_horner(-99.1, *coeff)
    assert np.isclose(res, 1.0)
    
    res = polynomial_horner(1.0e-3, *coeff)
    assert np.isclose(res, 1.0)

def test_02():

    coeff = np.array([1.0])
    # ==> f(x) = 1.0
    
    xVals =  np.array([0.0])
    res = polynomial_horner(xVals, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    xVals =  np.array([0.25])
    res = polynomial_horner(xVals, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    xVals =  np.array([0.6666667])
    res = polynomial_horner(xVals, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    xVals =  np.array([1.6666667e-9])
    res = polynomial_horner(xVals, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    xVals =  np.array([1.0])
    res = polynomial_horner(xVals, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
def test_03():

    coeff = np.array([1.0])
    # ==> f(x) = 1.0
    
    res = polynomial_horner(0.0, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    res = polynomial_horner(0.25, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    res = polynomial_horner(0.6666667, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    res = polynomial_horner(1.6666667e-9, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)
    
    res = polynomial_horner(1.0, *coeff)
    reference = 1.0
    assert np.isclose(res, reference)

def test_04():
    
    coeff = np.array([1.0, 1.0])
    # ==> f(x) = 1 + x
    xVals =  np.array([1.0, 0.0])
    reference = np.array([2.0, 1.0])
    res = polynomial_horner(xVals, *coeff)
    
    assert np.array_equal(res, reference)
    
if __name__ == '__main__':
    
    pass
    
    ######################################################################################
    # ToDo Clean up below:    
    
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