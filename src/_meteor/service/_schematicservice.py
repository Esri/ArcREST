"""
"""
from __future__ import absolute_import
from ._base import BaseService


########################################################################
class SchematicsService(BaseService):
    """
    The Schematic Service resource represents a Schematics service
    published with ArcGIS Server. The resource provides information about
    the service itself (name, type) the number of published diagrams and
    published schematic layers, and the number of published diagram
    templates.
    """
    _url = None
    _con = None
    _json = None
    _json_dict = None
    _nbSchematicLayers = None
    _nbTemplates = None
    _type = None
    _name = None
    _nbEstimatedDiagrams = None
    #----------------------------------------------------------------------
    @property
    def nbSchematicLayers(self):
        if self._nbSchematicLayers is None:
            self.init()
        return self._nbSchematicLayers
    #----------------------------------------------------------------------
    @property
    def nbTemplates (self):
        if self._nbTemplates  is None:
            self.init()
        return self._nbTemplates
    #----------------------------------------------------------------------
    @property
    def type(self):
        if self._type  is None:
            self.init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def name(self):
        if self._name is None:
            self.init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def nbEstimatedDiagrams(self):
        if self._nbEstimatedDiagrams is None:
            self.init()
        return self._nbEstimatedDiagrams
    #----------------------------------------------------------------------
    @property
    def diagrams(self):
        """
        The Schematic Diagrams resource represents all the schematic diagrams
        under a schematic service. It is returned as an array of Schematic
        Diagram resource by the REST API.
        """
        params = {"f" : "json"}
        exportURL = self._url + "/diagrams"
        return self._con.get(path_or_url=exportURL,
                             params=params)
    #----------------------------------------------------------------------
    @property
    def folders(self):
        """
        The Schematic Folders resource represents the set of schematic folders
        in the schematic dataset(s) related to the schematic layers under a
        schematic service. It is returned as an array of <Schematic Folder Object>
        by the REST API.
        """
        params = {"f" : "json"}
        exportURL = self._url + "/folders"
        return self._con.get(path_or_url=exportURL,
                         params=params)
    #----------------------------------------------------------------------
    @property
    def schematicLayers(self):
        """
        The Schematic Layers resource represents all the schematic layers
        under a schematic service published by ArcGIS Server. It is returned
        as an array of Schematic Layer resources by the REST API.
        """
        params = {"f" : "json"}
        exportURL = self._url + "/schematicLayers"
        return self._con.get(path_or_url=exportURL,
                         params=params)
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """
        The Schematic Diagram Templates represents all the schematic diagram
        templates related to the published schematic layers under a schematic
        service. It is returned as an array of Schematic Diagram Template
        resources by the REST API.
        """
        params = {"f" : "json"}
        exportURL = self._url + "/templates"
        return self._con.get(path_or_url=exportURL,
                                 params=params)
    #----------------------------------------------------------------------
    def searchDiagrams(self,whereClause=None,relatedObjects=None,
                       relatedSchematicObjects=None):
        """
        The Schematic Search Diagrams operation is performed on the schematic
        service resource. The result of this operation is an array of Schematic
        Diagram Information Object.

        It is used to search diagrams in the schematic service by criteria;
        that is, diagrams filtered out via a where clause on any schematic
        diagram class table field, diagrams that contain schematic features
        associated with a specific set of GIS features/objects, or diagrams
        that contain schematic features associated with the same GIS features/
        objects related to another set of schematic features.

        Inputs:
            whereClause - A where clause for the query filter. Any legal SQL
                          where clause operating on the fields in the schematic
                          diagram class table is allowed. See the Schematic
                          diagram class table fields section below to know the
                          exact list of field names that can be used in this
                          where clause.
            relatedObjects - An array containing the list of the GIS features/
                             objects IDs per feature class/table name that are in
                             relation with schematic features in the resulting
                             queried diagrams. Each GIS feature/object ID
                             corresponds to a value of the OBJECTID field in the
                             GIS feature class/table.
            relatedSchematicObjects - An array containing the list of the
                                      schematic feature names per schematic
                                      feature class ID that have the same
                                      associated GIS features/objects with
                                      schematic features in the resulting
                                      queried diagrams. Each schematic feature
                                      name corresponds to a value of the
                                      SCHEMATICTID field in the schematic
                                      feature class.
        """
        params = {"f" : "json"}
        if whereClause:
            params["where"] = whereClause
        if relatedObjects:
            params["relatedObjects"] = relatedObjects
        if relatedSchematicObjects:
            params["relatedSchematicObjects"] = relatedSchematicObjects

        exportURL = self._url + "/searchDiagrams"
        return self._con.get(path_or_url=exportURL,
                             params=params)