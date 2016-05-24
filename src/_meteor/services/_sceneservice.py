from __future__ import absolute_import
from __future__ import print_function
from ..common._base import BaseService

########################################################################
class SceneService(BaseService):
    """
    A scene service is an ArcGIS Server web service originating from a 3D
    scene in ArcGIS Pro. Scene services (also known as web scene layers)
    allow you to share 3D content via web scenes to your Portal for ArcGIS
    organization. Web scenes are similar in concept to web maps. However,
    instead of displaying 2D map or feature services, they use 3D scene
    services and give you access to 3D content originally created in ArcGIS
    Pro.
    """
    _url = None
    _con = None
    _json_dict = None
