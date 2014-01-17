from pymc import Potential,Container

def dummy(**args): return 0. 
from tikhonov import tikhonov
potentialdict = {
    '' : dummy,
    'Tikhonov':tikhonov,
    }

class Regularization(object):
    def __init__(self,regname='',ntotbins=1,ndiffbins=1,other_args={}):
        self.regname = regname
        assert ntotbins>0 and ndiffbins>0, 'ERROR: ntotbins and ndiffbins must be >0'
        self.edges = [(0,ntotbins)]
        if ntotbins%ndiffbins!=0: 
            print 'WARNING: inconsistent number of bins! Falling back to no potential...'
            self.regname = ''
        else:
            nbins = ntotbins/ndiffbins
            self.edges = [(ii,ii+nbins) for ii in range(0,ntotbins,nbins)]
        self.other_args = other_args
        self.function = dummy
        if self.regname in potentialdict: 
            self.function = potentialdict[self.regname]
        else:
            print 'WARNING: potential name not found! Falling back to no potential...'

    def wrapper(self,truth=None):
        default_args = dict(value=truth)
        args = dict(default_args.items()+self.other_args.items())
        potential = self.function(**args)
        return potential
    
    def getpotential(self,truth):
        potentials = [Potential(self.wrapper,self.regname,self.regname,
                                {'truth':truth[start:end]})
                      for (start,end) in self.edges]
        return Container(potentials)
