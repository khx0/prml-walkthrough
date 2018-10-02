#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-10-02
# file: polyLeastSquares.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################
import sys
import time
import datetime
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')
    
def polyLeastSquares(m, X):
    '''
    polynomial least squares curve fitting
    m = 3 degree of the fitting polynomial
    
    X = array which contains the data points
    and is of shape (nDatapoints, 2)
    
    returns the fitted weights vector, which is of shape
    (m + 1,)
    
    Usage:
    m = 9
    w = polyLeastSquares(m, Xt) # Xt = training data
    # returns the weight vector w
    '''
    nDatapoints = X.shape[0]
    assert X.shape[1] == 2, "Error: Shape assertion failed."
    
    # fill the Vandermonde matrix V
    V = np.ones((nDatapoints, m + 1))
    
    # column vector
    tmp = np.ones((nDatapoints,))
    
    for i in range(m):
        tmp = np.multiply(tmp, X[:, 0])
        V[:, i + 1] = tmp
    
    # fill the right hand side
    b = np.ones((nDatapoints, 1))
    b[:, 0] = X[:, 1]
    
    A = np.matmul(V.transpose(), V)
    b = np.matmul(V.transpose(), b)
        
    # solve linear system A * w = b for the weights vector w
    w = np.linalg.solve(A, b)
    w = w.reshape((m + 1,))
    
    return w
    
def polyLeastSquaresReg(m, X, mu):
    '''
    polynomial least squares curve fitting
    m = 3 degree of the fitting polynomial
    
    X = array which contains the data points
    and is of shape (nDatapoints, 2)
    
    mu = is the regularization strength parameter.
    This function implements quadratic regularization.
    
    returns the fitted weights vector, which is of shape
    (m + 1,)
    
    Usage:
    m = 9
    w = polyLeastSquares(m, Xt) # Xt = training data
    # returns the weight vector w
    '''
    nDatapoints = X.shape[0]
    assert X.shape[1] == 2, "Error: Shape assertion failed."
    
    # fill the Vandermonde matrix V
    V = np.ones((nDatapoints, m + 1))
    
    # column vector
    tmp = np.ones((nDatapoints,))
    
    for i in range(m):
        tmp = np.multiply(tmp, X[:, 0])
        V[:, i + 1] = tmp
    
    # fill the right hand side
    b = np.ones((nDatapoints, 1))
    b[:, 0] = X[:, 1]
    
    A = np.matmul(V.transpose(), V)
    b = np.matmul(V.transpose(), b)
    
    # add mu * Id to account for quadratic regularization
    A += mu * np.eye(m + 1)
        
    # solve linear system A * w = b for the weights vector w
    w = np.linalg.solve(A, b)
    w = w.reshape((m + 1,))
    
    return w

if __name__ == '__main__':

    pass
