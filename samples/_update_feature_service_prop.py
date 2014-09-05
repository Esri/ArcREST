
"""
   Updating a feature layer, OBJECTID must
   be included in the features.

"""
import json

from arcrest.agol import admin

if __name__ == "__main__":
    try:
        fURL = "http://services2.arcgis.com/PWJUSsdoJDp7SgLj/arcgis/rest/admin/services/HighWaterConsumption/FeatureServer"
        aF = admin.AdminFeatureServiceLayer(url=fURL,username='',password='',initialize=True)
        result = aF.capabilities
        if result  == "Query": 
            result = 'Create,Delete,Query,Update,Editing,Sync'
        else:
            result = 'Query'
            
        res = aF.updateDefinition(json_dict={"capabilities": result})
        
        print res 
    except ValueError, e:
        print e


