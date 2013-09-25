#!/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from math import sqrt

offset, scale = 100.0, 500.0
num_bins = 50
x = np.random.exponential(scale=1.0, size=1e6) * scale + offset
xm = np.random.normal(loc=4.0, scale=0.25, size=1e5) * scale + offset
xtot = np.concatenate((x, xm))

def smear(x, a=0.5, b=0.1) :
   sigma = a*sqrt(x) + b*x
   return x+np.random.normal(loc=0.0, scale=sigma)

xsmear = [smear(x) for x in xtot]
n, bins, patches = plt.hist(xtot, num_bins, facecolor='green', alpha=0.25, log=True)
n, bins, patches = plt.hist(xsmear, num_bins, facecolor='blue', alpha=0.25, log=True)

plt.show()
plt.savefig('fallingExp_withBump.png')
