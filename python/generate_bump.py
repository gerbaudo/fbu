#!/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from math import sqrt
import os
from utils import array2json, json2array
from pyFBU import pyFBU

regenerate = True

def generateTruthSpectrum(offset=100.0, scale=500.0, nbkg=1e6, nsig=1e5) :
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

def normalized(mat) :
    mat = mat.astype(float)
    return mat / mat.sum()

def generateAndPlot() :
    sigPlusBkg = generateTruthSpectrum()
    spbSmeared = np.array([smear(x) for x in sigPlusBkg])
    numBins = 50
    nBinsTruth, truthMin, truthMax = 50, 500.0, 4500.0
    nBinsReco,  recoMin,  recoMax  = 50, 500.0, 4500.0
    histTruth, binsTruth        = np.histogram(sigPlusBkg, bins=nBinsTruth, range=(truthMin, truthMax))
    histReco,  binsReco         = np.histogram(spbSmeared, bins=nBinsReco, range=(recoMin, recoMax))
    respHist,  xedges, yedges   = np.histogram2d(sigPlusBkg, spbSmeared, bins=(nBinsTruth, nBinsReco),
                                                 range=((truthMin, truthMax), (recoMin,  recoMax)))
    respMat = normalized(respHist)
    respMat = np.flipud(respMat) # histogram2d returns the y axis reversed (see docs)
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

pyfbu = pyFBU()
pyfbu.nMCMC        = 100000
pyfbu.nBurn        = 1000
pyfbu.nThin        = 10
pyfbu.lower        = 70000
pyfbu.upper        = 140000
pyfbu.jsonData     = jsonSmearFname
pyfbu.jsonMig      = jsonResMatFname
pyfbu.jsonBkg      = '' # this shouldnt be a requirement; pass [0.] ?
pyfbu.templateFile = '' # templateFile  ?
pyfbu.modelName    = '' # modelName if modelName else pyfbu.modelName ? I thought this wasn't necessary anymore
pyfbu.verbose      = True # verbose ? will be on cmd-line

pyfbu.run()

trace = pyfbu.trace
