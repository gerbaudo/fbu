import numpy as np
import pylab as plab

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

truth  = np.array([-0.029900, -0.017989, -0.006048,  0.024874, 0.044358, 0.064208])


def dolinearityplot(unfold, error):
    plab.figure()
    plab.errorbar(truth, unfold, yerr=error,  fmt='o')

    m,b = plab.polyfit(truth, unfold, 1)
    x = plab.linspace(-0.04, 0.08, 10)
    y = m*x + b
    plab.plot(x, y, 'r')

    plab.xlabel('Truth Ac')
    plab.ylabel('Unfolded Ac')
    plab.title('linearity 4DY bins')
    plab.text(0.02, -0.04, r'y = %f*x + %f'%(m,b))
    plab.savefig("linearity.eps",dpi=72)

    flag = True
    
    if b > 0.005: 
        flag = flag*False
        print 'offset > 0.05 NOT ok'
    if abs(1-m) > 0.05: 
        flag = flag*False
        print 'slope away from 1 by more than 5% NOT ok'

    return flag
