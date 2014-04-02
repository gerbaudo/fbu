from math import fabs

def tikhonov(value,refcurv=6.1e05,alpha=1e-8):
    def computeCurvature(bin): return value[bin-1]-2.0*value[bin]+value[bin+1]
    curvature = sum([c*c for c in map(computeCurvature,range(1,len(value)-1))])
    deltaCurv = fabs(curvature-refcurv)
    return -deltaCurv*alpha

