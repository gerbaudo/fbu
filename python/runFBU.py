import commands
import json
import os

from pymc import MCMC
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import savefig
from pymc.Matplot import plot

# MCMC parameters
nMCMC = 100000 # N trials
nBurn = 1000   # todo: describe
nThin = 10     # todo: describe

# model parameters (other numerical values read in from inputs)
lower = 1000 # lower sampling bound
upper = 1500 # upper sampling bound


def asString(val) : return str(val)

def formatTemplate(infile, outfile, values={}) :
    f=open(outfile, 'w')
    f.write(open(infile).read()%values)
    f.flush()
    f.close()

def getBackground(jsonfname='', variation='Nominal') :
    """Read bkg from json file. Note that because we are using this to
    fill in a template, we are returning a string, and not the actual
    numerical values.
    """
    nameBkg1 = 'BG'
    valuesBkg1 = str(json.load(open(jsonfname))[nameBkg1][variation])
    return "{ 'background1' : %s }" % valuesBkg1
def defaultModelFname(templateFname='') :
    return os.path.dirname(os.path.abspath(templateFname))+'/mymodel.py'

if __name__ == "__main__":
    projectDir = os.path.dirname(os.path.abspath(__file__)).replace('/python','')
    dataDir = projectDir+'/data/'
    defaultData = dataDir+'data.json'
    defaultMig  = dataDir+'migrations.json'
    defaultBkg  = dataDir+'background.json'
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option ('-D', '--data',       default=defaultData, help="json data file")
    parser.add_option ('-M', '--matrix',     default=defaultMig,  help="json migration matrix file")
    parser.add_option ('-B', '--background', default=defaultBkg,  help="json background file")
    parser.add_option ('-t', '--template',   help='input model template file')
    parser.add_option ('-m', '--model',      help='where the model will be defined')
    parser.add_option ('-v', '--verbose',    help='Toggle verbose', action='store_true', default=False)
    (opts, args) = parser.parse_args()
    if not opts.template : parser.error('Template not given')
    jsonData      = opts.data
    jsonMig       = opts.matrix
    jsonBkg       = opts.background
    templateFile  = opts.template
    modelFile     = opts.model if opts.model else defaultModelFname(templateFile)
    verbose       = opts.verbose

    if verbose :
        print 'Options:'
        print '\n'.join("%s : %s"%(v, str(eval(v))) for v in ['jsonData','jsonMig','jsonBkg',
                                                              'templateFile','modelFile'])
    #prepare the model
    if os.path.exists(modelFile) :
        if verbose : print "removing existing model '%s'"%modelFile
        os.remove(modelFile)

    values = {'data'    : asString(json.load(open(jsonData))),
              'mmatrix' : asString(json.load(open(jsonMig))),
              'lower'   : asString(lower),
              'upper'   : asString(upper),
              'bg'      : getBackground(jsonBkg)
              }

    formatTemplate(templateFile, modelFile, values)

    if verbose : print "importing model '%s'"%modelFile
    mytemplate = __import__(os.path.basename(modelFile).replace('.py',''))
    mcmc = MCMC(mytemplate)
    mcmc.sample(nMCMC,burn=nBurn,thin=nThin)

    plot(mcmc)
    mcmc.stats()
    unf_trace = mcmc.trace("truth")[:]
    print unf_trace
    #plt.hist(zip(*unf_trace)[0],bins=100,range=[100000,120000])
    plt.hist(zip(*unf_trace)[0],bins=100)
    print'\n'
    print mean(zip(*unf_trace)[0])
    print std(zip(*unf_trace)[0])
    savefig("outplot.eps")
