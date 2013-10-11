import pymc as mc
import pylab as plab
import numpy as np
from matplotlib import pyplot

import sys, os
sys.path.append(os.getcwd()+'/priors/')


#__________________________________________________________
if __name__ == "__main__":

    flatfunc = mc.DiscreteUniform('flatfunc', 70000, 140000,size=4)
    @mc.deterministic(plot=False)
    def flat(flatfunc=flatfunc): return flatfunc
    mcmc = mc.MCMC([flatfunc,flat])
    mcmc.sample(10000)
    trace_flat = mcmc.trace("flatfunc")[:]


    import Tikhonov
    tikhonov = Tikhonov.Tikhonov_factory(4, 6.1e05, 1e-8, 70000, 140000)
    @mc.deterministic(plot=False)
    def tiko(tikhonov=tikhonov): return tikhonov
    mcmc = mc.MCMC([tikhonov,tiko])
    mcmc.sample(10000)
    trace_tiko = mcmc.trace("tikhonov")[:]
    print trace_tiko[:,0]


    import matplotlib.pyplot as plt
    plt.figure()
    bins = np.linspace(65000, 150000, 100)
    plt.hist(trace_flat[:,0], bins, histtype='stepfilled', normed=True, color='b', label='flat')
    plt.hist(trace_tiko[:,0], bins, histtype='step', normed=True, color='r', label='flat')
    plt.savefig('testoverlay.eps')


