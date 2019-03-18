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

# def polynomial_horner(x, *coeff):
#     '''
#     Polynomial function using Horner's scheme.
#     '''
#     res = coeff[-1]
#     for i in range(-2, -len(coeff) - 1, -1):
#         res = res * x + coeff[i]
#     return res

def polynomial_horner(x, *coeff):
    '''
    Polynomial function using Horner's scheme.
    coeff is a tuple which contains the coefficients and returns
    f(x) = coeff[0] * x + coeff[1] * x^2 + ... +  coeff[m] * x^m
    where coeff contains the (m + 1) coefficients for a polynomial of degree m.
    
    The functions preserves the input shape, such that
    output.shape == x.shape.
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
