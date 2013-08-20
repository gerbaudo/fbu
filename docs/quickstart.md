Instructions to get started quickly with one of the examples.

Running tests
-------------

```
python -m unittest tests.dummy
```


Installation
------------

The recommended installation is with virtualenv.

First time:

```
git clone git@github.com:gerbaudo/fbu.git
virtualenv fbu
cd fbu
source bin/activate
cat requirements.txt | xargs pip install
python tests/pymc_test/unfold.py
...
deactivate
```

From then on:

```
cd fbu
source bin/activate
python tests/pymc_test/unfold.py
```

The instructions above have been tested with `python>=2.6.6`, on SLC6 and gentoo.
