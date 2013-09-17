#! /bin/env python
###################
# davide.gerbaudo@cern.ch clement.helsens@cern.ch, francesco.rubbo@cern.ch
###################
#
# Class    pyFBU
# Package  pyFBU
#
############################
#
# Main class to run pyFBU
#
#############################               
import commands
import json
import os

from pymc import MCMC
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import savefig
from pymc.Matplot import plot


class pyFBU(object):

    #__________________________________________________________
    def __init__(self):

        # MCMC default parameters
        self.nMCMC = 100000 # N trials
        self.nBurn = 1000   # todo: describe
        self.nThin = 10     # todo: describe

        # model default parameters (other numerical values read in from inputs)
        self.lower = 1000 # lower sampling bound
        self.upper = 1500 # upper sampling bound

        # project directory
        self.projectDir = os.path.dirname(os.path.abspath(__file__)).replace('/python','')

        # data directory
        self.dataDir = self.projectDir+'/data/'

        # load default example
        self.jsonData = self.dataDir+'data.json'       # json data file
        self.jsonMig  = self.dataDir+'migrations.json' # json migration matrix file
        self.jsonBkg  = self.dataDir+'background.json' # json background file

        # template file. If no templateFile given can not run
        self.templateFile  = None

        # model name
        self.modelName     = 'mymodel'

        # model file (will change the template file to this name). If no modelFile given, will use the default name
        self.modelFile     = None

        # verbose
        self.verbose       = False # Toggle verbose

        # mcmc model and statistics
        self.mcmc  = None
        self.stats = None
        self.trace = None

    #__________________________________________________________
    def setnMCMC(self, value): self.nMCMC = value
    #__________________________________________________________
    def setnBurn(self, value): self.nBurn = value
    #__________________________________________________________
    def setnThin(self, value): self.nThin = value


    #__________________________________________________________
    def setlower(self, value): self.lower = value
    #__________________________________________________________
    def setupper(self, value): self.upper = value
    #__________________________________________________________
    def setBounds(self, low, up): 
        self.lower = low
        self.upper = up

    #__________________________________________________________
    def setprojectDir(self, value): self.projectDir = value

    #__________________________________________________________
    def setdataDir(self, value): self.dataDir = value

    #__________________________________________________________
    def setjsonData(self, value): self.jsonData = value
    #__________________________________________________________
    def setjsonMig(self, value): self.jsonMig = value
    #__________________________________________________________
    def setjsonBkg(self, value): self.jsonBkg = value

    #__________________________________________________________
    def settemplateFile(self, value): self.templateFile = value

    #__________________________________________________________
    def setmodelName(self, value): self.modelName = value


    #__________________________________________________________
    def setverbose(self, value): self.verbose = value

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
 
        if self.templateFile == '' : 
            print 'ERROR Template not given'
            sys.exit(0)

        print 'model file  ',self.modelFile
        print 'model Name  ',self.modelName

        self.modelFile = self.defaultModelFname(self.templateFile)

        if self.verbose :
            print 'Options:'
            print '\n'.join("%s : %s"%(v, str(eval(v))) for v in ['jsonData','jsonMig','jsonBkg',
                                                                  'templateFile','modelFile'])
        #prepare the model
        if os.path.exists(self.modelFile) :
            if self.verbose : print "removing existing model '%s'"%self.modelFile
            os.remove(self.modelFile)

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

        #print 'model name : %s'%self.modelName
        plot(self.mcmc)
        savefig("Summary_%s.eps"%self.modelName)

        #plt.hist(zip(*self.trace)[0],bins=100)
        #savefig("Summary_%s.eps"%self.modelName)
