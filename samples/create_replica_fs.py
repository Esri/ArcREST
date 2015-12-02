"""
  This sample shows how to create a replica from a FS

  ArcREST version 3.5.x
  Python 2/3

"""
from __future__ import print_function
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
    result = fs.createReplica(replicaName='Demo',
                              layers=[0,1,2,3],
                              dataFormat="filegdb",
                              out_path='C:\\temp')

    print( result)