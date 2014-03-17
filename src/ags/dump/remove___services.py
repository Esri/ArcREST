"""
   This module contains classes and functions to work with
   ArcGIS Server Services.
"""
from base import BaseAGSService  


    
        
        

        
if __name__ == "__main__":
    #url = "http://sampleserver5.arcgisonline.com/arcgis/rest/services/Census/MapServer"
    url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/CommercialDamageAssessment/FeatureServer"#"http://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/0"#/dynamicLayer/1?layer={"id":101,"source":{"type":"mapLayer","mapLayerId":3}}&f=pjson
    #ms = MapService(url=url)
    #for fs in ms.layers:
    #    print fs['featureService'].currentVersion
    fs = FeatureService(url=url)    
    attributes = [attr for attr in dir(fs) 
                  if not attr.startswith('__') or not attr.startswith('_')]    
    for a in attributes:
        if a.startswith('_'):
            pass
        else:
            print a, getattr(fs, a)
        
    
    #print ms.find(searchText="1005", layers="0,1,2,3")
    #mdl = common.DynamicMapLayer(mapLayerId=3)
    #feature = ms.getFeatureDynamicLayer(1, dynamicLayer=mdl)
    #print feature.asRow
    #print feature.fields
    #print feature.geometry
    #print feature.geometryType