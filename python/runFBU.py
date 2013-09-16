import commands
import json
import os

from pymc import MCMC
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import savefig
from pymc.Matplot import plot

############################################
# MCMC configuration
############################################
#number of MCMC trials
nMCMC = 100000

#burn value -> MCMC will skip them
nBurn = 1000

#thin parameter, remove 
nThin = 10
############################################


############################################
# Things to be changed in the template file
############################################
lower = '1000'
upper = '1500'
############################################

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

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option ("-i","--inputFile", help="input template file")
    parser.add_option ("-o","--outputFile", help="where the model is defined")
    parser.add_option ("-v","--verbose", help="Toggle verbose", action="store_true", default=False)
    (opts, args) = parser.parse_args()
    if not opts.inputFile : parser.error('Template not given')
    inputFile  = opts.inputFile
    outputFile = opts.outputFile if opts.outputFile else os.path.dirname(inputFile)+'/'+'mymodel.py'
    verbose    = opts.verbose

    if outputFile[0]=='/': outputFile = outputFile[1:]

    #prepare the model
    if os.path.exists(outputFile) :
        if verbose : print "removing existing ouput '%s'"%outputFile
        os.remove(outputFile)

    projectDir = os.path.dirname(os.path.abspath(__file__)).replace('/python','')
    dataDir = projectDir+'/data/'
    values = {'data'    : asString(json.load(open(dataDir+'data.json'))),
              'mmatrix' : asString(json.load(open(dataDir+'migrations.json'))),
              'lower'   : lower,
              'upper'   : upper,
              'bg'      : getBackground(jsonfname=dataDir+'background.json')
              }

    formatTemplate(inputFile, outputFile, values)

    if verbose : print "importing model '%s'"%outputFile
    mytemplate = __import__(os.path.basename(outputFile).replace('.py',''))
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
