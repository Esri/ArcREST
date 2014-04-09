from distutils.core import setup
setup(
    author="Andrew Chapkowski",
    author_email="achapkowski@esri.com",
    description="Python hooks for ArcGIS REST API",
    license='Apache',
    url='www.esri.com',
    name='ArcREST',
    version='1.0.5b',
    packages=['arcrest','arcrest/agol', 'arcrest/ags'],
    package_dir={'':''}
    )