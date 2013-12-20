.. image:: https://travis-ci.org/gerbaudo/fbu.png
   :target: https://travis-ci.org/gerbaudo/fbu

=====
PyFBU
=====

Implementation of the Fully Bayesian Unfolding algorithm described in
`physics.data-an/1201.4612 <http://arxiv.org/abs/1201.4612>`_.
The software is based on the Markov Chain Monte Carlo sampling toolkit 
`PyMC <http://pymc-devs.github.io/pymc/>`_.

Dependencies
------------

PyFBU is tested on Python 2.6/2.7 and depends on NumPy, Matplotlib and PyMC.

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


Pip installation
~~~~~~~~~~~~~~~~

The latest stable version of PyFBU can be installed using pip.

::
 
    pip install fbu

This will also automatically install other missing dependencies
(this might take another while, up to several minutes...).

Git clone
~~~~~~~~~

Alternatively one can check out the development version of the code from the 
`GitHub <https://github.com/gerbaudo/fbu>`_ repository:

::

	git clone https://github.com/gerbaudo/fbu.git

and follow the `quickstart <https://github.com/gerbaudo/fbu/blob/master/docs/quickstart.md>`_ 
instructions.


Usage
-----

A `simple tutorial <http://nbviewer.ipython.org/github/gerbaudo/fbu/blob/master/tutorial.ipynb>`_
to help you get started.
