#! /bin/env python
###################
# davide.gerbaudo@cern.ch clement.helsens@cern.ch, francesco.rubbo@cern.ch
###################
# usage:
# python runPriors.py 
###################

import sys, os
sys.path.append(os.getcwd()+'/python/')
sys.path.append(os.getcwd()+'/priors/')
sys.path.append(os.getcwd()+'/tests/linearity/')

from pyFBU import pyFBU

import computeAc
import plot
import numpy as np

def Integral(array, up, down):
    nb=0
    print 'up=%f   down=%f'%(up,down)
    for i in array:
        if i>up or i<down:nb+=1
    return nb

#__________________________________________________________
if __name__ == "__main__":
    Dir = '/afs/cern.ch/user/h/helsens/TopWork/Unfolding/fbu/'
    pyfbu = pyFBU()

    pyfbu.nMCMC    = 100000
    pyfbu.setnBurn = 1000
    pyfbu.setnThin = 10
    
    pyfbu.lower = 400000
    pyfbu.upper = 900000

    data = 'dataA2pos.json'

    pyfbu.jsonMig = Dir+'data/mc12/migrations.json'
    pyfbu.jsonBkg = Dir+'data/mc12/background.json'
    pyfbu.jsonData  = Dir+'data/mc12/'+data
    pyfbu.modelName = data.replace('.json','')

    pyfbu.run()
    trace = pyfbu.trace
    AcListmc12  = computeAc.computeAcList(trace)
    AcArraymc12 = np.array(AcListmc12)

    #mc11
    pyfbu.lower = 70000
    pyfbu.upper = 140000

    pyfbu.jsonMig = Dir+'data/mc11/migrations.json'
    pyfbu.jsonBkg = Dir+'data/mc11/background.json'
    pyfbu.jsonData  = Dir+'data/mc11/'+data
    pyfbu.modelName = data.replace('.json','')

    pyfbu.run()
    trace = pyfbu.trace
    AcListmc11  = computeAc.computeAcList(trace)
    AcArraymc11 = np.array(AcListmc11)


    print 'RMS mc11 = %f   mc12=%f'%(np.std(AcArraymc11),np.std(AcArraymc12))

    ListArray = [AcArraymc11,AcArraymc12]

    plot.plotarraymulti(ListArray,'Ac_posterior_mc11-12_'+data.replace('.json',''))
