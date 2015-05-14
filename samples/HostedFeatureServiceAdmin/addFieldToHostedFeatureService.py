"""
   Adds a field to any layer matching the name in all feature services without
   republishing
"""
import arcrest

if __name__ == "__main__":
    url = "https://<url to spatial data store>/ArcGIS/rest/admin"
    username = "<user name>"
    password = "<password> "
    featureLayerNames = ["layerName1","layerName2"]
    fieldToAdd = {

        "fields" : [
            {
                "name" : "CommonField3",
                "type" : "esriFieldTypeString",
                "alias" : "Common Field 2",
                "sqlType" : "sqlTypeOther", "length" : 50,
                "nullable" : True,
                "editable" : True,
                "domain" : None,
                "defaultValue" : None
            }  ]
    }
    sh = arcrest.AGOLTokenSecurityHandler(username, password)
    agolServices = arcrest.hostedservice.Services(url, securityHandler=sh)
    for service in agolServices.services:
        if not service.layers is None:
            print service.url
            for lyr in service.layers:
                print lyr.name    
                
                if lyr.name.lower() in featureLayerNames:
                    print lyr.addToDefinition(fieldToAdd)                    
                    #  Output: {'success': True}