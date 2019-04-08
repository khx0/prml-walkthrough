#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-18
# file: polynomials.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np

def polynomial_horner(x, *coeff):
    '''
    Implements a standard polynomial in one variable using Horner's scheme.
    coeff is a tuple which contains the polynomials coefficients and returns
    f(x) = coeff[0] * x + coeff[1] * x^2 + ... +  coeff[m] * x^m
    where coeff contains the (m + 1) coefficients for a polynomial of degree m.
    
    The functions preserves the input shape, such that
    res.shape == x.shape.
    If x is a pure scalar float, res will equally be a single scalar float.
    
    For ultimate performance you might want to
    overload this function having an explicit function for pure floats
    and for vectorized inputs to avoid the try/except block of this implementation.
    
    The function signature is compatible with scipy's curve_fit module, in the sense
    that polynomial_horner is a callable function which satisfies the notion
    ydata = f(xdata, *params)
    '''
    try:
        res = np.ones(x.shape) * coeff[-1]
    except AttributeError:
        res = coeff[-1]
    for i in range(-2, -len(coeff) - 1, -1):
        res = res * x + coeff[i]
    return res

if __name__ == '__main__':

    pass
