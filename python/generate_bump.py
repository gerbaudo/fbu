#!/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from math import sqrt
import os
from utils import array2json, json2array
from pyFBU import pyFBU

nBinsTruth, truthMin, truthMax = 12, 500.0, 4500.0
nBinsReco,  recoMin,  recoMax  = 12, 500.0, 4500.0

def generateTruthSpectrum(offset=100.0, scale=500.0, nbkg=1e6, nsig=1e5) :
# def generateTruthSpectrum(offset=100.0, scale=500.0, nbkg=10, nsig=2) :
    """Generate pseudo-events with an observable in [offset, scale].
    The observable spectrum is inspired to the one expected for a
    di-jet resonance, where the background is distributed as a falling
    exponential, and the signal is a gaussian on top of it.
    """
    bkg = np.random.exponential(scale=1.0, size=nbkg) * scale + offset
    sig = np.random.normal(loc=4.0, scale=0.25, size=nsig) * scale + offset
    tot = np.concatenate((bkg, sig))
    return tot

def smear(x, a=0.5, b=0.1) :
    """Smear the pseudo-events generated with generateTruthSpectrum as
    to mimic the jet resolution, i.e. with a gaussianely-distributed
    \delta, see eq. 13, eq. 14, and par. 7.1 of the FBU paper.
    """
    sigma = a*sqrt(x) + b*x
    return x+np.random.normal(loc=0.0, scale=sigma)

jsonDir = 'data/bump/'
jsonTruthFname  = jsonDir+'truth.json'
jsonSmearFname  = jsonDir+'reco.json'
jsonResMatFname = jsonDir+'resMat.json'

regenerate = not os.path.exists(jsonResMatFname)
regenerate = True

def normalized(mat) :
    mat = mat.astype(float)
    return mat / mat.sum()

def generateAndPlot() :
    sigPlusBkg = generateTruthSpectrum()
    spbSmeared = np.array([smear(x) for x in sigPlusBkg])
    histTruth, binsTruth        = np.histogram(sigPlusBkg, bins=nBinsTruth, range=(truthMin, truthMax))
    histReco,  binsReco         = np.histogram(spbSmeared, bins=nBinsReco, range=(recoMin, recoMax))
    respHist,  xedges, yedges   = np.histogram2d(sigPlusBkg, spbSmeared, bins=(nBinsTruth, nBinsReco),
                                                 range=((truthMin, truthMax), (recoMin,  recoMax)))
    print 'in truth histo ',histTruth.shape,': ',histTruth
    print 'in reco histo  ',histReco.shape ,': ',histReco
    print 'in respHist    ',respHist.shape ,': ',respHist
    def prMatrix(recoVsTruthCounts) :
        """
        This matrix is p(r|t). Given recoVsTruthCounts, where truth is
        on axis=0 and reco is on axis=1, we can just obtain the p(r|t)
        matrix by normalizing each bin [t][r] by the total N of evts
        in that 'row' [t]:

           [t][r] -> [t][r]/sum([[t][r] for r in nreco])

        With np this can be done with the broadcasting mechanims. Try:
        a = np.array([[1., 2.],
                      [3., 4.]])
        a / np.sum(a, axis=1)[:,np.newaxis]
        --> [[ 0.33333333,  0.66666667],
             [ 0.42857143,  0.57142857]]
        And see for example
        http://stackoverflow.com/questions/7140738/numpy-divide-along-axis)
        """
        den = np.sum(recoVsTruthCounts, axis=1)[:,np.newaxis]
        den[den==0.0]=1.0 # avoid divide by zero; if all values in this row are zero, 0./1. is still 0.
        return recoVsTruthCounts / den
#return recoVsTruthCounts / truthCounts.astype('float')[:,np.newaxis]
    respMat = prMatrix(respHist)
    print 'respMat :'
    print respMat
    def plotTruthAndReco(histT, binsT, histR, binsR, outfname) :
        def getWidth(bins) : return bins[1] - bins[0]
        plt.figure()
        plt.bar(binsT[:-1], histT, color='b', width=getWidth(binsT), alpha=0.15)
        plt.bar(binsR[:-1], histR, color='r', width=getWidth(binsR), alpha=0.15)
        plt.savefig(outfname)
    def plotRespMatrix(respMatrix, xedges, yedges, outfname) :
        from matplotlib.colors import LogNorm
        extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
        plt.figure()
        plt.imshow(respMatrix, extent=extent, interpolation='nearest', norm=LogNorm(), origin='lower')
        plt.colorbar()
        plt.savefig(outfname)
    plotTruthAndReco(histTruth, binsTruth, histReco, binsReco, 'fallingExp_withBump.png')
    plotRespMatrix(respHist, xedges, yedges, 'responseMatrix.png')
    return histTruth, histReco, respMat

histTruth, histReco, respMat = None, None, None
if regenerate :
    histTruth, histReco, respMat = generateAndPlot()
    if not os.path.isdir(jsonDir) : os.path.mkdir(jsonDir)
    for a,f in [(histTruth, jsonTruthFname),
                (histReco,  jsonSmearFname),
                (respMat,   jsonResMatFname)] :
        array2json(a,f)
else :
    histTruth  = json2array(jsonTruthFname)
    histReco   = json2array(jsonSmearFname),
    respMat    = json2array(jsonResMatFname)

print 'histTruth : ',histTruth
print 'histReco : ',histReco
print 'respMat : ',respMat
pyfbu = pyFBU()
pyfbu.nMCMC        = 100000
pyfbu.nBurn        = 100
pyfbu.nThin        = 10
pyfbu.lower        = 1
pyfbu.upper        = 140000
pyfbu.jsonData     = jsonSmearFname
pyfbu.jsonMig      = jsonResMatFname
pyfbu.verbose      = True # verbose ? will be on cmd-line

pyfbu.run()

trace = pyfbu.trace
print trace
estMean   = np.mean(trace, axis=0)
estMedian = np.median(trace, axis=0)
estStd    = np.std(trace, axis=0)
print 'estMean: ',estMean
print 'estMedian: ',estMedian
xdata = np.linspace(truthMin, truthMax, nBinsTruth)
binW = (truthMax-truthMin)/nBinsTruth
plt.figure()
print 'xdata ',len(xdata)
print 'histTruth ',len(histTruth)
plt.bar(xdata, histTruth, color='b', width=binW, alpha=0.15)
#plt.bar(xdata, histReco, color='r',  width=binW, alpha=0.15)

plt.errorbar(xdata+0.5*binW, estMedian, yerr=estStd, fmt='k.')
plt.savefig('foo.png')
