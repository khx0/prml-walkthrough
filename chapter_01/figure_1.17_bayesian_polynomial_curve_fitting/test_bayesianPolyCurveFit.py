#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-12-06
# file: test_BayesianPolyCurveFit.py
# tested with python 3.7.6
##########################################################################################

'''
Also tested with pytest (version 6.1.2)
cd to the directory containing this script and
then invoke pytest as
$python -m pytest
where python is your chosen python interpreter or
alternatively simply call
$pytest
using the default python interpreter.
'''

import os
import platform
import datetime
import numpy as np
import unittest

# use PREDICTOR as an wrapper alias function
from BayesianPolyCurveFit import BayesianPolyCurveFit as PREDICTOR

class BayesianPolyCurveFitTest(unittest.TestCase):
    '''
    Unit test for the provided python implementation of the Bayesian
    polynomial curve fitting algorithm.
    The notation follows the notation from Bishop's book (Chapter 1) 
    to a certain extend.
    '''

    def test_case_01(self):

        X = np.array([0.0, 1.0])
        T = np.array([0.0, 1.0])
        n_datapoints = len(X)
        print("using n_datapoints =", n_datapoints)

        # set parameters for this problem
        alpha = 1.0
        beta = 1.0
        M = 1 # order of polynomial

        xSupport = np.array([0.5])

        mean_analytical = 2.0 / 5.0
        variance_analytical = 27.0 / 20.0

        res = PREDICTOR(xSupport, X, T, alpha, beta, M)

        # for this test case res should equal
        # res = ([[0.5, 0.4, 1.35]])
        self.assertTrue(res.shape == (1, 3))
        self.assertTrue(np.isclose(res[0, 0], xSupport[0]))
        self.assertTrue(np.isclose(res[0, 1], mean_analytical))
        self.assertTrue(np.isclose(res[0, 2], variance_analytical))

        print("res =", res)

    def test_case_02(self):

        X = np.array([0.0, 1.0])
        T = np.array([0.0, 1.0])
        n_datapoints = len(X)
        print("using n_datapoints =", n_datapoints)

        # set parameters for this problem
        alpha = 1.0
        beta = 1.0
        M = 1 # order of polynomial

        xSupport = np.array([0.0])

        mean_analytical = 1.0 / 5.0
        variance_analytical = 7.0 / 5.0

        res = PREDICTOR(xSupport, X, T, alpha, beta, M)

        # for this test case res should equal
        # res = ([[0.0, 0.2, 1.4]])
        self.assertTrue(res.shape == (1, 3))
        self.assertTrue(np.isclose(res[0, 0], xSupport[0]))
        self.assertTrue(np.isclose(res[0, 1], mean_analytical))
        self.assertTrue(np.isclose(res[0, 2], variance_analytical))

        print("res =", res)

    def test_case_03(self):

        X = np.array([0.0, 1.0])
        T = np.array([0.0, 1.0])
        n_datapoints = len(X)
        print("using n_datapoints =", n_datapoints)

        # set parameters for this problem
        alpha = 1.0
        beta = 1.0
        M = 1 # order of polynomial

        xSupport = np.array([1.0])

        mean_analytical = 3.0 / 5.0
        variance_analytical = 8.0 / 5.0

        res = PREDICTOR(xSupport, X, T, alpha, beta, M)

        # for this test case res should equal
        # res = ([[0.0, 0.6, 1.6]])
        self.assertTrue(res.shape == (1, 3))
        self.assertTrue(np.isclose(res[0, 0], xSupport[0]))
        self.assertTrue(np.isclose(res[0, 1], mean_analytical))
        self.assertTrue(np.isclose(res[0, 2], variance_analytical))

        print("res =", res)

if __name__ == '__main__':

    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running ", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")

    unittest.main()
