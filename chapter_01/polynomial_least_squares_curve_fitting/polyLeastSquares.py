#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-04-10
# file: polyLeastSquares.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np

def polyLeastSquares(m, X):
    '''
    polynomial least squares curve fitting
    m = degree of the fitting polynomial

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
    m = degree of the fitting polynomial

    X = array which contains the data points
    and is of shape (nDatapoints, 2)

    mu = is the regularization strength parameter.
    I would have liked to use lambda for the regularization strength. But since lambda
    is a python keyword I chose mu instead.
    This function implements quadratic regularization.

    returns the fitted weights vector, which is of shape
    (m + 1,)

    Usage:
    m = 9
    regLambda = 0.001
    w = polyLeastSquaresReg(m, Xt, regLambda) # Xt = training data
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
