
"""
   This sample shows how to add a field to a set of layers
   from their rest services url

"""
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureLayer

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    urls = ["url to layer","url to layer"]
    proxy_port = None
    proxy_url = None
    
    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)
    
    for url in urls:
        fl = FeatureLayer(
            url=url,
            securityHandler=agolSH,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            initialize=True)
        adminFl = fl.administration
        fieldToAdd = {
    
            "fields" : [
                {
                    "name" : "CommonField2",
                    "type" : "esriFieldTypeString",
                    "alias" : "Common Field 2",
                    "sqlType" : "sqlTypeOther", "length" : 50,
                    "nullable" : True,
                    "editable" : True,
                    "domain" : None,
                    "defaultValue" : None
                }  ]
        }
        print adminFl.addToDefinition(fieldToAdd)
  