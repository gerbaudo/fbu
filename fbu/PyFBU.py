import pymc as mc
from numpy import empty, random, dot

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
        self.lower = 1000   # lower sampling bound
        self.upper = 1500   # upper sampling bound
        self.prior = 'DiscreteUniform'
        self.priorparams = {}
        #                                     [begin numerical parameters]
        self.data        = None # data list
        self.response    = None # response matrix
        self.background  = None # background dict
        self.backgroundsyst = None
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
        bkgd = [self.background[syst] for syst in self.backgroundsyst] 

        print bkgd
        ndim = len(data)
        resmat = self.response

        import priors
        truth = priors.wrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    size=ndim,
                                    other_args=self.priorparams)

        def smear(bckg):
            return bckg[0]


        #This is where the FBU method is actually implemented
        @mc.deterministic(plot=False)
        def unfold(truth=truth):
            out = empty(ndim)
            bckg = smear(bkgd)
            out = bckg + dot(truth, resmat)
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=ndim)
        model = mc.Model([unfolded, unfold, truth])
        map_ = mc.MAP( model ) # this call determines good initial MCMC values
        map_.fit()
        mcmc = mc.MCMC( model )  # MCMC instance for model
        mcmc.use_step_method(mc.AdaptiveMetropolis, truth)
        mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = mcmc.stats()
        self.trace = mcmc.trace("truth")[:]

        if self.monitoring:
            import validation
            validation.plot(self.name+'_monitoring',data,bkgd,resmat,self.trace,
                                 self.lower,self.upper)

