import commands, os
from pymc import *
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import *

data        = 'array([11064,11804,11780,11135])'
migrations  = 'array([[0.1,0,0,0],[0,0.1,0,0],[0,0,0.1,0],[0,0,0,0.1]])'
truth_do    = '5000'
truth_up    = '150000'

def formatTemplate(infile, outfile, values={}) :
        f=open(outfile, 'w')
        f.write(open(infile).read()%values)
        f.flush()
        f.close()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option ("-i","--inputFile", help="input template file")
    parser.add_option ("-v","--verbose", help="Toggle verbose", action="store_true", default=False)
    (options, args) = parser.parse_args()
    inputFile = options.inputFile
    verbose   = options.verbose

    #prepare the model
    outputFile = 'mytemplate.py'
    if os.path.exists(outputFile):
        commands.getstatusoutput('rm %s'%outputFile)
    values = {'data':data,
              'mmatrix':migrations,
              'lower':truth_do,
              'upper':truth_up
              }
    formatTemplate(inputFile, outputFile, values)
    #Import the model
    import mytemplate
    mcmc = MCMC(mytemplate)
    mcmc.sample(100000,burn=1000,thin=10)

    unf_trace = mcmc.trace("truth")[:]
    #plt.hist(zip(*unf_trace)[0],bins=100,range=[100000,120000])
    plt.hist(zip(*unf_trace)[0],bins=100)
    print'\n'
    print mean(zip(*unf_trace)[0])
    print std(zip(*unf_trace)[0])
    savefig("outplot.eps")
