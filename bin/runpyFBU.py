#!/bin/env python

import os
import sys
sys.path.append('fbu')
from PyFBU import PyFBU
from optparse import OptionParser

#__________________________________________________________
if __name__ == "__main__":
    projectdir = os.path.dirname(os.path.abspath(__file__)).replace('/bin','/')
    datadir = projectdir+'tests/linearity/data/mc11/'
    defaultdata = datadir+'dataA2pos.json'
    defaultmig  = datadir+'migrations.json'
    defaultbkg  = datadir+'background.json'
    usage = "usage: %prog -t python/unfold_template.py [options]"
    parser = OptionParser(usage=usage)
    parser.add_option ('-D', '--data', default=defaultdata, help="json data file")
    parser.add_option ('-M', '--matrix', default=defaultmig, help="json migration matrix file")
    parser.add_option ('-B', '--background', default=defaultbkg, help="json background file")
    parser.add_option ('-s', '--seed', default=-1, help='random seed value. should be greater than -1 to ues a different random seed. Default is -1, so same random seed')
    parser.add_option ('-v', '--verbose', help='Toggle verbose', action='store_true', default=False)
    (opts, args) = parser.parse_args()
    jsondata = opts.data
    jsonmig = opts.matrix
    jsonbkg = opts.background
    rndseed = opts.seed
    verbose = opts.verbose

    pyfbu = PyFBU()
    pyfbu.nMCMC            = 10000
    pyfbu.nBurn            = 1000
    pyfbu.nThin            = 10
#    pyfbu.potential = 'Tikhonov'
    import json
    pyfbu.data             = json.load(open(jsondata))
    ndim = len(pyfbu.data)
    pyfbu.lower            = [0]*ndim
    pyfbu.upper            = [140000]*ndim
    pyfbu.response         = json.load(open(jsonmig))
    pyfbu.background       = json.load(open(jsonbkg))
    pyfbu.backgroundsyst = {'bckg':0.1}
    pyfbu.rndseed          = int(rndseed)
    pyfbu.verbose          = verbose
    pyfbu.monitoring = True
    pyfbu.name = 'test'
    pyfbu.run()

    if False:
        trace = pyfbu.trace
        from numpy import mean,std
        mm = mean(trace,1)
        ss = std(trace,1)
        
        pyfbu.lower            = mm-5*ss
        pyfbu.upper            = mm+5*ss
        
        pyfbu.name = 'optim'
        pyfbu.backgroundsyst = {'bckg':0.1}
        pyfbu.nMCMC            = 500000
        pyfbu.nBurn            = 1000
        pyfbu.nThin            = 50
        pyfbu.run()
