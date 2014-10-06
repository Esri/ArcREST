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
    ldf = LayerDefinitionFilter()
    ldf.addFilter(0, where="1=1")
    print fs.query(layerDefsFilter=ldf,
                   returnCountOnly=True)
    # should see something like : {'layers': [{'count': 4, 'id': 0}]}