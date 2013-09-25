import commands
import json
import os

from pymc import MCMC
from numpy import array,mean,std
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


        self.modelName     = 'mymodel'
        self.modelFile     = ''
        self.verbose       = False

        # mcmc model and statistics
        self.mcmc  = None
        self.stats = None
        self.trace = None
    #__________________________________________________________
    def asString(self, value) : return str(value)
    #__________________________________________________________
    def formatTemplate(self, infile, outfile, values={}) :
        f=open(outfile, 'w')
        f.write(open(infile).read()%values)
        f.flush()
        f.close()
    #__________________________________________________________
    def getBackground(self, jsonfname='', variation='Nominal') :
        """Read bkg from json file. Note that because we are using this to
        fill in a template, we are returning a string, and not the actual
        numerical values.
        """
        nameBkg1 = 'BG'
        valuesBkg1 = str(json.load(open(jsonfname))[nameBkg1][variation])
        return "{ 'background1' : %s }" % valuesBkg1
    #__________________________________________________________
    def defaultModelFname(self, templateFname='') :
        return os.path.dirname(os.path.abspath(templateFname))+'/'+self.modelName+'.py'
    #__________________________________________________________
    def run(self):
        assert self.templateFile, "A template is required"
        self.modelFile = self.modelFile if self.modelFile else self.defaultModelFname(self.templateFile)
        if self.verbose :
            print 'Options:'
            print '\n'.join("%s : %s"%(v, str(eval(v))) for v in ['jsonData','jsonMig','jsonBkg',
                                                                  'templateFile','modelFile'])
        def removeExistingModelFile(filename, verbose) :
            if os.path.exists(filename) :
                if verbose : print "removing existing model '%s'"%filename
                os.remove(filename)
        removeExistingModelFile(self.modelFile, self.verbose)
        values = {'data'    : self.asString(json.load(open(self.jsonData))),
                  'mmatrix' : self.asString(json.load(open(self.jsonMig))),
                  'lower'   : self.asString(self.lower),
                  'upper'   : self.asString(self.upper),
                  'bg'      : self.getBackground(self.jsonBkg)
                  }
        self.formatTemplate(self.templateFile, self.modelFile, values)
        if self.verbose : print "importing model '%s'"%self.modelFile
        mytemplate = __import__(os.path.basename(self.modelFile).replace('.py',''))

        self.mcmc = MCMC(mytemplate)
        self.mcmc.sample(self.nMCMC,burn=self.nBurn,thin=self.nThin)
        self.stats = self.mcmc.stats()
        self.trace = self.mcmc.trace("truth")[:]
        plot(self.mcmc,"Summary_%s.eps"%self.modelName)
    #__________________________________________________________
