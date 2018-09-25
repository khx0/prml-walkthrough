#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-25
# file: ch_01_curve_fitting_figure_1.5_batch.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import sys
import time
import datetime
import os
import math
import numpy as np

from scipy.optimize import curve_fit

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)

# normally
# def poly_horner(x, coeff):
#     result = coeff[-1]
#     for i in range(-2, -len(coeff)-1, -1):
#         result = result*x + coeff[i]
#     return result

def poly_horner(x, *coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result*x + coeff[i]
    return result

def poly_horner2(x, coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result*x + coeff[i]
    return result
    
def func(x, p):
    return p[0] + p[1] * x    

def auxFunc(*args):
    return func(args[0], args[1:])

if __name__ == '__main__':
    
    # load training data (figure 1.2 curve fitting demo)
    
    filename = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_523456789.txt'
    Xt = np.genfromtxt(os.path.join(RAWDIR, filename))
    
    assert Xt.shape == (10, 2), "Error: Shape assertion failed."
    
    N = Xt.shape[0]
    print("Training data shape =", Xt.shape)
    print("no. of training data points N = ", N)
    
    ######################################################################################
    
    # polynomial curve fitting
    
    mOrder = np.arange(0, 10, 1).astype('int')
    # mOrder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    fitparameter_file = 'prml_ch_01_curve_fitting_parameter_results.txt'
    
    f = open(os.path.join(RAWDIR, fitparameter_file), 'wr')
    
    line = '\t M = 0 \t M = 1 \t M = 3 \t M = 9 \n'
    f.write(line)
    
    res = np.zeros((len(mOrder), 2))
    
    for m in mOrder:
        
        print "m = ", m
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        print(w)
        print(w.shape)
        
        # curve fitting
        popt, pcov = curve_fit(poly_horner, Xt[:, 0], Xt[:, 1], p0 = w)
                
        yPredict = np.array([poly_horner2(x, popt) for x in Xt[:, 0]])
        
        # compute sum of squares deviation
                
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))
        
        RMS = np.sqrt(2.0 * sum_of_squares_error / N)
        
        res[m, 0] = m
        res[m, 1] = RMS
    
    ######################################################################################
    # file i/o

    f.close()
    
    outname = 'prml_ch_01_figure_1.5_training_error.txt'
    
    np.savetxt(os.path.join(RAWDIR, outname),res, fmt = '%.8f')
    
    
    
