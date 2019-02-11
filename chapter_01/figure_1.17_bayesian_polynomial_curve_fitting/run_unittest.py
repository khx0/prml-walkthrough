#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-11
# file: run_unittest.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import numpy as np

from bayesianPolyCurveFit import bayesianPolyCurveFit

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)

if __name__ == '__main__':
    
    X = np.array([0.0, 1.0])
    T = np.array([0.0, 1.0])
    nDatapoints = len(X)
    print("using nDatapoints =", nDatapoints)
    
    # set (hyper-) parameters for this problem
    alpha = 1.0
    beta = 1.0
    M = 1 # order of polynomial

    xSupport = np.array([0.5])
    
    res = bayesianPolyCurveFit(xSupport, X, T, alpha, beta, M)
    
    # for this test case res should equal
    # res = ([[0.5, 0.4, 1.35]])
    print("res =", res)
