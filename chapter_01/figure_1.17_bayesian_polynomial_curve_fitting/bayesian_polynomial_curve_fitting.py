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
    D = M + 1 # dimensionality
    
    # x query point
    x = np.linspace(0.0, 1.0, 11)
    
    ######################################################################################

    phiMat = np.ones((D, nDatapoints))    
    for n in range(nDatapoints):  # fill a column
        for i in range(D):
            phiMat[i, n] *= X[n] ** i
    
    # determine right hand side of linear system    
    rhs = np.matmul(phiMat, T)
    
    # determine Sinv
    tmp = np.zeros((D, D))
    for n in range(D):
        phi_xn = phiMat[:, n].reshape(D, 1)
        tmp += np.dot(phi_xn, phi_xn.T)
    
    Sinv = alpha * np.eye(D) + beta * tmp
    
    # solve linear system A * w = b for the weights vector w
    # here: Sinv * a = rhs
    a = np.linalg.solve(Sinv, rhs)
    
    # fill the predictive mean array mean
    mean = np.zeros((len(x),))
    
    for i in range(len(mean)):
        
        phi_of_x = np.ones((D, 1))
        for j in range(D):
            phi_of_x[j] *= x[i] ** j
        
        mean[i] = beta * phi_of_x.transpose().dot(a)
    
    res = np.zeros((len(mean), 2))
    res[:, 0] = x
    res[:, 1] = mean
    np.savetxt(os.path.join(RAWDIR, 'mean_prediction.txt'), res, fmt = '%.8f')
    
    print("mean = ", mean)
    
    