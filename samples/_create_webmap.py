"""
    create a webmap from code, 
    add a dynamic layer, with dynamiclayer option for changing the symbols

"""


import arcrest
import arcrest.webmap
import arcrest.agol
import json

USER = "XXXXX"
PASSWORD = "xxxxxx"
ORGANISATION = "xxxxxx"

wm = arcrest.webmap.layers.AGSMapServiceLayer("http://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer", "", "Service Census")

wm.add_layer({ "id":0, "minScale":0,"maxScale":0, "layerDefinition": { "source": { "type":"mapLayer", "mapLayerId":3}, "drawingInfo":{"renderer":{"type":"simple","symbol":{"color":[0,0,0,128],"outline":{"color":[0,0,0,255],"width":1.5,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}}},"name":"Geology (Stratigraphy)","parentLayerId":-1,"defaultVisibility":True}})


topomap = arcrest.webmap.layers.BaseMapLayer("defaultBaseMap", url="http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer")

bm = arcrest.webmap.webmapobjects.BaseMap("Topographic", [topomap])

w = arcrest.webmap.webmap.WebMap(baseMap = bm, 
           operationalLayers = [ wm ])


pa = arcrest.agol.admin.AGOL(USER, PASSWORD, ORGANISATION)

pa.addItem("MyNew WebMap","montag", "description de la webmap", "snippet", json.loads(str(w)),None)




