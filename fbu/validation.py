import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import mean,std,arange
import pymc
from pymc.Matplot import plot as mcplot

def plot(dirname,data,bkgd,resmat,trace,bckgtrace,lower=0,upper=0):
    import os
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    mcplot(bckgtrace,common_scale=False)
    plt.savefig(dirname+'/pymc_summary_bckgs.eps')
    plt.close()
    mcplot(trace,common_scale=False)
    plt.savefig(dirname+'/pymc_summary_bins.eps')
    plt.close()

    trace = trace[:]
    bckgtrace = bckgtrace[:]
    nbins = len(data)
    bintrace = zip(*trace)

    for bin in xrange(nbins): 
        ax = plt.subplot(311)
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
        plt.subplot(312)
        x = arange(len(trace))
        plt.plot(x,trace[:,bin],label='trace of bin %d'%bin)
        plt.subplot(313)
        plt.plot(x,bckgtrace[:,0],label='trace of background')
        plt.savefig(dirname+'/bin%s.eps'%bin)
        plt.close()
