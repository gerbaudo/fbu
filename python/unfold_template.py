from pymc import *
from numpy import array, empty

#Data points of the distribution to unfold
data = %(data)s

#This is the number of data bins
nreco = len(data)

#Migration matrix truth level -> reconstructed level
migrations = %(mmatrix)s

#define uniformely distributed variable truth, range betweem lower and upper, for nreco variables
truth = DiscreteUniform('truth', lower=%(lower)s, upper=%(upper)s, doc='truth', size=nreco)

#This is where the FBU method is actually implemented
@deterministic(plot=False)
def unfold(truth=truth):
    out = empty(nreco)
    for r in xrange(nreco):
        tmp=0.
        for t in xrange(nreco):
            tmp += truth[t]*migrations[r][t]
        out[r:r+1] = tmp 
    return out


#This is the unfolded distribution
unfolded = Poisson('unfolded', mu=unfold, value=data, observed=True, size=nreco)
