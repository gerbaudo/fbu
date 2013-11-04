import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import mean,std

def plot(name,data,bkgd,resmat,trace,lower=0,upper=0):
    dirname = name+'_monitoring'
    import os
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    nbins = len(data)
    bintrace = zip(*trace)
    for bin in xrange(nbins): 
        fig = plt.figure(num=bin)
        ax = fig.add_subplot(111)
        xx = bintrace[bin]
        mu = mean(xx)
        sigma = std(xx)
        n, bins, patches = plt.hist(xx, 50, normed=1, facecolor='green', alpha=0.5, histtype='stepfilled')
        yy = mlab.normpdf(bins,mu,sigma)
        plt.plot(bins,yy,'r-')
        plt.ylabel('Probability')
        plt.xlabel('Bin content')
        ymean = mean(ax.get_ylim())
        plt.hlines(ymean,lower,upper,linestyles='dashed',colors='m',label='hyperbox')
        plt.vlines(data[bin],0.,ymean,linestyles='solid',colors='c',label='data')
        plt.xlim(xmin=0)
        plt.savefig(dirname+'/bin%s.eps'%bin)
