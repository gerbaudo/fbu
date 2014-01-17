import pymc as mc
from numpy import random, dot, array

class PyFBU(object):
    """A class to perform a MCMC sampling.
    
    [more detailed description should be added here]
    
    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """
    #__________________________________________________________
    def __init__(self,data=[],response=[],background={},
                 backgroundsyst={},objsyst={'signal':{},'background':{}},
                 lower=[],upper=[],regularization=None,
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
        self.regularization = regularization
        if not regularization:
            import Regularization
            self.regularization = Regularization.Regularization()
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
        responsetruthbins = self.response
        responserecobins = [row for row in self.response]
        for list in self.background.values()+responserecobins:
            checklen(self.data,list)
        for list in [self.lower,self.upper]:
            checklen(list,responsetruthbins)
    #__________________________________________________________
    def fluctuate(self, data):
        random.seed(self.rndseed)
        return random.poisson(data)
    #__________________________________________________________
    def run(self):
        self.validateinput()
        data = self.data
        data = self.fluctuate(data) if self.rndseed>=0 else data

        # unpack background dictionaries
        backgroundkeys = self.backgroundsyst.keys()
        backgrounds = array([self.background[key] for key in backgroundkeys])
        backgroundnormsysts = array([self.backgroundsyst[key] for key in backgroundkeys])

        # unpack object systematics dictionary
        objsystkeys = self.objsyst['signal'].keys()
        signalobjsysts = array([self.objsyst['signal'][key] for key in objsystkeys])
        backgroundobjsysts = array([])
        if len(objsystkeys)>0 and backgroundkeys>0:
            backgroundobjsysts = array([[self.objsyst['background'][syst][bckg] 
                                         for syst in objsystkeys] 
                                        for bckg in backgroundkeys])
        recodim  = len(data)
        resmat = self.response
        truthdim = len(resmat)

        import priors
        truth = priors.wrapper(priorname=self.prior,
                                    low=self.lower,up=self.upper,
                                    other_args=self.priorparams)

        bckgnuisances = [ mc.Normal('gaus_%s'%name,value=self.systfixsigma if err>0.0 else 0.0,
                                    mu=0.,tau=1.0,
                                    observed=(True if (not err>0.0 or self.systfixsigma!=0) 
                                              else False) )
                          for name,err in zip(backgroundkeys,backgroundnormsysts) ]
        bckgnuisances = mc.Container(bckgnuisances)
        
        objnuisances = [ mc.Normal('gaus_%s'%name,value=self.systfixsigma,mu=0.,tau=1.0,
                                   observed=(True if self.systfixsigma!=0 else False) )
                         for name in objsystkeys]
        objnuisances = mc.Container(objnuisances)

        # define potential to constrain truth spectrum
        truthpot = self.regularization.getpotential(truth)
        
        #This is where the FBU method is actually implemented
        @mc.deterministic(plot=False)
        def unfold(truth=truth,bckgnuisances=bckgnuisances,objnuisances=objnuisances):
            smearbckg = 1.
            if len(backgroundobjsysts)>0:
                smearbckg = smearbckg + dot(objnuisances,backgroundobjsysts) 
            smearedbackgrounds = backgrounds*smearbckg
            bckg = dot(1. + bckgnuisances*backgroundnormsysts,smearedbackgrounds)
            reco = dot(truth, resmat)
            smear = 1. + dot(objnuisances,signalobjsysts)
            out = bckg + reco*smear
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=recodim)
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
        self.trace = [mcmc.trace('truth%d'%bin)[:] for bin in xrange(truthdim)]
        self.nuisancestrace = {}
        for name,err in zip(backgroundkeys,backgroundnormsysts):
            if err>0.:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s'%name)[:]
        for name in objsystkeys:
            if self.systfixsigma==0.:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s'%name)[:]
        

        if self.monitoring:
            import monitoring
            monitoring.plot(self.name+'_monitoring',data,backgrounds,resmat,self.trace,
                            self.nuisancestrace,self.lower,self.upper)
