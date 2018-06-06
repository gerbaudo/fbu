import pymc3 as mc
from numpy import random, dot, array, inf
import theano

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
        self.nTune = 1000
        self.nMCMC = 10000 # N of sampling points
        self.target_accept = 0.95
        self.lower = lower  # lower sampling bounds
        self.upper = upper  # upper sampling bounds
        #                                     [unfolding model parameters]
        self.prior = 'DiscreteUniform'
        self.priorparams = {}
        self.regularization = regularization
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
        for bin in list(self.background.values())+responserecobins:
            checklen(self.data,bin)
        for bin in [self.lower,self.upper]:
            checklen(bin,responsetruthbins)
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
        nbckg = len(backgroundkeys)
        
        if nbckg>0:
            backgrounds = array([self.background[key] for key in backgroundkeys])
            backgroundnormsysts = array([self.backgroundsyst[key] for key in backgroundkeys])

        # unpack object systematics dictionary
        objsystkeys = self.objsyst['signal'].keys()
        nobjsyst = len(objsystkeys)
        if nobjsyst>0:
            signalobjsysts = array([self.objsyst['signal'][key] for key in objsystkeys])
            if nbckg>0:
                backgroundobjsysts = array([])
                backgroundobjsysts = array([[self.objsyst['background'][syst][bckg] 
                                             for syst in objsystkeys] 
                                            for bckg in backgroundkeys])

        recodim  = len(data)
        resmat = self.response
        truthdim = len(resmat)

        model = mc.Model()
        from .priors import wrapper
        with model:
            truth = wrapper(priorname=self.prior,
                            low=self.lower,up=self.upper,
                            other_args=self.priorparams)
            
            if nbckg>0:
                bckgnuisances = []
                for name,err in zip(backgroundkeys,backgroundnormsysts):
                    if err<0.:
                        bckgnuisances.append( 
                            mc.Uniform('norm_%s'%name,lower=0.,upper=3.)
                            )
                    else:
                        BoundedNormal = mc.Bound(mc.Normal, lower=(-1.0/err if err>0.0 else -inf))
                        bckgnuisances.append(
                            BoundedNormal('gaus_%s'%name,
                                          mu=0.,tau=1.0)
                            )
                bckgnuisances = mc.math.stack(bckgnuisances)
        
            if nobjsyst>0:
                objnuisances = [ mc.Normal('gaus_%s'%name,mu=0.,tau=1.0#,
                                           #observed=(True if self.systfixsigma!=0 else False) 
                                           )
                                 for name in objsystkeys]
                objnuisances = mc.math.stack(objnuisances)

        # define potential to constrain truth spectrum
            if self.regularization:
                truthpot = self.regularization.getpotential(truth)
        
        #This is where the FBU method is actually implemented
            def unfold():
                smearbckg = 1.
                if nbckg>0:
                    bckgnormerr = [(-1.+nuis)/nuis if berr<0. else berr 
                                         for berr,nuis in zip(backgroundnormsysts,bckgnuisances)]
                    bckgnormerr = mc.math.stack(bckgnormerr)
                    
                    smearedbackgrounds = backgrounds
                    if nobjsyst>0:
                        smearbckg = smearbckg + theano.dot(objnuisances,backgroundobjsysts) 
                        smearedbackgrounds = backgrounds*smearbckg
                        
                    bckg = theano.dot(1. + bckgnuisances*bckgnormerr,smearedbackgrounds)

                tresmat = array(resmat)
                reco = theano.dot(truth, tresmat)
                out = reco
                if nobjsyst>0:
                    smear = 1. + theano.dot(objnuisances,signalobjsysts)
                    out = reco*smear
                if nbckg>0:
                    out = bckg + out
                return out

            unfolded = mc.Poisson('unfolded', mu=unfold(), 
                                  observed=array(data))

            trace = mc.sample(self.nMCMC,tune=self.nTune,target_accept=self.target_accept)
        
            self.trace = [trace['truth%d'%bin][:] for bin in range(truthdim)]
            self.nuisancestrace = {}
            if nbckg>0:
                for name,err in zip(backgroundkeys,backgroundnormsysts):
                    if err<0.:
                        self.nuisancestrace[name] = trace['norm_%s'%name][:]
                    if err>0.:
                        self.nuisancestrace[name] = trace['gaus_%s'%name][:]
            for name in objsystkeys:
                if self.systfixsigma==0.:
                    self.nuisancestrace[name] = trace['gaus_%s'%name][:]

        if self.monitoring:
            import monitoring
            monitoring.plot(self.name+'_monitoring',data,backgrounds,resmat,self.trace,
                            self.nuisancestrace,self.lower,self.upper)
