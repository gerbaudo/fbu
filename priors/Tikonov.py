import pymc
import numpy
from math import fabs

def Tikonov_factory(nreco=4, refcurv=6.1e05,alpha=1e-8, t_l=10, t_h=1000):
    @pymc.stochastic
    def truth(value=[(t_l+t_h)/2 for xx in xrange(nreco)],refcurv=refcurv, alpha=alpha, low=t_l, high=t_h):

        for val in value:
            if val>high or val<low:
                return -numpy.inf

        tikonov = 0.
        for ii in xrange(1,nreco-1):
            tikonov += (value[ii+1]-2*value[ii]+value[ii-1])**2
        deltaCurv = fabs(tikonov-refcurv)
        return -deltaCurv*alpha

    return truth
