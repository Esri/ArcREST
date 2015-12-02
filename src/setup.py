from distutils.core import setup
setup(
    author="Andrew Chapkowski, Mike Miller",
    author_email="achapkowski@esri.com, mmiller@esri.com",
    description="Python hooks for ArcGIS REST API",
    license='Apache',
    url='www.github.com/Esri/ArcREST',
    name='ArcREST',
    version='3.5.0',
    packages=['arcresthelper',
              'arcrest','arcrest/agol','arcrest/agol/helperservices', 'arcrest/ags', 'arcrest/common',
              'arcrest/manageorg', 'arcrest/security', 'arcrest/web',
              'arcrest/_abstract', 'arcrest/webmap', 'arcrest/geometryservice',
              'arcrest/manageags', 'arcrest/manageportal', 'arcrest/hostedservice',
              'arcrest/enrichment', 'arcrest/security/ntlm3'],
    package_data = {'arcrest/enrichment' : ['__countrycodes.csv', '__datacollectionnames.csv']},
    install_requires=['six'],
    package_dir={'':''}
    )
