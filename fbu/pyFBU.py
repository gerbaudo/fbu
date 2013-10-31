import commands
import os

import pymc as mc
from numpy import array,mean,std, empty, empty_like, random

import matplotlib.pyplot as plt
from pylab import savefig
from pymc.Matplot import plot


class pyFBU(object):
    """A class to perform a MCMC sampling.

    [more detailed description should be added here]

    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """
    #__________________________________________________________
    def __init__(self):
        self.nMCMC = 100000 # N trials        [begin MCMC parameters]
        self.nBurn = 1000   # todo: describe
        self.nThin = 10     # todo: describe
        self.lower = 1000   # lower sampling bound
        self.upper = 1500   # upper sampling bound
        self.prior = 'DiscreteUniform'
        self.priorParams = {}
        #                                     [begin numerical parameters]
        self.Data           = None # data list
        self.ResponseMatrix = None # response matrix
        self.Background     = None # background dict
        self.rndseed   = -1
        self.mcmc      = None # clarify these attributes (better names? required by pymc?)
        self.stats     = None
        self.trace     = None
        self.modelName = 'mymodel' #model name, will be used to save plots with a given name 
        self.verbose   = False
    #__________________________________________________________
    def fluctuate(self, data):
        random.seed(self.rndseed)
        return random.poisson(data)
    #__________________________________________________________
    def run(self):
        data = array(self.Data)
        data = self.fluctuate(data) if self.rndseed>=0 else data
        bkgd = self.Background['bckg'] 
        nreco = len(data)
        resmat = array(self.ResponseMatrix)

        import priors
        truth = priors.PriorWrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    theSize=nreco,
                                    other_args=self.priorParams)


        #This is where the FBU method is actually implemented
        @mc.deterministic(plot=False)
        def unfold(truth=truth):
            out = empty(nreco)
            for r in xrange(nreco):
                # out[r] =  sum(b[r] for b in bkgd.values()) if bkgd else 0.0
                out[r] =  bkgd[r]
                out[r] += sum(truth[t]*resmat[r][t] for t in xrange(nreco))
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=nreco)
        model = mc.Model([unfolded, unfold, truth])
        map_ = mc.MAP( model ) # this call determines good initial MCMC values
        map_.fit()
        self.mcmc = mc.MCMC( model )  # Define the MCMC model (DG?? clarify, it was defined above)
        self.mcmc.use_step_method(mc.AdaptiveMetropolis, truth)
        self.mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = self.mcmc.stats()
        self.trace = self.mcmc.trace("truth")[:]

        plot(self.mcmc)
        savefig("Summary_%s.eps"%self.modelName)
