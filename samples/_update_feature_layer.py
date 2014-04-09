
"""
   Updating a feature layer, OBJECTID must
   be included in the features.

"""
from arcrest.agol import featureservice, layer

if __name__ == "__main__":

    fURL = "http://services2.arcgis.com/PWJUSsdoJDp7SgLj/arcgis/rest/services/PublicOutages/FeatureServer/1"
    fl = layer.FeatureLayer(url=fURL,username='',password='')
    result = fl.query(where="1=1",out_fields='OBJECTID,NUMSERVED,NUMOUT',returnGeometry=False)
    for res in result:
        res.set_value("NUMSERVED", 99)
        res.set_value("NUMOUT", 100)

    print fl.updateFeature(result)

