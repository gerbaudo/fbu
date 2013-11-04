#! /bin/env python

import sys, os
import numpy as np
from fbu.PyFBU import PyFBU
from tests.linearity import computeAc
from utils import plot

#__________________________________________________________
if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))+'/'
    lin_dir = 'tests/linearity/'
    pyfbu = PyFBU()

    pyfbu.nMCMC    = 100000
    pyfbu.setnBurn = 1000
    pyfbu.setnThin = 10

    data = 'dataA2pos.json'
    migr = 'migrations.json'
    back = 'background.json'

    json_dir = lin_dir+'data/mc12/'
    pyfbu.lower, pyfbu.upper = 400000, 900000
    import json
    pyfbu.response  = json.load(open(json_dir+migr))
    pyfbu.background  = json.load(open(json_dir+back))
    pyfbu.data = json.load(open(json_dir+data))
    pyfbu.run()
    acListmc12  = computeAc.computeAcList(pyfbu.trace)
    acArraymc12 = np.array(acListmc12)

    json_dir = lin_dir+'data/mc11/'
    pyfbu.response  = json.load(open(json_dir+migr))
    pyfbu.background  = json.load(open(json_dir+back))
    pyfbu.data = json.load(open(json_dir+data))
    pyfbu.lower, pyfbu.upper = 70000, 140000
    pyfbu.run()
    acListmc11  = computeAc.computeAcList(pyfbu.trace)
    acArraymc11 = np.array(acListmc11)

    print 'RMS mc11 = %f   mc12=%f'%(np.std(acArraymc11),np.std(acArraymc12))
    acMc11Mc12 = [acArraymc11,acArraymc12]
    plot.plotarraymulti(acMc11Mc12, out_dir+'Ac_posterior_mc11-12_'+data.replace('.json',''))
