import pymc as mc
from numpy import random, dot, array

class PyFBU(object):
    """A class to perform a MCMC sampling.

    [more detailed description should be added here]

    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """
    #__________________________________________________________
    def __init__(self,data=[],response=[],background={},backgroundsyst={},
                 lower=[],upper=[],
                 rndseed=-1,verbose=False,name='',monitoring=False):
        #                                     [MCMC parameters]
        self.nMCMC = 100000 # N of sampling points    
        self.nBurn = 20000  # skip first N sampled points (MCMC learning period)
        self.nThin = 1      # accept every other N sampled point (reduce autocorrelation)
        self.lower = lower  # lower sampling bounds
        self.upper = upper  # upper sampling bounds
        #                                     [unfolding model parameters]
        self.prior = 'DiscreteUniform'
        self.priorparams = {}
        self.potential = ''
        self.potentialparams = {}
        #                                     [input]
        self.data        = data           # data list
        self.response    = response       # response matrix
        self.background  = background     # background dict
        self.backgroundsyst = backgroundsyst
        #                                     [settings]
        self.rndseed   = rndseed
        self.verbose   = verbose
        self.name      = name
        self.monitoring = monitoring
    
    #__________________________________________________________
    def validateinput(self):
        def checklen(list1,list2):
            assert len(list1)==len(list2), 'Input Validation Error: inconstistent size of input'
        response = [self.response]+[row for row in self.response]
        for list in [self.lower,self.upper]+self.background.values()+response:
            checklen(self.data,list)
        
    #__________________________________________________________
    def fluctuate(self, data):
        random.seed(self.rndseed)
        return random.poisson(data)
    #__________________________________________________________
    def run(self):
        self.validateinput()
        data = self.data
        data = self.fluctuate(data) if self.rndseed>=0 else data
        backgrounds = [array(self.background[syst]) for syst in self.backgroundsyst]
        backgroundsysts = array(self.backgroundsyst.values())
        ndim = len(data)
        resmat = self.response

        import priors
        truth = priors.wrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    other_args=self.priorparams)

        gausparams = []
        for name,err in self.backgroundsyst.items():
            gausparams.append( mc.Normal('gaus_%s'%name,value=0,mu=0,tau=1.0,
                                         observed=(False if err>0.0 else True) ))
        gausparams = mc.Container(gausparams)

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
        def unfold(truth=truth,gausparams=gausparams):
            bckg = dot(1.+gausparams*backgroundsysts,backgrounds)
            out = bckg + dot(truth, resmat)
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=ndim)
        model = mc.Model([unfolded, unfold, truth, truthpot, gausparams])

        map_ = mc.MAP( model ) # this call determines good initial MCMC values
        map_.fit()

        mcmc = mc.MCMC( model )  # MCMC instance for model

#        for tt,low,up in zip(truth,self.lower,self.upper):
#            mcmc.use_step_method(mc.Metropolis, tt, proposal_distribution='Normal', proposal_sd=(up-low)/100)
#        for gaus in gausparams:
#            if not gaus.observed:
#                mcmc.use_step_method(mc.Metropolis, gaus, proposal_distribution='Normal', proposal_sd=0.1)
        mcmc.use_step_method(mc.AdaptiveMetropolis,truth+gausparams)
        
        mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = mcmc.stats()
        self.trace = [mcmc.trace('truth%d'%bin)[:] for bin in xrange(ndim)]
        self.bckgtrace = []
        for name,err in self.backgroundsyst.items():
            if err>0.:
                self.bckgtrace.append(mcmc.trace('gaus_%s'%name)[:])
        
        if self.monitoring:
            import monitoring
            monitoring.plot(self.name+'_monitoring',data,backgrounds,resmat,self.trace,
                            self.bckgtrace,self.lower,self.upper)
