#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-06
# file: test_unitSphereArea.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import platform
import numpy as np
import unittest

from unitSphereArea import unitSphereArea

class TestUnitSphereArea(unittest.TestCase):
    '''
    Test cases for the unitSphereArea module
    '''
    
    def test_01(self):
        
        A1 = 2.0
        A2 = 2.0 * np.pi
        A3 = 4.0 * np.pi
        
        self.assertTrue(np.isclose(A1, unitSphereArea(1)))
        self.assertTrue(np.isclose(A2, unitSphereArea(2)))
        self.assertTrue(np.isclose(A3, unitSphereArea(3)))
           
        return None

if __name__ == '__main__':
    
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running ", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    
    unittest.main()
