"""
ArcREST Setup Code

"""
from distutils.core import setup
from codecs import open
from os import path


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
    name='ArcREST',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='3.5.3',

    description='ArcREST is a Python Wrapper for the Esri REST Framework',
    long_description=long_decription,
    # The project's main homepage.
    url='https://github.com/Esri/ArcREST',
    # Author details
    author='Andrew Chapkowski, Mike Miller',
    author_email='achapkowski@esri.com, mmiller@esri.com',
    # Choose your license
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers/GIS Users',
        'Topic :: Software Development :: Esri REST API',

        # Pick your license as you wish (should match "license" above)
        'License :: Apache License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='REST, Esri, ArcGIS, Python, ArcPy',
    packages=packages,
    package_dir={'requests': 'requests'},
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy>=1.7.1'],
    extras_require={},
    package_data={'arcrest/enrichment' : ['__countrycodes.csv', '__datacollectionnames.csv']},
)
