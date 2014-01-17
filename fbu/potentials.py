from pymc import Potential

def dummy(**args): return 0. 
from tikhonov import tikhonov
potentialdict = {
    '' : dummy,
    'Tikhonov':tikhonov,
    }

class Regularization(object):
    def __init__(self,regname='',size=1,other_args={}):
        self.regname = regname
        self.size = size
        self.other_args = other_args
        self.function = dummy
        if regname in potentialdict: 
            self.function = potentialdict[regname]
        else:
            print 'WARNING: potential name not found! Falling back to no potential...'

    def wrapper(self,truth=None):
        default_args = dict(value=truth,size=self.size)
        args = dict(default_args.items()+self.other_args.items())
        potential = self.function(**args)
        return potential
    
    def getpotential(self,truth):
        return Potential(self.wrapper,self.regname,self.regname,{'truth':truth})
