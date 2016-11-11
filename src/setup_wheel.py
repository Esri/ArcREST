"""
ArcREST Setup Code

"""
from setuptools import setup, find_packages
from codecs import open
from os import path
import re

with open('arcrest/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)



here = path.abspath(path.dirname(__file__))

packages = ['arcresthelper','arcresthelper/packages',
            'arcrest','arcrest/agol','arcrest/agol/helperservices', 'arcrest/ags', 'arcrest/common',
            'arcrest/manageorg', 'arcrest/security', 'arcrest/web',
            'arcrest/_abstract', 'arcrest/webmap', 'arcrest/geometryservice',
            'arcrest/manageags', 'arcrest/manageportal', 'arcrest/hostedservice',
            'arcrest/enrichment', 'arcrest/opendata', 'arcrest/cmp', 'arcrest/packages',
            'arcrest/packages/ntlm3']

# Get the long description from the README file
try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_decription = f.read()
except:
    long_decription = "ArcREST Python Package"

setup(
    name='ArcREST_Package',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='ArcREST is a Python Wrapper for the Esri REST Framework',
    long_description=long_decription,
    # The project's main homepage.
    url='https://github.com/Esri/ArcREST',
    # Author details
    author='Andrew Chapkowski, Mike Miller',
    author_email='achapkowski@esri.com, mmiller@esri.com',
    # Choose your license
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    keywords='REST, Esri, ArcGIS, Python, ArcPy',
    packages=packages,
    include_package_data=True,
    zip_safe=True,
    install_requires=['numpy>=1.7.1'],
    extras_require={},
    package_data={'arcrest/enrichment' : ['__countrycodes.csv', '__datacollectionnames.csv']},
)
