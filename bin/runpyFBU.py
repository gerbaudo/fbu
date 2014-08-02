#!/bin/env python

import sys
sys.path.append('fbu')
from PyFBU import PyFBU

#__________________________________________________________
if __name__ == "__main__":

    pyfbu = PyFBU()
    pyfbu.data             = [100,150]
    pyfbu.response         = [[0.08,0.02], #first truth bin
                              [0.02,0.08]]
    ndim = len(pyfbu.response)
    pyfbu.lower            = [500,500]
    pyfbu.upper            = [3000,3000]

    pyfbu.monitoring = True
    pyfbu.name = 'test'

    pyfbu.background       = {'bckg1': [5,20],'bckg2': [5,30]}
    pyfbu.backgroundsyst   = {'bckg1': 0.5,'bckg2': 0.4}

    pyfbu.objsyst = { 
        'signal':{
            's1':[0.05,0.05],
            's2':[0.03,0.03],
            's3':[0.03,0.03],
            's4':[0.03,0.03],
            's5':[0.03,0.03],
            's6':[0.03,0.03],
            's7':[0.03,0.03],
            's8':[0.03,0.03],
            },
        'background':{
            's1':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's2':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's3':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's4':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's5':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's6':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's7':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                },
            's8':{ 
                'bckg1': [0.05,0.05],
                'bckg2': [0.05,0.05]
                }
            }
        }

    pyfbu.run()

    from numpy import mean, std
    for bin in pyfbu.trace:
        print mean(bin),std(bin)
