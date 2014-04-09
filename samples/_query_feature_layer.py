
"""
   Querying a feature layer can be done in two
   different ways.  You can obtains the feature
   layer object from the featureservice or the
   object can be created directly.

"""
from arcrest.agol import featureservice, layer

if __name__ == "__main__":

    # WAY 1 - from featureserver
    url = "http://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Urban_Areas/FeatureServer"
    fs = featureservice.FeatureService(url=url)
    for l in fs.layers:
        print l.query(returnCountOnly=True)

    # WAY 2 - connect directly to feature layer
    fURL = "http://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Urban_Areas/FeatureServer/0"
    fl = layer.FeatureLayer(url=fURL)
    print fl.query(where="FID < 10", returnCountOnly=True)