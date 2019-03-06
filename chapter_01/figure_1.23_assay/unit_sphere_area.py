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

import os
import datetime
import math
import numpy as np
from scipy import special

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')
  
def unitSphereArea(n):
    
    num = 2.0 * np.pi ** (n / 2.0)
#     if (n == 1):
#         return num / np.sqrt(np.pi)
#     else:
    den = special.gamma(n / 2.0)
    return num / den
    
if __name__ == '__main__':
    
    print(unitSphereArea(1))
    print(unitSphereArea(2))
    print(unitSphereArea(3))
    
    # A_n = 2 pi^n/2 / Gamma(n/2)
    # Gamma(n) = (n - 1)!
    
    
    '''
    yVals = np.array([2.0 / np.sqrt(2.0 * np.pi * sigma ** 2) * np.exp(-r ** 2 / (2.0 * sigma ** 2)) for r in xVals])
    
    yVals = np.array([r * np.exp(-r ** 2 / (2.0 * sigma ** 2)) / (sigma ** 2) for r in xVals])

    preFactor = 2.0 * np.pi ** (Dval / 2.0) / math.factorial(Dval / 2 - 1) \
             / (2.0 * np.pi * sigma ** 2) ** (Dval / 2)
    yVals = np.array([preFactor * r ** (Dval - 1) * np.exp(-r ** 2 / (2.0 * sigma ** 2)) for r in xVals])
    '''
    
