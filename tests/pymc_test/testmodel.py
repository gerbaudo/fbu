from pymc import *
from numpy import array, empty
from numpy.random import randint

__all__ = ['dy_data', 'truth','unfold','dy_unfolded']

dy_data = array([11064,11804,11780,11135])

truth = DiscreteUniform('truth', lower=50000, upper=150000, doc='truth')

@deterministic(plot=False)
def unfold(t=truth):
    out = empty(len(dy_data))
    out[0:-1] = t*0.1
    return out

dy_unfolded = Poisson('dy_unfolded', mu=unfold, value=dy_data, observed=True)

