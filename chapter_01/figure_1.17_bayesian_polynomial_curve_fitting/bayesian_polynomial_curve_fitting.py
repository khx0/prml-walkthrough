#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-07
# file: bayesian_polynomial_curve_fitting.py
# tested with python 2.7.15
# tested with python 3.7.0
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

def predictive_mean(xSupport, X, T, alpha, beta, M):
    '''
    still needs to be heavily vectorized
    '''
    assert len(X) == len(T), "Error: length assertion failed."
    D = M + 1 # dimensionality
    nDatapoints = len(X)
    
    V = np.ones((D, nDatapoints))    
    for n in range(nDatapoints):  # fill a column
        for i in range(D):        
            V[i, n] *= X[n] ** i
    
    # determine right hand side of linear system    
    rhs = np.matmul(V, T)
    
    # determine Sinv (inverse of the matrix S)
    Sinv = np.zeros((D, D))
    for n in range(D):
        pxn = V[:, n].reshape(D, 1)
        Sinv += np.dot(pxn, pxn.T)
    Sinv *= beta
    Sinv += alpha * np.eye(D)
    
    # solve the linear system Sinv * solvec = rhs
    solvec = np.linalg.solve(Sinv, rhs)
    
    # fill the predictive mean array mean
    mean = np.zeros((len(xSupport),))
    
    for i in range(len(mean)):    
        px = np.ones((D, 1))
        for j in range(D):
            px[j] *= xSupport[i] ** j
        
        mean[i] = beta * px.transpose().dot(solvec)
    
    res = np.zeros((len(mean), 2))
    res[:, 0] = xSupport
    res[:, 1] = mean

    return res

if __name__ == '__main__':
    
    # PRML - Bishop - Chapter 1 Introduction - Bayesian Polynomial Curve Fitting
    
    ######################################################################################
    # file i/o
    
    seedValue = 523456789
    filename = 'prml_ch_01_figure_1.2_training_Data_PRNG-seed_{}.txt'.format(seedValue)
    
    data = np.genfromtxt(os.path.join(RAWDIR, filename))
    assert data.shape[1] == 2, "Error: Shape assertion failed."
    print("data.shape =", data.shape)
    nDatapoints = data.shape[0]
    
    X, T = data[:, 0], data[:, 1] # using the Bishop naming convention
    
    ######################################################################################
    # set parameters for this problem
    alpha = 5.0e-3
    beta = 11.1
    M = 9 # order of polynomial
    xSupport = np.linspace(0.0, 1.0, 201)
    ######################################################################################

    res = predictive_mean(xSupport, X, T, alpha, beta, M)

    np.savetxt(os.path.join(RAWDIR, 'mean_prediction.txt'), res, fmt = '%.8f')
    