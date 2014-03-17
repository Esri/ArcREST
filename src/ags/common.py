"""
   contains all the common JSON objects as defined
   at in the common object type in the ArcGIS REST 
   API.
"""
import json
import arcpy

#class Geometry(object):
    #""" Base Geometry Class """
    #pass
#########################################################################
#class Point(Geometry):
    #""" Point Geometry 
        
    #"""
    #_x = None
    #_y = None
    #_z = None
    #_m = None
    #_wkid = None
    #_json = None
    #_geom = None
    #_dict = None
    ##----------------------------------------------------------------------
    #def __init__(self, x, y, wkid, z=None, m=None):
        #"""Constructor"""
        #self._x = float(x)
        #self._y = float(y)
        #self._wkid = wkid
        #if not z is None:
            #self._z = float(z)
        #self._m = m
        #self._dict = self.asDictionary
        #self._json = self.asJSON
        #self._geom = self.asArcPyObject
    ##----------------------------------------------------------------------
    #@property
    #def asJSON(self):
        #""" returns a geometry as JSON """
        #value = self._json
        #if value is None:
            #value = json.dumps(self.asDictionary)
            #self._json = value
        #return self._json
    ##----------------------------------------------------------------------
    #@property
    #def asArcPyObject(self):
        #""" returns the Point as an ESRI arcpy.Point object """
        #return arcpy.AsShape(self.asDictionary, True)
    ##----------------------------------------------------------------------
    #@property
    #def asDictionary(self):
        #""" returns the object as a python dictionary """
        ##
        #value = self._dict
        #if value is None:
            #template = {"x" : self._x, 
                        #"y" : self._y, 
                        #"spatialReference" : {"wkid" : self._wkid}
                        #}
            #if not self._z is None:
                #template['z'] = self._z
            #if not self._m is None:
                #template['z'] = self._m
            #self._dict = template
        #return self._dict
    ##----------------------------------------------------------------------
    #@property
    #def asList(self):
        #""" returns a Point value as a list of [x,y,<z>,<m>] """
        #base = [self._x, self._y]
        #if not self._z is None:
            #base.append(self._z)
        #elif not self._m is None:
            #base.append(self._m)
        #return base

#########################################################################
#class MultiPoint(Geometry):
    #""" Implements the ArcGIS JSON MultiPoint Geometry Object """
    #_geom = None
    #_json = None
    #_dict = None
    #_wkid = None
    #_points = None
    #_hasZ = False
    #_hasM = False
    ##----------------------------------------------------------------------
    #def __init__(self, points, wkid, hasZ=False, hasM=False):
        #"""Constructor"""
        #self._points = points
        #self._wkid = wkid
        #self._hasZ = hasZ
        #self._hasM = hasM
        #self.asDictionary
        #self.asJSON
        #self.asArcPyObject
    ##----------------------------------------------------------------------
    #@property
    #def asJSON(self):
        #""" returns a geometry as JSON """
        #value = self._json
        #if value is None:
            #value = json.dumps(self.asDictionary)
            #self._json = value
        #return self._json
    ##----------------------------------------------------------------------
    #@property
    #def asArcPyObject(self):
        #""" returns the Point as an ESRI arcpy.MultiPoint object """
        #return arcpy.AsShape(self.asDictionary, True)
    ##----------------------------------------------------------------------
    #@property
    #def asDictionary(self):
        #""" returns the object as a python dictionary """
        ##
        #value = self._dict
        #if value is None:
            #template = {
                #"hasM" : self._hasM,
                #"hasZ" : self._hasZ,
                #"points" : [], 
                #"spatialReference" : {"wkid" : self._wkid}
            #}
            #for pt in self._points:
                #template['points'].append(pt.asList)
            #self._dict = template
        #return self._dict  
#########################################################################
#class Polyline(Geometry):
    #""" Implements the ArcGIS REST API Polyline Object 
        #Inputs:
           #paths - list - list of lists of Point objects
           #wkid - integer - well know spatial reference id
           #hasZ - boolean - 
           #hasM - boolean - 
    #"""
    #_paths = None
    #_wkid = None
    #_json = None
    #_dict = None
    #_geom = None
    #_hasZ = None
    #_hasM = None
    ##----------------------------------------------------------------------
    #def __init__(self, paths, wkid, hasZ=False, hasM=False):
        #"""Constructor"""
        #self._paths = paths
        #self._wkid = wkid
        #self._hasM = hasM
        #self._hasZ = hasZ
        #self.asDictionary
        #self.asArcPyObject
        #self.asJSON
    ##----------------------------------------------------------------------
    #@property
    #def asJSON(self):
        #""" returns a geometry as JSON """
        #value = self._json
        #if value is None:
            #value = json.dumps(self.asDictionary)
            #self._json = value
        #return self._json
    ##----------------------------------------------------------------------
    #@property
    #def asArcPyObject(self):
        #""" returns the Polyline as an ESRI arcpy.Polyline object """
        #return arcpy.AsShape(self.asDictionary, True)
    ##----------------------------------------------------------------------
    #@property
    #def asDictionary(self):
        #""" returns the object as a python dictionary """
        #value = self._dict
        #if value is None:
            #template = {
                #"hasM" : self._hasM,
                #"hasZ" : self._hasZ,
                #"paths" : [], 
                #"spatialReference" : {"wkid" : self._wkid}
            #}
            #for part in self._paths:
                #lpart = []
                #for pt in part:
                    #lpart.append(pt.asList)
                #template['paths'].append(lpart)
                #del lpart
            #self._dict = template
        #return self._dict        
#########################################################################
#class Polygon(Geometry):
    #""" Implements the ArcGIS REST JSON for Polygon Object """
    #_rings = None
    #_wkid = None
    #_json = None
    #_dict = None
    #_geom = None
    #_hasZ = None
    #_hasM = None    
    ##----------------------------------------------------------------------
    #def __init__(self, rings, wkid, hasZ=False, hasM=False):
        #"""Constructor"""
        #self._rings = rings
        #self._wkid = wkid
        #self._hasM = hasM
        #self._hasZ = hasZ
        #self.asDictionary
        #self.asArcPyObject
        #self.asJSON        
    ##----------------------------------------------------------------------
    #@property
    #def asJSON(self):
        #""" returns a geometry as JSON """
        #value = self._json
        #if value is None:
            #value = json.dumps(self.asDictionary)
            #self._json = value
        #return self._json
    ##----------------------------------------------------------------------
    #@property
    #def asArcPyObject(self):
        #""" returns the Polyline as an ESRI arcpy.Polyline object """
        #return arcpy.AsShape(self.asDictionary, True)
    ##----------------------------------------------------------------------
    #@property
    #def asDictionary(self):
        #""" returns the object as a python dictionary """
        #value = self._dict
        #if value is None:
            #template = {
                #"hasM" : self._hasM,
                #"hasZ" : self._hasZ,
                #"rings" : [], 
                #"spatialReference" : {"wkid" : self._wkid}
            #}
            #for part in self._rings:
                #lpart = []
                #for pt in part:
                    #lpart.append(pt.asList)
                #template['rings'].append(lpart)
                #del lpart
            #self._dict = template
        #return self._dict            
########################################################################
class Feature(object):
    """ returns a feature  """
    _geom = None
    _json = None
    _dict = None
    _geom = None
    _geomType = None
    _attributes = None
    #----------------------------------------------------------------------
    def __init__(self, json_string):
        """Constructor"""
        if type(json_string) is dict:
            self._json = json.dumps(json_string)
            self._dict = json_string
        elif type(json_string) is str:
            self._dict = json.loads(json_string)
            self._json = json_string
        else:
            raise TypeError("Invalid Input, only dictionary of string allowed")
    #----------------------------------------------------------------------
    @property
    def asRow(self):
        """ converts a feature to a list for insertion into an insert cursor 
            Output:
               [row items], [field names]
               returns a list of fields and the row object
        """
        fields = self.fields
        row = [""] * len(fields)
        for k,v in self._attributes.iteritems():
            row[fields.index(k)] = v
            del v
            del k
        row.append(self.geometry)
        fields.append("SHAPE@")
        return row, fields
    #----------------------------------------------------------------------
    @property
    def geometry(self):
        """returns the feature geometry"""
        if self._geom is None:
            if self._dict.has_key('feature'):
                self._geom = arcpy.AsShape(self._dict['feature']['geometry'], esri_json=True)
            else:
                self._geom = arcpy.AsShape(self._dict['geometry'], esri_json=True)
        return self._geom
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns a list of feature fields """
        if self._dict.has_key("feature"):
            self._attributes = self._dict['feature']['attributes']
        else:
            self._attributes = self._dict['attributes']
        return self._attributes.keys()
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the feature's geometry type """
        if self._geomType is None:
            self._geomType = self.geometry.type
        return self._geomType


#if __name__ == "__main__":
    #dml = DynamicMapLayer(mapLayerId=0)
    #print dml.asDictionary
    #print dml.asJSON
    #tds = TableDataSource(workspaceId="myid", dataSourceName="")
    #print  isinstance(tds, DataSource)#tds is DataSource
    #print tds.asDictionary
    #print tds.asJSON
    #rds = RasterDataSource(workspaceId="rasID", dataSourceName="neworlean.tif")
    #print rds.asDictionary
    #print rds.asJSON
    #value = {
  #"geometry" : {"x" : -118.15, "y" : 33.80},

  #"attributes" : {
    #"OWNER" : "Joe Smith",
    #"VALUE" : 94820.37,
    #"APPROVED" : True,
    #"LASTUPDATE" : 1227663551096
  #}
#}
    #f = Feature(json.dumps(value))
    #print f.asRow
    #print f.fields
    #print f.geometry
    #print f.geometryType
    
    #pt = Point(x=1, y=2, wkid=4326)
    #pt2 = Point(x=3, y=4, wkid=4326)
    #print pt.asDictionary
    #print pt.asJSON
    #pt_obj = pt.asArcPyObject
    #print pt_obj.centroid.X, pt_obj.centroid.Y
    #mp = MultiPoint(points=[pt, pt2], wkid=4326)
    #print mp.asJSON
    #print mp.asDictionary
    #print mp.asArcPyObject
    #path = [
        #[Point(-97.06138,32.837, 4326),Point(-97.06133,32.836, 4326)], 
        #[Point(-97.06326,32.759, 4326),Point(-97.06298,32.755, 4326)]
    #]
    #line = Polyline(paths=path, wkid=4326)
    #print line.asJSON
    #print line.asDictionary
    #arcpy.env.overwriteOutput = True
    ##arcpy.CopyFeatures_management(line.asArcPyObject, r"c:\temp\line.shp")
    #rings =  [
        #[Point(0,0,4326, z=35.1),Point(0,1,4326, z=35.2),Point(.5,.5,4326, z=35.3),Point(1,1,4326, z= 35.2),
         #Point(1,0,4326, z=35.1)]
        #]
    #poly = Polygon(rings, wkid=4326, hasZ=True)
    #print poly.asDictionary
    #print poly.asJSON
    ##arcpy.CopyFeatures_management(poly.asArcPyObject, r"c:\temp\polygon.shp")