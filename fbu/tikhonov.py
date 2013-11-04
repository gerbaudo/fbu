import pymc
import numpy
from math import fabs

def tikhonov(name='Tikhonov',lower=10,upper=1000,size=4,refcurv=6.1e05,alpha=1e-8):
    @pymc.stochastic
    def truth(value=[(lower+upper)/2 for xx in xrange(size)],refcurv=refcurv, alpha=alpha, low=lower, high=upper):

        for val in value:
            if val>high or val<low:
                return -numpy.inf

        def computeCurvature(bin): return value[bin-1]-2.0*value[bin]+value[bin+1]
        curvature = sum([c*c for c in map(computeCurvature,range(1,size-1))])

        deltaCurv = fabs(curvature-refcurv)
        return -deltaCurv*alpha

    return truth
