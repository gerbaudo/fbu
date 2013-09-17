import numpy as np
import pylab as plab

def plotarray(todraw, name):

    plab.figure()
    plab.hist(todraw, bins=50)
    plab.xlabel('unfold Ac')
    plab.ylabel('number of events')
    plab.title('posterior distribution of unfolded Ac')
    plab.savefig('%s.eps'%name,dpi=72)
