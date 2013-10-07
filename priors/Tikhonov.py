import pymc
import numpy
from math import fabs

def Tikhonov_factory(nreco=4, refcurv=6.1e05,alpha=1e-8, t_l=10, t_h=1000):
    @pymc.stochastic
    def truth(value=[(t_l+t_h)/2 for xx in xrange(nreco)],refcurv=refcurv, alpha=alpha, low=t_l, high=t_h):

        for val in value:
            if val>high or val<low:
                return -numpy.inf

        def computeCurvature(bin): return value[bin-1]-2.0*value[bin]+value[bin+1]
        curvature = sum([c*c for c in map(computeCurvature,range(1,nreco-1))])

        deltaCurv = fabs(curvature-refcurv)
        return -deltaCurv*alpha

    return truth
