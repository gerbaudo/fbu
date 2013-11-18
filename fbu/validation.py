import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import mean,std,arange,array
import pymc
from pymc.Matplot import plot as mcplot
from pymc.Matplot import geweke_plot

def plot(dirname,data,bkgd,resmat,trace,bckgtrace,lower=0,upper=0):
    import os
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    dirname = os.path.normpath(dirname) + os.sep

    ndim = len(data)
    # overlay data and background
    x = arange(0.5,ndim+0.5)
    plt.plot(x,data,'k',label='data',drawstyle='steps-mid')
    plt.plot(x,array(bkgd).sum(axis=0),'b',label='background',drawstyle='steps-mid')
    plt.ylim([0.,max(data)*1.3])
    plt.xlim([0.,len(data)])
    plt.savefig(dirname+'databckg.eps')
    plt.close()

    # plot traces and autocorrelation
    mcplot(bckgtrace,common_scale=False,suffix='_summary',path=dirname,format='eps')
    mcplot(trace,common_scale=False,suffix='_summary',path=dirname,format='eps')
    plt.close()

    # plot geweke test
    trace = trace[:]
    scores = pymc.geweke(trace)
    geweke_plot(scores,'truth',path=dirname,format='eps')
    plt.close()
    
    # raftery lewis test
    pymc.raftery_lewis(scores, q=0.975, r=0.005)

    bckgtrace = bckgtrace[:]
    nbins = len(data)
    bintrace = zip(*trace)

    for bin in xrange(nbins): 
        ax = plt.subplot(211)
        xx = bintrace[bin]
        mu = mean(xx)
        sigma = std(xx)
        n, bins, patches = plt.hist(xx, bins=50, normed=1, facecolor='green', alpha=0.5, histtype='stepfilled')
        yy = mlab.normpdf(bins,mu,sigma)
        plt.plot(bins,yy,'r-')
        plt.ylabel('Probability')
        plt.xlabel('Bin content')
        ymean = mean(ax.get_ylim())
        plt.hlines(ymean,lower,upper,linestyles='dashed',colors='m',label='hyperbox')
        plt.vlines(data[bin],0.,ymean,linestyles='solid',colors='c',label='data')
        plt.xlim(xmin=0)
        plt.subplot(212)
        x = arange(len(trace))
        plt.plot(x,trace[:,bin],label='trace of bin %d'%bin)
        plt.savefig(dirname+'bin%s.eps'%bin)
        plt.close()
