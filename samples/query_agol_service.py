"""
   Query agol service
   Python 2.x
   ArcREST 3.0.1
"""
from arcresthelper import securityhandlerhelper
from arcrest.agol import FeatureService
from arcrest.common.filters import LayerDefinitionFilter

if __name__ == "__main__":
    url = ''
    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfo['username'] = ""
    securityinfo['password'] = ""
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    shh = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
    if shh.valid == False:
        print shh.message
    else:
        fs = FeatureService(
            url=url,
            securityHandler=shh.securityhandler,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            initialize=True)
        ldf = LayerDefinitionFilter()
        ldf.addFilter(0, where="1=1")
        print fs.query(layerDefsFilter=ldf,
                       returnCountOnly=True)
        # should see something like : {'layers': [{'count': 4, 'id': 0}]}