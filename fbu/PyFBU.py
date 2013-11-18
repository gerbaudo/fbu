import pymc as mc
from numpy import empty, random

class PyFBU(object):
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
        self.lower = []   # lower sampling bound
        self.upper = []   # upper sampling bound
        self.prior = 'DiscreteUniform'
        self.priorparams = {}
        self.potential = ''
        self.potentialparams = {}
        #                                     [begin numerical parameters]
        self.data        = None # data list
        self.response    = None # response matrix
        self.background  = None # background dict
        self.rndseed   = -1
        self.stats     = None
        self.trace     = None
        self.verbose   = False
        self.name      = '' 
        self.monitoring = False
    #__________________________________________________________
    def fluctuate(self, data):
        random.seed(self.rndseed)
        return random.poisson(data)
    #__________________________________________________________
    def run(self):
        data = self.data
        data = self.fluctuate(data) if self.rndseed>=0 else data
        bkgd = self.background['bckg'] 
        ndim = len(data)
        resmat = self.response

        import priors
        truth = priors.wrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    size=ndim,
                                    other_args=self.priorparams)

        # define potential to constrain truth spectrum
        import potentials
        if self.potential in potentials.potentialdict:
            @mc.potential
            def truthpot(truth=truth):
                return potentials.wrapper(self.potential,
                                          truth,size=ndim,
                                          other_args=self.potentialparams)
        else:
            print 'WARNING: potential name not found! Falling back to no potential...'
            @mc.potential
            def truthpot():
                return 0.
        
        #This is where the FBU method is actually implemented
        @mc.deterministic(plot=False)
        def unfold(truth=truth):
            out = empty(ndim)
            for r in xrange(ndim):
                out[r] =  bkgd[r]
                out[r] += sum(truth[t]*resmat[r][t] for t in xrange(ndim))
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=ndim)
        model = mc.Model([unfolded, unfold, truth, truthpot])
        map_ = mc.MAP( model ) # this call determines good initial MCMC values
        map_.fit()
        mcmc = mc.MCMC( model )  # MCMC instance for model
        mcmc.use_step_method(mc.AdaptiveMetropolis, truth)
        mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = mcmc.stats()
        self.trace = [mcmc.trace('truth%d'%bin)[:] for bin in xrange(ndim)]

        if self.monitoring:
            import validation
            validation.plot(self.name,data,bkgd,resmat,self.trace,
                            self.lower,self.upper)

