#!/bin/env python

import os
from pyFBU import pyFBU
from optparse import OptionParser

#__________________________________________________________
if __name__ == "__main__":
    projectDir = os.path.dirname(os.path.abspath(__file__)).replace('/python','')
    dataDir = projectDir+'/data/mc11/'
    defaultData = dataDir+'data.json'
    defaultMig  = dataDir+'migrations.json'
    defaultBkg  = dataDir+'background.json'
    usage = "usage: %prog -t python/unfold_template.py [options]"
    parser = OptionParser(usage=usage)
    parser.add_option ('-D', '--data', default=defaultData, help="json data file")
    parser.add_option ('-M', '--matrix', default=defaultMig, help="json migration matrix file")
    parser.add_option ('-B', '--background', default=defaultBkg, help="json background file")
    parser.add_option ('-s', '--seed', default=-1, help='random seed value. should be greater than -1 to ues a different random seed. Default is -1, so same random seed')
    parser.add_option ('-v', '--verbose', help='Toggle verbose', action='store_true', default=False)
    (opts, args) = parser.parse_args()
    jsonData = opts.data
    jsonMig = opts.matrix
    jsonBkg = opts.background
    rndseed = opts.seed
    verbose = opts.verbose

    pyfbu = pyFBU()
    pyfbu.nMCMC        = 100000
    pyfbu.nBurn        = 1000
    pyfbu.nThin        = 10
    pyfbu.lower        = 70000
    pyfbu.upper        = 140000
    pyfbu.jsonData     = jsonData
    pyfbu.jsonMig      = jsonMig
    pyfbu.jsonBkg      = jsonBkg
    pyfbu.rndseed      = int(rndseed)
    pyfbu.verbose      = verbose
    
    pyfbu.run()

    trace = pyfbu.trace

#    AcList  = computeAc.computeAcList(trace)
#    AcArray = np.array(AcList)
#    meanAc  = np.mean(AcArray)
#    stdAc   = np.std(AcArray)
