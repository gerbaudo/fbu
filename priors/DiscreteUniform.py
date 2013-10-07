import pymc
import numpy

def myDiscreteUniform_factory(nreco, t_l=10, t_h=1000):
    @pymc.stochastic(dtype=int)
    def truth(value=[(t_l+t_h)/2 for xx in xrange(nreco)], t_l=t_l, t_h=t_h):
        """The switchpoint for the rate of disaster occurrence."""
        
        for val in value:
            if val>t_h or val<t_l:
                return -numpy.inf

        return -numpy.log(t_h - t_l + 1)


    return truth
