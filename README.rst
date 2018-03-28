[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FEMBL-EBI-TSI%2Faap-client-python.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FEMBL-EBI-TSI%2Faap-client-python?ref=badge_shield)

.. image:: https://travis-ci.org/EMBL-EBI-TSI/aap-client-python.svg?branch=master
    :target: https://travis-ci.org/EMBL-EBI-TSI/aap-client-python
.. image:: https://codecov.io/gh/EMBL-EBI-TSI/aap-client-python/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/EMBL-EBI-TSI/aap-client-python
.. image:: https://coveralls.io/repos/github/EMBL-EBI-TSI/aap-client-python/badge.svg?branch=master
  :target: https://coveralls.io/github/EMBL-EBI-TSI/aap-client-python?branch=master


Overview
########

This library can be used to interface with the AAP, although it is also able to sign tokens.
(for testing the verification is done correctly)

Cryptographic files here shouldn't be used in production, they're just for testing :)

Usage
#####

To install the package, enable the virtual environment where it's going to be used and run
``$ pip install aap-client-python``

To use the Flask functionality this needs to be installed:
``$ pip install aap-client-python[flask]``

Developing
##########

To prepare the environment for developing the library, create a virtual environment, go to project root and then run:

::

  $ pip install -e .[dev]

Testing
#######
The recommended way is to test using detox.
This allows for testing in all the supported python versions using virtual environments effortlessly.
To use, install it, then run in the project root:

::

  $ pip install detox
  $ detox

Alternatively, testing can be done in the same environment as the dev one by installing it's dependecies, then running pytest:

::

  $ pip install -e .[test]
  $ python -m pytest -s


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FEMBL-EBI-TSI%2Faap-client-python.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FEMBL-EBI-TSI%2Faap-client-python?ref=badge_large)