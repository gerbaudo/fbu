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
    pyfbu.data             = [20,100,150,20]
    pyfbu.response         = [[0.06,0.02,0.01,0.01], #first truth bin
                              [0.02,0.06,0.02,0.01],
                              [0.01,0.04,0.03,0.02], #first truth bin
                              [0.01,0.03,0.04,0.02], #second truth bin
                              [0.01,0.02,0.06,0.02], #first truth bin
                              [0.01,0.01,0.02,0.06]] #second truth bin
    ndim = len(pyfbu.response)
    pyfbu.lower            = [0]*ndim
    pyfbu.upper            = [3000]*ndim

    from potentials import Regularization
    pyfbu.regularization = Regularization('Tikhonov',ntotbins=6,ndiffbins=2)

    pyfbu.background       = {'bckg1': [5,5,20,5],'bckg2': [0,5,20,0]}
    pyfbu.backgroundsyst   = {'bckg1': 0.,'bckg2': 0.}
    pyfbu.objsyst = { 
        'signal':{'jes':[0.05,0.05,0.05,0.05],
                  'jer':[0.03,0.03,0.03,0.03]
                  },
        'background':{
            'jes':{
                'bckg1':[0.05,0.05,0.05,0.05],
                'bckg2':[0.01,0.01,0.01,0.01]
                },
            'jer':{
                'bckg1':[0.01,0.01,0.01,0.01],
                'bckg2':[0.05,0.05,0.05,0.05]
                }
            }
        }
    pyfbu.systfixsigma = -1.
    pyfbu.monitoring = True
    pyfbu.name = 'test'
    pyfbu.run()
