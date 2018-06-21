import io
from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = f.read()

INSTALL_DEPS = ['pyjwt[crypto]>=1.5.2',
                'future>=0.16.0']
FLASK_DEPS = ['flask>=0.12.2']
TEST_DEPS = ['pytest',
             'python-testdata-tsi>=0.2.0.1'] + FLASK_DEPS
DEV_DEPS = FLASK_DEPS

setup(
    name='aap-client-python',

    # https://pypi.python.org/pypi/setuptools_scm
    use_scm_version=True,

    description='AAP Client',
    long_description=LONG_DESC,

    url='https://github.com/EMBL-EBI-TSI/aap-client-python',

    author='Pau Ruiz Safont',
    author_email='psafont@ebi.ac.uk',

    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='aap jose jwt auth flask',

    packages=find_packages(exclude=['examples', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=INSTALL_DEPS,

    setup_requires=['setuptools_scm'],

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': DEV_DEPS,
        'test': TEST_DEPS,
        'flask': FLASK_DEPS
    },
)
