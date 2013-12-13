import pymc

priors = {
    }

def wrapper(priorname='',low=[],up=[],other_args={},optimized=False):

    
    if priorname in priors: 
        priormethod = priors[priorname] 
    elif hasattr(pymc,priorname):
        priormethod = getattr(pymc,priorname)
    else:
        print 'WARNING: prior name not found! Falling back to DiscreteUniform...'
        priormethod = pymc.DiscreteUniform

    truthprior = []
    for bin,(l,u) in enumerate(zip(low,up)):
        name = 'truth%d'%bin
        default_args = dict(name=name,value=l+(u-l)/2,lower=l,upper=u)
        args = dict(default_args.items()+other_args.items())
        prior = priormethod(**args)
        truthprior.append(prior)

    return pymc.Container(truthprior)
