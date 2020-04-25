#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-25
# file: test_entropy.py
# tested with python 3.7.6  and pytest 5.4.1
##########################################################################################

import time
import numpy as np

from entropy import entropy

'''
Tested with pytest version 5.4.1.
Unit test invocation:
Run this test script by calling
$python -m pytest (-v)
from the directory which contains this script. Here python is your desired
python interpreter. To show print statements add the -s flag to the actual
pytest command, i.e. execute
$python -m pytest -s
'''

def test_01():
    
    x = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    
    norm = np.sum(x)
    
    assert np.isclose(norm, 1.0)
    
    eVal = entropy(x)
    
    assert np.isclose(eVal, np.log(len(x)))
    
    return None

def test_02():

    x = np.array([0.5, 0.5])
    
    norm = np.sum(x)
    
    assert np.isclose(norm, 1.0)
    
    eVal = entropy(x)
    
    assert np.isclose(eVal, np.log(len(x)))

    return None

if __name__ == '__main__':

    test_01()

    test_02()
