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
    defaultdata = datadir+'data.json'
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
    pyfbu.nMCMC            = 100000
    pyfbu.nBurn            = 1000
    pyfbu.nThin            = 10
    pyfbu.lower            = 0
    pyfbu.upper            = 140000
#    pyfbu.prior            = 'Tikhonov'
    import json
    pyfbu.data             = json.load(open(jsondata))
    pyfbu.response         = json.load(open(jsonmig))
    pyfbu.background       = json.load(open(jsonbkg))
    pyfbu.backgroundsyst = {'bckg':0.20}
    pyfbu.monitoring = True
    pyfbu.rndseed          = int(rndseed)
    pyfbu.verbose          = verbose
    pyfbu.monitoring = True
    pyfbu.name = 'test'
    pyfbu.run()

    trace = pyfbu.trace

#    AcList  = computeAc.computeAcList(trace)
#    AcArray = np.array(AcList)
#    meanAc  = np.mean(AcArray)
#    stdAc   = np.std(AcArray)
