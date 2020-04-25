#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-25
# file: test_entropy.py
# tested with python 3.7.6  and pytest 5.5.2
##########################################################################################

import time
import numpy as np

from entropy import entropy

'''
Tested with pytest version 5.3.5.
Unit test invocation:
Run this test script by calling
$python -m pytest (-v)
from the directory which contains this script. Here python is your desired
python interpreter. To show print statements add the -s flag to the actual
pytest command, i.e. execute
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

if __name__ == '__main__':

    test_01()

    # make this below a unit test
    #     x = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
# 
#     # x = np.array([0.5, 0.5])
# 
#     print(np.sum(x))
#     
#     H = entropy(x)
#     
#     print("H =", H)
#     print(np.log(5))
