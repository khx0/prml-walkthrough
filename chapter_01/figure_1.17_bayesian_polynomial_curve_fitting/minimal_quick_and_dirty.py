#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-12
# file: minimal_quick_and_dirty.py
# tested with python 2.7.15 and matplotlib 2.2.3
# tested with python 3.7.2 and matplotlib 3.0.3
##########################################################################################

'''
Quick and dirty version of the bayesian polynomial curve fitting example
as illustrated in figure 1.17 of chapter 1 of Bishop's "Pattern Recognition and
Machine Learning" book. This script is not really meant for easy accessibility 
due to its brevity but rather as show case with no external dependencies. 
For a more pedagocical version refer to the bayesianPolyCurveFit.py module 
in the same directory.
'''

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

if __name__ == '__main__':
    
    # np.random.seed(523456789)
    
    N = 15 # number of training (sampling) data points
    X = np.linspace(0.0, 1.0, N)
    T = np.sin(2.0 * np.pi * X) + np.random.normal(0.0, 0.3, N)
    X_gt = np.linspace(-0.5, 1.5, 301)
    T_gt = np.sin(2.0 * np.pi * X_gt)
    
    # set parameters
    alpha = 5.0e-3
    beta = 11.1
    M = 9       # order of polynomial
    D = M + 1   # dimension
    
    # perform bayesian polynomial curve fitting
    V = np.ones((D, N)) 
    for n in range(N):
        V[:, n] = np.power(X[n], np.arange(0, D, 1))
    rhs = np.matmul(V, T)
    Sinv = alpha * np.eye(D) + beta * np.matmul(V, V.T)
    xData = np.linalg.solve(Sinv, rhs)
    mean, var = np.zeros((len(X_gt),)), np.zeros((len(X_gt),))
    for i in range(len(X_gt)):    
        px = np.power(X_gt[i], np.arange(0, D, 1))
        xPrediction = np.linalg.solve(Sinv, px)
        mean[i] = beta * (px.T).dot(xData)
        var[i] =  1.0 / beta + (px.T).dot(xPrediction)
	
    # plot result
    f, ax1 = plt.subplots(1)
    ax1.plot(X_gt, T_gt, color = '#00FF00', zorder = 2)
    ax1.scatter(X, T, facecolor = 'None', edgecolor = '#0000FF', zorder = 4)
    ax1.plot(X_gt, mean, color = '#FF0000', zorder = 3)
    ax1.fill_between(X_gt, mean - np.sqrt(var), mean + np.sqrt(var), 
                     color = '#FF0000', alpha = 0.20, lw = 0.0, zorder = 1)
    ax1.set_xlim(-0.05, 1.05)
    ax1.set_ylim(-1.65, 1.65)  
    ax1.set_xlabel(r'$x$')
    ax1.set_ylabel(r'$t$')        
    f.savefig('figure_1.17_minimal_quick_and_dirty.pdf', dpi = 300, transparent = True)
    
    plt.show()
