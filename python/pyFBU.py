import commands
import json
import os

import pymc as mc
from numpy import array,mean,std, empty

import matplotlib.pyplot as plt
from pylab import savefig
from pymc.Matplot import plot


class pyFBU(object):
    """A class to perform a MCMC sampling for an unfolding model.
    The model is specified with a template whose numerical values are
    filled in reading the inputs from json values.

    [more detailed description should be added here]

    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """
    #__________________________________________________________
    def __init__(self):
        self.templateFile  = None  #required
        self.nMCMC = 100000 # N trials        [begin MCMC parameters]
        self.nBurn = 1000   # todo: describe
        self.nThin = 10     # todo: describe
        self.lower = 1000   # lower sampling bound
        self.upper = 1500   # upper sampling bound
        #                                     [begin numerical parameters]
        self.projectDir = os.path.dirname(os.path.abspath(__file__)).replace('/python','')
        self.dataDir = self.projectDir+'/data/'
        self.jsonData = self.dataDir+'data.json'       # json data file
        self.jsonMig  = self.dataDir+'migrations.json' # json migration matrix file
        self.jsonBkg  = self.dataDir+'background.json' # json background file

        # model name
        self.modelName     = 'mymodel'

        # verbose
        self.verbose       = False # Toggle verbose

        # mcmc model and statistics
        self.mcmc  = None
        self.stats = None
        self.trace = None
        
 
    #__________________________________________________________
    def asString(self, value) : return str(value)

    #__________________________________________________________
    def getBackground(self, jsonfname='', variation='Nominal') :
        """Read bkg from json file. Note that because we are using this to
        fill in a template, we are returning a string, and not the actual
        numerical values.
        """
        nameBkg1 = 'BG'
        valuesBkg1 = json.load(open(jsonfname))[nameBkg1][variation]
        return { 'background1' : valuesBkg1 }

    #__________________________________________________________
    def run(self):
 
        # Data points of the distribution to unfold
        data = array(json.load(open(self.jsonData)))

        # Background distribution
        bkgd = self.getBackground(self.jsonBkg)

        #This is the number of data bins
        nreco = len(data)

        #Migration matrix truth level -> reconstructed level
        migrations = array(json.load(open(self.jsonMig)))

        #define uniformely distributed variable truth, range betweem lower and upper, for nreco variables
        truth = mc.DiscreteUniform('truth', lower=self.lower, upper=self.upper, doc='truth', size=nreco)

#        import Tikhonov
#        truth = Tikhonov.Tikhonov_factory(nreco, 6.1e05, 1e-8, self.lower, self.upper)

#        import DiscreteUniform
#        truth = DiscreteUniform.myDiscreteUniform_factory(4, self.lower, self.upper)


        #This is where the FBU method is actually implemented
        #__________________________________________________________
        @mc.deterministic(plot=False)
        def unfold(truth=truth):
            out = empty(nreco)
            for r in xrange(nreco):
                tmp=0.
                for b in bkgd:
                    tmp+=bkgd[b][r]
                for t in xrange(nreco):
                    tmp += truth[t]*migrations[r][t]
                    out[r:r+1] = tmp 
            return out

        #This is the unfolded distribution
        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=nreco)

        # Define the model using the model class
        model = mc.Model([unfolded, unfold, truth])

        # Call MAP before MCMC to find good starting MCMC values
        map_ = mc.MAP( model )
        map_.fit() 

        
        #Define the MCMC model
        self.mcmc = mc.MCMC( model )
        self.mcmc.use_step_method(mc.AdaptiveMetropolis, truth)
        self.mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = self.mcmc.stats()
        self.trace = self.mcmc.trace("truth")[:]

        plot(self.mcmc)
        savefig("Summary_%s.eps"%self.modelName)
