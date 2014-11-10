from distutils.core import setup
setup(
    author="Andrew Chapkowski, Mike Miller",
    author_email="achapkowski@esri.com, mmiller@esri.com",
    description="Python hooks for ArcGIS REST API",
    license='Apache',
    url='www.github.com/Esri/ArcREST',
    name='ArcREST',
    version='2.0.100',
    packages=['arcrest','arcrest/agol', 'arcrest/ags', 'arcrest/common',
              'arcrest/manageorg', 'arcrest/security', 'arcrest/web',
              'arcrest/_abstract', 'arcrest/webmap', 'arcrest/geometryservice',
              'arcrest/manageags', 'arcrest/manageportal', 'arcrest/hostedservice'],
    package_dir={'':''}
    )
