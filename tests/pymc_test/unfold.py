from pymc import *
from numpy import array,mean,std
import matplotlib.pyplot as plt
from pylab import *
import unfoldmodel

dy_data = array([11064,11804,11780,11135])
migrations = array([[0.1,0,0,0],
                    [0,0.1,0,0],
                    [0,0,0.1,0],
                    [0,0,0,0.1]])

unfoldmodel.setData(dy_data)
unfoldmodel.setMigrations(migrations)
#unfoldmodel.setTruth([50000,150000])

mcmc = MCMC(unfoldmodel)
mcmc.sample(100000,burn=1000,thin=10)

unf_trace = mcmc.trace("truth")[:]
#plt.hist(zip(*unf_trace)[0],bins=100,range=[100000,120000])
plt.hist(zip(*unf_trace)[0],bins=100)
print mean(zip(*unf_trace)[0])
print std(zip(*unf_trace)[0])
show()
