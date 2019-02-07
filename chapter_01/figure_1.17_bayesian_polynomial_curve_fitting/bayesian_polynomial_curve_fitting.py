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

if __name__ == '__main__':
    
    # PRML - Bishop - Chapter 1 Introduction - Bayesian Polynomial Curve Fitting
    
    ######################################################################################
    # file i/o
    
    seedValue = 523456789
    filename = 'prml_ch_01_figure_1.2_training_Data_PRNG-seed_{}.txt'.format(seedValue)
    
    X = np.genfromtxt(os.path.join(RAWDIR, filename))
    assert X.shape[1] == 2, "Error: Shape assertion failed."
    print("X.shape =", X.shape)
    nDatapoints = X.shape[0]
    
    ######################################################################################
    # set parameters for this problem
    alpha = 5.0e-3
    beta = 11.1
    M = 9 # order of polynomial
    D = M + 1 # dimensionality
    
    # x query point
    x = np.array([0.5])
    
    ########## FIX ME #############
    # construct ... *** ...
    
    phiMat = np.ones((D, nDatapoints))
    for n in range(nDatapoints):    
        for i in range(1, D, 1):
            phiMat[i, n] *= X[n, 0] ** i
    
    a = np.matmul(phiMat, X[:, 1])
    
    tmp = np.zeros((D, D))
    for n in range(D):
        tmp += np.matmul(phiMat[n, :], phiMat[n, :])
    
    Sinv = alpha * np.eye(D) + beta * tmp
    
    # solve linear system A * w = b for the weights vector w
    b = np.linalg.solve(Sinv, a)
    print(b.shape)
    
    # fill the predictive mean array mean
    mean = np.array((len(x),))
    for i in range(len(mean)):
        
        phi_of_x = np.ones((D,))
        for j in range(1, D, 1):
            phi_of_x[j] *= x[i] ** j
        
        mean[i] = beta * phi_of_x.transpose().dot(b)
    
    print("mean = ", mean)
    print("mean.shape =", mean.shape)
    
    