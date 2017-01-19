ArcREST Version 3.5.x
=====================

A latest release(v3.5.9) of ArcREST can be downloaded here:
https://github.com/Esri/ArcREST/releases/tag/3.5.9 \* If you are using
an older version(v3.0.1) of ArcRest, you can find it here:
https://github.com/Esri/ArcREST/releases/tag/v3.0.1 \* If you are using
an older version(v2) of ArcRest, you can find it here:
https://github.com/Esri/ArcREST/tree/FinalV2 \* If you are using an
older version(v1) of ArcRest, you can find it here:
https://github.com/Esri/ArcREST/tree/October2014v1.0Final

A set of python tools to assist working with ArcGIS REST API for ArcGIS
Server (AGS), ArcGIS Online (AGOL), and ArcGIS WebMap JSON.

This is not a full implementation of the Esri REST API, but we would
like to make it, so help out! Please feel free to contribute.

Features
--------

-  Add, Delete, Update and Query Feature Services
-  Upload attachments to feature services
-  Assists in managing and publishing content
-  Allows users to control, migrate and update online content
-  Manage users on Portal, ArcGIS Server, and ArcGIS Online sites
-  Plus additional information not even listed here!

Requirements
------------

-  Python 2.7.x/Python 3.4 (https://www.python.org/)
-  numpy >= 1.7.1 (numpy is included with ArcGIS default installation)
-  [STRIKEOUT:Six (https://pypi.python.org/pypi/six)] (Six is included
   in current version)
-  pip (https://pip.pypa.io/en/stable/installing/)

Getting Started
---------------

Fetch your folders:

.. code:: python

    import arcrest
    from arcresthelper import securityhandlerhelper

    config = {'username': 'myusername', 'password': 'myp4ssword'}
    token = securityhandlerhelper.securityhandlerhelper(config)
    admin = arcrest.manageorg.Administration(securityHandler=token.securityhandler)
    content = admin.content
    userInfo = content.users.user()
    userInfo.folders

Get item metadata:

.. code:: python

    item = admin.content.getItem(itemId=itemId)
    item.title
     u'Streets'

Issues
------

Find a bug or want to request a new feature? Please let us know by
submitting an issue.

Contributing
------------

Esri welcomes contributions from anyone and everyone. Please see our
`guidelines for contributing <https://github.com/esri/contributing>`__.


Licensing
---------

Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
