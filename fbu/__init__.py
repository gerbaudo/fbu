__version__ = '0.0.3'

try:
    import numpy
except ImportError:
    raise ImportError(
        'NumPy does not seem to be installed. Please see the installation guide.')

from .PyFBU import PyFBU
from .Regularization import Regularization

from .tests import test
