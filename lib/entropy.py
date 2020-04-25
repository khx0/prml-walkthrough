#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-25
# file: entropy.py
# tested with python 3.7.6
##########################################################################################

import numpy as np

def entropy(x):
    '''
    Computes the discrete entropy of the given
    probabilities x.
    '''
    H = 0.0
    for pi in x:
        if np.isclose(pi, 0.0):
            continue
        else:
            H += -pi * np.log(pi)
    return H

if __name__ == '__main__':

    pass

    ######################################################################################
    # TODO:
    # Ideally I would like to compute the sample entropy in a vectorized from, by using
    # something along the lines like this:
    # return -x.dot(np.log(x))
    ######################################################################################
