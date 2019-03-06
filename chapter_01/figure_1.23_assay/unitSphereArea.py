#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-06
# file: unit_sphere_area.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np
from scipy import special

def unitSphereArea(n):
    '''
    returns the area of a n dimensional unit sphere (r = 1)
    $A_n = 2 \pi^{n/2} / \Gamma(n / 2)$,
    where Gamma(n) = (n - 1)!
    '''
    return 2.0 * np.pi ** (n / 2.0) / special.gamma(n / 2.0)

def p_of_r_GaussianDistribution(r, sigma, D):
    '''
    radial pdf p(r) of the radial coordinate of a D dimensional normal distribution
    '''
    preF = unitSphereArea(D) * r ** (D - 1) / (2.0 * np.pi * sigma ** 2) ** (D / 2.0)
    return preF * np.exp(-r ** 2 / (2.0 * sigma ** 2))

if __name__ == '__main__':
    
    pass
