from setuptools import setup

DISTNAME = 'fbu'
DESCRIPTION = "PyFBU"
#VERSION = '0.0.2'
VERSION = '0.0.3dev.3'
AUTHOR = 'Davide Gerbaudo, Clement Helsens and Francesco Rubbo'
AUTHOR_EMAIL = 'rubbo.francesco@gmail.com'
URL = 'https://github.com/gerbaudo/fbu'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Physics',
    'Operating System :: OS Independent',
    ]

required = ['numpy>=1.7.0','scipy>=0.12.0','matplotlib>=1.2.1','pymc==2.3','emcee']

setup(
    name=DISTNAME,
    version=VERSION,
    packages=['fbu','fbu.tests'],
    license='LICENSE.txt',
    long_description=open('README.rst','rt').read(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=classifiers,
    install_requires=required
    )
    
##to upload package
## python setup.py sdist
## python setup.py sdist upload
