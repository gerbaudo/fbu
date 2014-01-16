from numpy.testing import assert_,assert_raises,run_module_suite

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
        for bin in trace:
            assert_(len(bin)==80000)

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
        for bin in trace:
            assert_(len(bin)==80000)

    def test_bckgsyst(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.background       = {'bckg1': [5,20],'bckg2': [5,30]}
        fbu_.backgroundsyst   = {'bckg1': 0.5,'bckg2': 0.5}
        fbu_.run()
        trace = fbu_.trace
        for bin in trace:
            assert_(len(bin)==80000)

    def test_objsyst(self):
        fbu_ = PyFBU()
        fbu_.data = [100,150]        
        fbu_.response = [[0.08,0.02],[0.02,0.08]]
        fbu_.lower = [0,0]
        fbu_.upper = [3000,3000]
        fbu_.objsyst['signal']={
            'jes':[0.05,0.05],
            'jer':[0.03,0.03]
            }
        fbu_.run()
        trace = fbu_.trace
        for bin in trace:
            assert_(len(bin)==80000)
