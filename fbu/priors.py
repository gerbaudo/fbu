import pymc

import tikhonov
priors = {
    'Tikhonov':tikhonov.tikhonov
    }

def wrapper(priorname='',low=0,up=100,theSize=1,other_args={}):

    default_args = dict(name='truth',
                        lower=low,
                        upper=up,
                        size=theSize)
    args = dict(default_args.items()+other_args.items())
    
    if priorname in priors: 
        return priors[priorname](**args)
    elif hasattr(pymc,priorname):
        return getattr(pymc,priorname)(**args)
    else:
        print 'WARNING: prior name not found! Falling back to DiscreteUniform...'
        return pymc.DiscreteUniform(**args)
