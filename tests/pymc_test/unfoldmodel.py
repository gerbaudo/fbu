from pymc import *
from numpy import array, empty

__all__ = ['data', 'migrations', 'truth','unfold','unfolded']

data = array([11064,11804,11780,11135])
nreco = len(data)
def setData(indata):
    global data,reco
    data = indata
    nreco = len(data)

migrations = array([[0.1,0,0,0],
                    [0,0.1,0,0],
                    [0,0,0.1,0],
                    [0,0,0,0.1]])
def setMigrations(migrMatrix):
    global migrations
    migrations = migrMatrix

truth = DiscreteUniform('truth', lower=50000, upper=150000, doc='truth', size=nreco)
def setTruth(hyperbox):
    global truth
    truth = DiscreteUniform('truth', lower=50000, upper=150000, doc='truth', size=nreco)

@deterministic(plot=False)
def unfold(truth=truth):
    out = empty(nreco)
    for r in xrange(nreco):
        tmp=0.
        for t in xrange(nreco):
            tmp += truth[t]*migrations[r][t]
        out[r:r+1] = tmp 
    return out

unfolded = Poisson('unfolded', mu=unfold, value=data, observed=True,size=nreco)

