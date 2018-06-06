import pymc3 as mc

priors = {
    }

def wrapper(priorname='',low=[],up=[],other_args={},optimized=False):

    
    if priorname in priors: 
        priormethod = priors[priorname] 
    elif hasattr(mc,priorname):
        priormethod = getattr(mc,priorname)
    else:
        print( 'WARNING: prior name not found! Falling back to DiscreteUniform...' )
        priormethod = mc.DiscreteUniform

    truthprior = []
    for bin,(l,u) in enumerate(zip(low,up)):
        name = 'truth%d'%bin
        default_args = dict(name=name,lower=l,upper=u)
        args = dict(list(default_args.items())+list(other_args.items()))
        prior = priormethod(**args)
        truthprior.append(prior)

    return mc.math.stack(truthprior) #https://github.com/pymc-devs/pymc3/issues/502
