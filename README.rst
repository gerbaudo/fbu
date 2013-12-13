. image:: https://travis-ci.org/gerbaudo/fbu.png
   :target: https://travis-ci.org/gerbaudo/fbu

=====
PyFBU
=====

Implementation of the Fully Bayesian Unfolding algorithm described in
`physics.data-an/1201.4612 <http://arxiv.org/abs/1201.4612>`_.
The software is based on the Markov Chain Monte Carlo sampling toolkit PyMC.

Dependencies
------------

PyFBU is tested on Python 2.7 and depends on NumPy, Matplotlib and PyMC.

Installation
------------

The use of an isolated Python environment is recommended:

::
 
    virtualenv ENVFBU
    cd ENVFBU
    source bin/activate

Install NumPy-1.7.0 (this may take a while).

::

	pip install numpy==1.7.0


The latest version of PyFBU can be installed using pip.

::
 
    pip install fbu

This will also automatically install the other missing dependencies
(this might take another while, up to several minutes...and lots of printout).
