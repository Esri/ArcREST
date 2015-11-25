"""
   This sample shows how to add a Web Map
   AGOL using ArcREST
   version 3.5.x
   Python 2/3
"""
from __future__ import print_function
import arcrest
import json
if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    portalId = "<portal Id>"
    url = "<portal or AGOL url>"
    thumbnail_url = "<url to thumbnail>"
    webmap_json_as_dict = {
    "operationalLayers":[
        {"id":"a",
         "type":"CSV",
         "layerType":"CSV",
         "title":"eqs",
         "visibility":True,
         "opacity":1,
         "url":"http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.csv",
         "layerDefinition":{"drawingInfo":{"renderer":{"description":"",
                                                       "symbol":{
                                                           "style":"esriSMSCircle",
                                                           "angle":0,
                                                           "color":[255,0,0,0],
                                                           "yoffset":0,
                                                           "type":"esriSMS",
                                                           "xoffset":0,
                                                           "size":8
                                                           },
                                                       "rotationExpression":"",
                                                       "label":"test",
                                                       "rotationType":"geographic",
                                                       "type":"simple"},
                                           "fixedSymbols":False},
                            "name":"csv",
                            "hasAttachments":False,
                            "definitionExpression":"",
                            "maxScale":0,
                            "objectIdField":"__OBJECTID",
                            "minScale":0,
                            "type":"Feature Layer",
                            "extent":""},
         "locationInfo":{
             "locationType":"coordinates",
             "latitudeFieldName":"latitude",
             "longitudeFieldName":"longitude"
             },
         "columnDelimiter":","},
        {"id":"csv_8583",
         "type":"CSV",
         "layerType":"CSV",
         "title":"all_hour",
         "visibility":True,
         "opacity":1,
         "url":"http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv",
         "layerDefinition":{
             "geometryType":"esriGeometryPoint",
             "objectIdField":"__OBJECTID",
             "type":"Feature Layer",
             "typeIdField":"",
             "drawingInfo":{
                 "renderer":{
                     "type":"simple",
                     "symbol":{
                         "type":"esriPMS",
                         "url":"http://static.arcgis.com/images/Symbols/Basic/RedSphere.png",
                         "imageData":"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",
                         "contentType":"image/png",
                         "width":15,"height":15}},
                 "fixedSymbols":True},
             "fields":[{
                 "name":"__OBJECTID",
                 "alias":"__OBJECTID",
                 "type":"esriFieldTypeOID",
                 "editable":False,
                 "Noneable":False,
                 "domain":None},
                       {"name":"time","alias":"time","type":"esriFieldTypeDate","length":36,"editable":True,"Noneable":True,"domain":None},{"name":"latitude","alias":"latitude","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"longitude","alias":"longitude","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"depth","alias":"depth","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"mag","alias":"mag","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"magType","alias":"magType","type":"esriFieldTypeString","length":255,"editable":True,"Noneable":True,"domain":None},{"name":"nst","alias":"nst","type":"esriFieldTypeInteger","editable":True,"Noneable":True,"domain":None},{"name":"gap","alias":"gap","type":"esriFieldTypeInteger","editable":True,"Noneable":True,"domain":None},{"name":"dmin","alias":"dmin","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"rms","alias":"rms","type":"esriFieldTypeDouble","editable":True,"Noneable":True,"domain":None},{"name":"net","alias":"net","type":"esriFieldTypeString","length":255,"editable":True,"Noneable":True,"domain":None},{"name":"id","alias":"id","type":"esriFieldTypeString","length":255,"editable":True,"Noneable":True,"domain":None},{"name":"updated","alias":"updated","type":"esriFieldTypeDate","length":36,"editable":True,"Noneable":True,"domain":None},{"name":"place","alias":"place","type":"esriFieldTypeString","length":255,"editable":True,"Noneable":True,"domain":None},{"name":"type","alias":"type","type":"esriFieldTypeString","length":255,"editable":True,"Noneable":True,"domain":None}],"types":[],"capabilities":"Query","name":"csv","extent":{"type":"extent","xmin":-16209420.29764264,"ymin":3785953.3038973636,"xmax":-10823505.034137173,"ymax":8414179.048043747,"spatialReference":{"wkid":102100}}},"popupInfo":{"title":"","fieldInfos":[{"fieldName":"__OBJECTID","label":"__OBJECTID","isEditable":False,"tooltip":"","visible":False,"format":None,"stringFieldOption":"textbox"},{"fieldName":"time","label":"time","isEditable":True,"tooltip":"","visible":True,"format":{"dateFormat":"longMonthDayYear"},"stringFieldOption":"textbox"},{"fieldName":"latitude","label":"latitude","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"longitude","label":"longitude","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"depth","label":"depth","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"mag","label":"mag","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"magType","label":"magType","isEditable":True,"tooltip":"","visible":True,"format":None,"stringFieldOption":"textbox"},{"fieldName":"nst","label":"nst","isEditable":True,"tooltip":"","visible":True,"format":{"places":0,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"gap","label":"gap","isEditable":True,"tooltip":"","visible":True,"format":{"places":0,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"dmin","label":"dmin","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"rms","label":"rms","isEditable":True,"tooltip":"","visible":True,"format":{"places":2,"digitSeparator":True},"stringFieldOption":"textbox"},{"fieldName":"net","label":"net","isEditable":True,"tooltip":"","visible":True,"format":None,"stringFieldOption":"textbox"},{"fieldName":"id","label":"id","isEditable":True,"tooltip":"","visible":True,"format":None,"stringFieldOption":"textbox"},{"fieldName":"updated","label":"updated","isEditable":True,"tooltip":"","visible":True,"format":{"dateFormat":"longMonthDayYear"},"stringFieldOption":"textbox"},{"fieldName":"place","label":"place","isEditable":True,"tooltip":"","visible":True,"format":None,"stringFieldOption":"textbox"},{"fieldName":"type","label":"type","isEditable":True,"tooltip":"","visible":True,"format":None,"stringFieldOption":"textbox"}],"description":None,"showAttachments":False,"mediaInfos":[]},"locationInfo":{"locationType":"coordinates","latitudeFieldName":"latitude","longitudeFieldName":"longitude"},"columnDelimiter":","}],"baseMap":{"baseMapLayers":[{"id":"defaultBasemap","layerType":"ArcGISTiledMapServiceLayer","opacity":1,"visibility":True,
"url":"http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer"}],
"title":"Topographic"},
    "spatialReference":{"wkid":102100,"latestWkid":3857},"version":"2.0"}
    securityHandler = arcrest.AGOLTokenSecurityHandler(username,
                                                       password)
    #   Create the administration connection
    #
    admin = arcrest.manageorg.Administration(url, securityHandler)
    #   Access the content properties to add the item
    #
    content = admin.content
    #   Get the user
    #
    user = content.users.user()
    #   Provide the item parameters
    #
    itemParams = arcrest.manageorg.ItemParameter()
    itemParams.title = "MY FIRST WEB MAP"
    itemParams.thumbnailurl = "http://its.ucsc.edu/software/images/arcgis.jpg"
    itemParams.type = "Web Map"
    itemParams.tags = "Map, Earthquake"
    itemParams.extent = "-180,-80.1787,180, 80.1787"

    #   Add the Web Map
    #
    print user.addItem(itemParameters=itemParams,
                              overwrite=True,
                              text=json.dumps(map_json))
