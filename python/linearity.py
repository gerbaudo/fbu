import numpy as np
import pylab as plab

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

truth  = np.array([-0.029900, -0.017989, -0.006048,  0.024874, 0.044358, 0.064208])
unfold = np.array([-0.013196, -0.00309,  -0.003560,  0.032435, 0.045866, 0.062519])
error  = np.array([0.048970,  0.035875, 0.029474, 0.026788, 0.025932, 0.032679])

unfold = np.array([-0.025084, -0.012933, -0.000005, 0.029309,  0.048371, 0.065852])
error  = np.array([0.016170,  0.016095,  0.015916, 0.016666,  0.015830, 0.016098])


#A6neg mean, std unfolded Ac  -0.025084 , 0.016170
#A4neg mean, std unfolded Ac  -0.012933 , 0.016095
#A2neg mean, std unfolded Ac  -0.000005 , 0.015916
#A2pos mean, std unfolded Ac  0.029309 , 0.016666
#A4pos mean, std unfolded Ac  0.048371 , 0.015830
#A6pos mean, std unfolded Ac  0.065852 , 0.016098


x = plab.linspace(-0.04, 0.08, 10)
y = x
plab.figure()
plab.errorbar(truth, unfold, yerr=error,  fmt='o')
#plab.scatter(truth,unfold, c='b', marker='o', linewidths=0 )
#plab.plot(x, y, 'r')

m,b = plab.polyfit(truth, unfold, 1)
x1 = plab.linspace(-0.04, 0.08, 10)
y1 = m*x + b
plab.plot(x1, y1, 'r')

plab.xlabel('Truth Ac')
plab.ylabel('Unfolded Ac')
plab.title('linearity 4DY bins')
plab.text(0.02, -0.04, r'y = %f*x + %f'%(m,b))

#show()

#plab.hist2d(truth,unfold , bins=10)
plab.savefig("linearity.eps",dpi=72)
