#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-04-08
# file: test_polynomials.py
# tested with python 2.7.15 and pytest 4.3.1
# tested with python 3.7.2  and pytest 4.3.1
##########################################################################################

import time
import numpy as np

from polynomials import polynomial_horner

'''
Unit test invocation:
Run this test script by calling in this scripts containing directory.
$python -m pytest
where python is your desired python interpreter.
To show print statements add the -s flag to the actual pytest command.
$python -m pytest -s
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

def test_05():

    nVals = 120
    xVals = np.linspace(0.0, 1.0, nVals)
    coeff = np.array([0.0, 1.0])
    yVals = polynomial_horner(xVals, *coeff)
    assert xVals.shape == yVals.shape
    assert np.array_equal(xVals, yVals)

def test_06():

    nVals = 130
    xVals = np.linspace(0.0, 1.0, nVals)
    coeff = np.array([1.0])
    yVals = polynomial_horner(xVals, *coeff)
    assert xVals.shape == yVals.shape
    assert np.array_equal(np.ones(nVals), yVals)

def test_07():

    nVals = 140
    xVals = np.linspace(0.0, 1.0, nVals)
    coeff = np.array([1.0, 0.0, 0.5])
    yVals = polynomial_horner(xVals, *coeff)
    assert xVals.shape == yVals.shape
    yVals_ref = np.array([1.0 + 0.5 * x ** 2 for x in xVals])
    assert np.array_equal(yVals, yVals_ref)

def test_08():
    # single value test
    xVals = np.array([0.91264712])
    coeff = np.array([0.15, 2.83, 3.5, -0.224, 2.9971])
    yVals = polynomial_horner(xVals, *coeff)
    assert xVals.shape == yVals.shape
    yVals_ref = np.array([0.15 + 2.83 * x + 3.5 * x ** 2 - 0.224 * x ** 3 \
        + 2.9971 * x ** 4 for x in xVals])
    assert np.array_equal(yVals, yVals_ref)

def test_09():
    # return type test
    coeff = np.array([1.0, 1.0]) # i.e. f(x) = 1 + x

    # vector in / vector out
    xVals = np.array([0.15])
    yVals = polynomial_horner(xVals, *coeff)
    assert xVals.shape == yVals.shape
    assert type(xVals) == type(yVals)
    yVals_ref = np.array([1.0 + x for x in xVals])
    assert np.array_equal(yVals, yVals_ref)

    # scalar in / scalar out
    xVals = 0.15
    yVals = float(polynomial_horner(xVals, *coeff))
    assert type(xVals) == type(yVals)
    yVals_ref = 1.0 + 1.0 * 0.15
    assert np.array_equal(yVals, yVals_ref)

def test_10():

    # return type test
    coeff = np.array([0.0]) # i.e. f(x) = 1.0

    yValue_ref = 1.0
    yValue = polynomial_horner(0.0, *coeff)

    assert np.isclose(yValue, yValue_ref)

if __name__ == '__main__':

    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()
    test_08()
    test_09()
    test_10()
