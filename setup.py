from distutils.core import setup

setup(
    name='fbu',
    version='0.0.1dev.7',
    packages=['fbu',],
    license='LICENSE.txt',
    long_description=open('README.rst','rt').read(),
    url='https://pypi.python.org/pypi/fbu',
    author='Davide Gerbaudo,Clement Helsens,Francesco Rubbo',
    author_email='rubbo.francesco@gmail.com',
    )
    
##to upload package
## python setup.py sdist
## python setup.py sdist upload
