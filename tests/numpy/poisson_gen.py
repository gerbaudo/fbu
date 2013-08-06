
import sys
import numpy as np

mu=2500.00
nEvts = int(sys.argv[1])
s = np.random.poisson(mu, nEvts)
