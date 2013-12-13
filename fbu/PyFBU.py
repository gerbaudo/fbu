import pymc as mc
from numpy import random, dot, array

class PyFBU(object):
    """A class to perform a MCMC sampling.

    [more detailed description should be added here]

    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """
    #__________________________________________________________
    def __init__(self,data=[],response=[],background={},backgroundsyst={},objsyst={},
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
        self.objsyst        = objsyst
        self.systfixsigma = 0.
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
        objsysts = array(self.objsyst.values())
        ndim = len(data)
        resmat = self.response

        import priors
        truth = priors.wrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    other_args=self.priorparams)

        bckgnuisances = [ mc.Normal('gaus_%s'%name,value=self.systfixsigma if err>0.0 else 0.0,
                                    mu=0.,tau=1.0,
                                    observed=(True if (not err>0.0 or self.systfixsigma!=0) 
                                              else False) )
                          for name,err in self.backgroundsyst.items() ]
        bckgnuisances = mc.Container(bckgnuisances)
        
        objnuisances = [ mc.Normal('gaus_%s'%name,value=self.systfixsigma,mu=0.,tau=1.0,
                                   observed=(True if self.systfixsigma!=0 else False) )
                         for name,err in self.objsyst.items()]
        objnuisances = mc.Container(objnuisances)

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
        def unfold(truth=truth,bckgnuisances=bckgnuisances,objnuisances=objnuisances):
            bckg = dot(1. + bckgnuisances*backgroundsysts,backgrounds)
            reco = dot(truth, resmat)
            smear = 1. + dot(objnuisances,objsysts)
            out = (bckg + reco)*smear
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=ndim)
        allnuisances = mc.Container(bckgnuisances + objnuisances)
        model = mc.Model([unfolded, unfold, truth, truthpot, allnuisances])

        map_ = mc.MAP( model ) # this call determines good initial MCMC values
        map_.fit()

        mcmc = mc.MCMC( model )  # MCMC instance for model

#        for tt,low,up in zip(truth,self.lower,self.upper):
#            mcmc.use_step_method(mc.Metropolis, tt, proposal_distribution='Normal', proposal_sd=(up-low)/100)
#        for gaus in bckgparams+objparams:
#            if not gaus.observed:
#                mcmc.use_step_method(mc.Metropolis, gaus, proposal_distribution='Normal', proposal_sd=0.1)
#        mcmc.sample(5000)
        
        mcmc.use_step_method(mc.AdaptiveMetropolis,truth+allnuisances)
        mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = mcmc.stats()
        self.trace = [mcmc.trace('truth%d'%bin)[:] for bin in xrange(ndim)]
        self.nuisancestrace = {}
        for name,err in self.backgroundsyst.items():
            if err>0.:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s'%name)[:]
        for name in self.objsyst.keys():
            if self.systfixsigma==0.:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s'%name)[:]
        

        if self.monitoring:
            import monitoring
            monitoring.plot(self.name+'_monitoring',data,backgrounds,resmat,self.trace,
                            self.nuisancestrace,self.lower,self.upper)
