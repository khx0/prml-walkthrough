#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-08
# file: bayesianPolyCurvFit.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import numpy as np

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)

def bayesianPolyCurveFit(xSupport, X, T, alpha, beta, M):
    '''
    Bayesian polynomial curve fitting.
    For variable naming conventions see Bishop chapter 1, page 31.
    '''
    
    assert len(X) == len(T), "Error: length assertion failed. Input training data mismatch."
    
    D = M + 1 # dimensionality
    nDatapoints = len(X)
    exponents = np.arange(0, D, 1)
    
    V = np.ones((D, nDatapoints)) 
    for n in range(nDatapoints): # fill V matrix column by column
        V[:, n] = np.power(X[n], exponents)
    
    # determine right hand side of linear system    
    rhs = np.matmul(V, T)
    
    # determine Sinv (inverse of the matrix S)
    Sinv = alpha * np.eye(D) + beta * np.matmul(V, V.T)
    
    # solve the linear system Sinv * xData = rhs
    # This linear system needs to be solved only once given all training data points
    # hence I call the solution vector xData, because it is based on the given training
    # data points as input.
    xData = np.linalg.solve(Sinv, rhs)
    
    # fill the predictive arrays
    mean = np.zeros((len(xSupport),))
    var = np.zeros((len(xSupport),))
    
    for i in range(len(mean)):    
        
        px = np.power(xSupport[i], exponents)
        
        xPrediction = np.linalg.solve(Sinv, px)
        
        mean[i] = (px.T).dot(xData)
        
        var[i] = (px.T).dot(xPrediction)
    
    res = np.zeros((len(mean), 3))
    res[:, 0] = xSupport
    res[:, 1] = beta * mean
    res[:, 2] = var + 1.0 / beta
    
    return res

if __name__ == '__main__':
    
    pass
