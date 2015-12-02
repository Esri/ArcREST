"""
   GeoJSON example using addItem

   Python 2/3
   ArcREST version 3.5.0
"""
from __future__ import print_function
import arcrest

if __name__ == "__main__":
    username = ""
    password = ""
    geojsonFile = r""
    sh = arcrest.AGOLTokenSecurityHandler(username, password)
    admin = arcrest.manageorg.Administration(securityHandler=sh)
    user = admin.content.users.user()
    ip = arcrest.manageorg.ItemParameter()
    ip.title = "MyGeoJSONTestFile"
    ip.type = "GeoJson"
    ip.tags = "Geo1,Geo2"
    ip.description = "Publishing a geojson file"
    addedItem = user.addItem(itemParameters=ip, filePath=geojsonFile)
    itemId = addedItem.id
    pp = arcrest.manageorg.PublishGeoJSONParameter()
    pp.name = "Geojsonrocks"
    pp.hasStaticData = True
    print( user.publishItem(fileType="geojson", publishParameters=pp, itemId=itemId, wait=True))