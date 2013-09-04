import commands, os
from pymc import MCMC
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import savefig

#histTruth
truthhist = array([104303.6640625,105277.6796875,105633.7109375,106462.5078125])


#histReco
data        = 'array([11064.75,11804.203125,11780.1181640625,11135.34375])'

#Truth versus Reco Migration matrix from protos MC, 2011 7TeV charge asymmetry analysis (closure test)
migrations  = 'array([[0.063770,0.022177,0.011848,0.007905],[0.022544,0.051560,0.026740,0.011981],[0.011556,0.026787,0.051118,0.022614],[0.007696,0.011584,0.021881,0.062564]])'
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
    parser.add_option ("-o","--outputFile", help="where the model is defined")
    parser.add_option ("-v","--verbose", help="Toggle verbose", action="store_true", default=False)
    (opts, args) = parser.parse_args()
    if not opts.inputFile : parser.error('Template not given')
    inputFile  = opts.inputFile
    outputFile = opts.outputFile if opts.outputFile else os.path.dirname(inputFile)+'/'+'mymodel.py'
    verbose    = opts.verbose

    #prepare the model
    if os.path.exists(outputFile) :
        if verbose : print "removing existing ouput '%s'"%outputFile
        os.remove(outputFile)
    values = {'data':data,
              'mmatrix':migrations,
              'lower':truth_do,
              'upper':truth_up
              }
    formatTemplate(inputFile, outputFile, values)
    if verbose : print "importing model '%s'"%outputFile
    mytemplate = __import__(os.path.basename(outputFile).replace('.py',''))
    mcmc = MCMC(mytemplate)
    mcmc.sample(100000,burn=1000,thin=10)
    unf_trace = mcmc.trace("truth")[:]
    print unf_trace
    #plt.hist(zip(*unf_trace)[0],bins=100,range=[100000,120000])
    plt.hist(zip(*unf_trace)[0],bins=100)
    print'\n'
    print mean(zip(*unf_trace)[0])
    print std(zip(*unf_trace)[0])
    savefig("outplot.eps")
