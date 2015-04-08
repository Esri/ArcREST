"""
  This sample shows how to create a replica from a FS

"""
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureService
from arcrest.common.filters import LayerDefinitionFilter

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    url = "<Feature Service URL on AGOL>"
    proxy_port = None
    proxy_url = None
    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)
    fs = FeatureService(
        url=url,
        securityHandler=agolSH,
        proxy_port=proxy_port,
        proxy_url=proxy_url,
        initialize=True)
    result = fs.createReplica(replicaName='Demo', layers='0,1,2,3,4', keep_replica=False, 
                              layerQueries=None, 
                              geometryFilter=None, 
                              returnAttachments=True, 
                              returnAttachmentDatabyURL=False, 
                              returnAsFeatureClass=True, 
                              out_path='C:\\temp')

    print result
    # should see something like : {'layers': [{'count': 4, 'id': 0}]}