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

def polynomial_horner(x, *coeff):
    '''
    Polynomial function using Horner's scheme.
    '''
    res = coeff[-1]
    for i in range(-2, -len(coeff) - 1, -1):
        res = res * x + coeff[i]
    return res

if __name__ == '__main__':

    pass
