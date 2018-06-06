.. image:: https://travis-ci.org/gerbaudo/fbu.png
   :target: https://travis-ci.org/gerbaudo/fbu

=====
PyFBU
=====

Implementation of the Fully Bayesian Unfolding algorithm described in
`physics.data-an/1201.4612 <http://arxiv.org/abs/1201.4612>`_.
The software is based on the Bayesian statistical modeling package
`PyMC3 <http://docs.pymc.io/index.html>`_.

Dependencies
------------

PyFBU is tested on Python 3.6.3 within Anaconda 4.3.30 and depends on PyMC 3.

Installation
------------

The use of an isolated Python environment is recommended:

::

    conda create --name fbuenv
    source activate fbuenv

PyMC 3 can be installed using conda

::

   conda install -c conda-forge pymc3

or pip

::

    pip install git+https://github.com/pymc-devs/pymc3


The latest stable version of PyFBU can be installed using pip.

::
 
    pip install fbu

Alternatively one can check out the development version of the code from the 
`GitHub <https://github.com/gerbaudo/fbu>`_ repository:

::

	git clone https://github.com/gerbaudo/fbu.git


Usage
-----

A `simple tutorial <tutorial.ipynb>`_ to help you get started.

