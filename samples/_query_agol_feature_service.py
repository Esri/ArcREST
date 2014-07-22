"""
   Queries a feature service and returns the feature count
"""
from arcrest.agol import featureservice, filters

if __name__ == "__main__":
    try:
        url = "http://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Urban_Areas/FeatureServer"
        fs = featureservice.FeatureService(url=url)
        lds = filters.LayerDefinitionFilter()
        lds.addFilter(layer_id=0, where="FID <= 100")
        print fs.query(layerDefsFilter=lds, returnCountOnly=True)
    except ValueError, e:
        print e
