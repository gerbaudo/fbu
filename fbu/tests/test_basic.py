from numpy.testing import assert_,assert_raises,run_module_suite
from numpy import mean,std

from fbu import PyFBU

class Test:
    def test_run(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.run()
        trace = fbu_.trace
        for bin,expected in zip(trace,[800,1600]):
            assert_(mean(bin)+std(bin)>expected)

    def test_bckg(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.background       = {'bckg1': [5,20],'bckg2': [5,30]}
        fbu_.backgroundsyst   = {'bckg1': 0.,'bckg2': 0.}
        fbu_.run()
        trace = fbu_.trace
        for bin,expected in zip(trace,[700,1000]):
            assert_(mean(bin)+std(bin)>expected)

    def test_bckgsyst(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.background       = {'bckg1': [5,20]}
        fbu_.backgroundsyst   = {'bckg1': 0.2}
        fbu_.run()
        trace = fbu_.trace
        for bin,expected in zip(trace,[700,1000]):
            assert_(mean(bin)+std(bin)>expected)

    def test_objsyst(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.objsyst['signal']={
            'syst':[0.05,0.05],
            }
        fbu_.run()
        trace = fbu_.trace
        for bin,expected in zip(trace,[800,1600]):
            assert_(mean(bin)+std(bin)>expected)
