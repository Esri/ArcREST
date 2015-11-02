"""
    Adds a domain to the specified field in any layer matching the name in all feature services
    without republishing
"""
import arcrest

if __name__ == "__main__":
    url = "https://<url to spatial data store>/ArcGIS/rest/admin"
    username = "<user name>"
    password = "<password>"
    featureLayerNames = ["layername"] # must be all lowercase
    definition = {
        "fields": [
            {
                "name": "Type",
                "domain": {
                    "type": "codedValue",
                    "name": "Type",
                    "codedValues": [
                        {
                            "name": "Option A",
                            "code": "type_a"
                        },
                        {
                            "name": "Option B",
                            "code": "type_b"
                        },
                        {
                            "name": "Option C",
                            "code": "type_c"
                        }
                    ]
                }
            }
        ]
    }

    sh = arcrest.AGOLTokenSecurityHandler(username, password)
    agolServices = arcrest.hostedservice.Services(url, securityHandler=sh)
    for service in agolServices.services:
        if not service.layers is None:
            print service.url
            for lyr in service.layers:
                print lyr.name    
                
                if lyr.name.lower() in featureLayerNames:
                    print lyr.updateDefinition(definition)
                    #  Output: {'success': True}