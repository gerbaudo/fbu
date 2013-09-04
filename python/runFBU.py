import commands, os
from pymc import *
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import *

#histTruth
truthhist = array([104303.6640625,105277.6796875,105633.7109375,106462.5078125])


#histReco
data        = 'array([11064.75,11804.203125,11780.1181640625,11135.34375])'

#Truth versus Reco Migration matrix from protos MC, 2011 7TeV charge asymmetry analysis (closure test)
migrations  = 'array([[0.063770,0.022177,0.011848,0.007905],[0.022544,0.051560,0.026740,0.011981],[0.011556,0.026787,0.051118,0.022614],[0.007696,0.011584,0.021881,0.062564]])'
truth_do    = '5000'
truth_up    = '150000'

def inplace_change(infile, outfile, old_string, new_string):
        s=open(infile).read()
        if old_string in s:
                print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
                s=s.replace(old_string, new_string)
                f=open(outfile, 'w')
                f.write(s)
                f.flush()
                f.close()
        else:
                print 'No occurances of "{old_string}" found.'.format(**locals())


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option ("-i","--inputFile",
                       help="input files to be uses as template",
                       dest="inputFile",
                       default="")
    parser.add_option ("-v","--verbose",
                       help="Turn on verbose printout",
                       dest="verbose",
                       action="store_true",
                       default=False)
    
    (options, args) = parser.parse_args()
    inputFile = options.inputFile
    verbose   = options.verbose

    #prepare the model
    outputFile = 'mytemplate.py'
    if os.path.exists(outputFile):
        commands.getstatusoutput('rm %s'%outputFile)

    inplace_change(inputFile , outputFile, '@DATA@'   , data)
    inplace_change(outputFile, outputFile, '@MMATRIX@', migrations)
    inplace_change(outputFile, outputFile, '@LOW@'    , truth_do)
    inplace_change(outputFile, outputFile, '@HIGH@'   , truth_up)


    #Import the model
    import mytemplate
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
