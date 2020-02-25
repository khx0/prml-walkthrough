#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-02-25
# file: legacy.py
# tested with python 2.7.15
# tested with python 3.7.6
##########################################################################################

def ensure_dir(dir):
    '''
    The ensure_dir function can be replaced by
    os.makedirs(<DIRNAME>, exist_ok = True) in python 3.x.
    For Python 2.7.x however I frequently used this version.
    '''
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':

    pass
