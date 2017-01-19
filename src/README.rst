# ArcREST Version 3.5.x

A latest release(v3.5.8) of ArcREST can be downloaded here: https://github.com/Esri/ArcREST/releases/tag/3.5.8
* If you are using an older version(v3.0.1) of ArcRest, you can find it here: https://github.com/Esri/ArcREST/releases/tag/v3.0.1
* If you are using an older version(v2) of ArcRest, you can find it here: https://github.com/Esri/ArcREST/tree/FinalV2
* If you are using an older version(v1) of ArcRest, you can find it here: https://github.com/Esri/ArcREST/tree/October2014v1.0Final

A set of python tools to assist working with ArcGIS REST API for ArcGIS Server (AGS), ArcGIS Online (AGOL), and ArcGIS WebMap JSON.

This is not a full implementation of the Esri REST API, but we would like to make it, so help out!  Please feel free to contribute.

## Features

* Add, Delete, Update and Query Feature Services
* Upload attachments to feature services
* Assists in managing and publishing content
* Allows users to control, migrate and update online content
* Manage users on Portal, ArcGIS Server, and ArcGIS Online sites
* Plus additional information not even listed here!

## Documentation
 The API reference is [hosted here](http://esri.github.io/ArcREST/index.html).
 The Esri portal API reference is [hosted here](http://resources.arcgis.com/en/help/arcgis-rest-api)

### General Help

[New to Github? Get started here.](http://htmlpreview.github.com/?https://github.com/Esri/esri.github.com/blob/master/help/esri-getting-to-know-github.html)

## Requirements

* Python 2.7.x/Python 3.4 (https://www.python.org/)
* numpy >= 1.7.1 (numpy is included with ArcGIS default installation)
* ~~Six (https://pypi.python.org/pypi/six)~~ (Six is included in current version)
* pip (https://pip.pypa.io/en/stable/installing/)

## Recommended Installation

* ArcPy (optional)
* ArcGIS Desktop 10.2, 10.3, 10.4, 10.5 (optional)
  - If ArcPy is not installed, there will be limited functionality.

## Installation

### Download from PyPi using pip

```pip install arcrest_package```

### Download a geoprocessing package to install ArcREST!
        Download the GeoProcessing Package here: https://github.com/Esri/ArcREST/blob/master/ArcGIS%20Desktop%20Installer/installing_arcrest.gpk
        * Note: ArcMap/Catalog/Pro is required to use the gpk format.
        * Note: this tools can be used to update ArcREST as well
    1. Open the GPK in the ArcGIS Desktop Product of your choosing.
        2. Run the tool by double clicking on the tool icon.
        3. Test the import

* Note:  If you have not done so, you may need to add your python install path and scripts folder to your environment variables.  In your system PATH environment variable, add both the path to Python and the Python Scripts folder. ex: C:\Python27\ArcGIS10.3;C:\Python27\ArcGIS10.3\Scripts

1. Install requirements
2. run the setup.py.  This should copy it to your python's site-package folder.

```bash
pip install -r requirements.txt
python setup.py install
```

## Getting Started

Fetch your folders:

```python
import arcrest
from arcresthelper import securityhandlerhelper

config = {'username': 'myusername', 'password': 'myp4ssword'}
token = securityhandlerhelper.securityhandlerhelper(config)
admin = arcrest.manageorg.Administration(securityHandler=token.securityhandler)
content = admin.content
userInfo = content.users.user()
userInfo.folders
```

Get item metadata:

```python
item = admin.content.getItem(itemId=itemId)
item.title
 u'Streets'
```

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## PyPi

Please see our [PyPi page](https://pypi.python.org/pypi/ArcREST_Package).

To build the wheel - python setup_wheel.py bdist_wheel

## Licensing

Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's
[LICENSE](LICENSE) file.

[](Esri Tags: AGS AGOL ArcGIS Server ArcGIS Online Utilities Telecommunications ArcGISSolutions)
[](Esri Language: Python)

