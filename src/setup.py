from distutils.core import setup
setup(
    author="Andrew Chapkowski, Mike Miller",
    author_email="achapkowski@esri.com, mmiller@esri.com",
    description="Python hooks for ArcGIS REST API",
    license='Apache',
    url='www.github.com/Esri/ArcREST',
    name='ArcREST',
    version='1.0.7',
    packages=['arcrest','arcrest/agol', 'arcrest/ags'],
    package_dir={'':''}
    )