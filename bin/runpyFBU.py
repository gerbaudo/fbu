#!/bin/env python

import os
import sys
sys.path.append('fbu')
from PyFBU import PyFBU
from optparse import OptionParser

#__________________________________________________________
if __name__ == "__main__":

    pyfbu = PyFBU()
    pyfbu.nMCMC            = 100000
    pyfbu.nBurn            = 20000
    pyfbu.nThin            = 1
#    pyfbu.potential = 'Tikhonov'
    pyfbu.data             = [20,100,150,20]
    pyfbu.response         = [[0.01,0.06,0.02,0.01], #first truth bin
                              [0.01,0.02,0.06,0.01]] #second truth bin
    ndim = len(pyfbu.response)
    pyfbu.lower            = [0]*ndim
    pyfbu.upper            = [3000]*ndim
    pyfbu.background       = {'bckg': [5,10,40,5]}
    pyfbu.backgroundsyst   = {'bckg': 0.}
    pyfbu.objsyst = {'jes':[0.05,0.03,0.03,0.05]}
#    pyfbu.systfixsigma = -1.
    pyfbu.monitoring = True
    pyfbu.name = 'test'
    pyfbu.run()
