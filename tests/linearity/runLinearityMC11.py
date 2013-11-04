#! /bin/env python

import sys, os
import json
import numpy as np

from fbu.PyFBU import PyFBU
from tests.linearity import computeAc, linearity
from utils import plot

def count_outside_range(elements, hi, lo): return sum(1 for e in elements if e>hi or e<lo)
#__________________________________________________________
if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))+'/'
    lin_dir = 'tests/linearity/'
    pyfbu = PyFBU()
    pyfbu.nMCMC = 100000
    pyfbu.nBurn = 1000
    pyfbu.nThin = 10
    pyfbu.verbose = False
    json_dir = lin_dir+'data/mc11/'
    pyfbu.lower, pyfbu.upper = 70000, 140000
    pyfbu.response       = json.load(open(json_dir+'migrations.json'))
    pyfbu.background     = json.load(open(json_dir+'background.json'))

    labels = ["A%s%s"%(ax, pn) for pn in ['pos','neg'] for ax in [2, 4, 6]]
    data_fnames = ["data%s.json"%l for l in labels]
    meanAc, stdAc = [], []
    TestPassed = True
    for label, data_fname in zip(labels, data_fnames):
        pyfbu.data  = json.load(open(json_dir+data_fname))
        pyfbu.modelName = data_fname.replace('.json','')
        pyfbu.run()
        # np.save('outputFile'+data_fname.replace('.json',''),trace) # un-needed? DG 2013-10-27
        acValues = np.array(computeAc.computeAcList(pyfbu.trace))
        meanAc.append(np.mean(acValues))
        stdAc.append(np.std(acValues))
        plot_fname = out_dir+'Ac_posterior_'+label+'.png'
        plot.plotarray(acValues, plot_fname)
        mean, sigma = np.mean(acValues), np.std(acValues)
        num_outsiders = count_outside_range(acValues, mean+3.*sigma, mean-3.*sigma)
        ratio = float(num_outsiders)/float(len(pyfbu.trace))
        if ratio>0.0027:
            print ("outsiders: %i, ratio  %f"%(num_outsiders, ratio)
                   +'-->> this is NOT ok, should be < 0.0027 (3sigmas)')
            TestPassed = TestPassed and False
    meanAc, stdAc = np.array(meanAc), np.array(stdAc)
    TestPassed = TestPassed and linearity.dolinearityplot(meanAc, stdAc, out_dir+'linearity.eps')
    if TestPassed: print 'TEST PASSED'
    else :         print 'TEST FAILED'
