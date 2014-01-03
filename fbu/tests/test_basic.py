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
