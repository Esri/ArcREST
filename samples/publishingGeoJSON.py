"""
   GeoJSON example using addItem

   Python 2/3
   ArcREST version 3.5.0
"""
from __future__ import print_function
import arcrest

sh = arcrest.AGOLTokenSecurityHandler("user", "password")
admin = arcrest.manageorg.Administration(securityHandler=sh)
user = admin.content.users.user()
ip = arcrest.manageorg.ItemParameter()
ip.title = "MyGeoJSONTestFile"
ip.type = "GeoJson"
ip.tags = "Geo1,Geo2"
ip.description = "Publishing a geojson file"
addedItem = user.addItem(itemParameters=ip, filePath=r"c:\temp3\states2.geojson")
itemId = addedItem['id']
pp = arcrest.manageorg.PublishGeoJSONParameter()
pp.name = "Geojsonrocks"
pp.hasStaticData = True
print( user.publishItem(fileType="geojson", publishParameters=pp, itemId=itemId))