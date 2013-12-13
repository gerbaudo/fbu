import pymc

def dummy(**args): return 0. 
from tikhonov import tikhonov
potentialdict = {
    '' : dummy,
    'Tikhonov':tikhonov,
    }

def wrapper(potname='',truth=None,size=1,other_args={}):

    potential = 0.
    if potname in potentialdict: 
        potmethod = potentialdict[potname] 
        default_args = dict(value=truth,size=size)
        args = dict(default_args.items()+other_args.items())
        potential = potmethod(**args)

    return potential
