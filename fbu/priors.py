import pymc

import tikhonov
priors = {
    'Tikhonov':tikhonov.tikhonov
    }

def wrapper(priorname='',low=0,up=100,size=1,other_args={}):

    name='truth%d'
    default_args = dict(value=(up-low)/2,lower=low,upper=up)
    args = dict(default_args.items()+other_args.items())
    
    if priorname in priors: 
        prior = priors[priorname] 
    elif hasattr(pymc,priorname):
        prior = getattr(pymc,priorname)
    else:
        print 'WARNING: prior name not found! Falling back to DiscreteUniform...'
        prior = pymc.DiscreteUniform

    truthprior = [prior(name%bin,**args) for bin in xrange(size)]

    return pymc.Container(truthprior)
