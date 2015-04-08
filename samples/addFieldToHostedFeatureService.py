"""
   Adds a field to an existing hosted feature service without
   republishing
"""
import arcrest

if __name__ == "__main__":
    url = "https://<url to spatial data store>/ArcGIS/rest/admin"
    username = "<user name>"
    password = "<password>"
    featureLayerName = "<feature layer name>"
    fieldToAdd = {

        "fields" : [
            {
                "name" : "FUNWITHREST",
                "type" : "esriFieldTypeString",
                "alias" : "FUNFUN",
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
        for lyr in service.layers:
            if lyr.name.lower() == featureLayerName.lower():
                print lyr.addToDefinition(fieldToAdd)
                break
#  Output: {'success': True}