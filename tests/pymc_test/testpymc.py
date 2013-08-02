import scipy.stats as stats
from pylab import *
import matplotlib.pyplot as plt
from pymc import *
import testmodel

mcmc = MCMC(testmodel)
mcmc.sample(50000)

unf_trace = mcmc.trace("truth")
print unf_trace
unf_trace  = unf_trace[:]
print unf_trace

#plot( unf_trace, label = "trace", c = "#348ABD", lw=1)
#plt.title("trace")
#savefig("test.png")

mcmc.sample(100000)
unf_trace = mcmc.trace("truth")[:]

plt.hist(unf_trace[:],color="#348ABD",bins=30,histtype="stepfilled")
show()
