from arcresthelper import securityhandlerhelper
from arcrest.agol import FeatureService
from arcrest.common.filters import LayerDefinitionFilter

if __name__ == "__main__":
    url = ''
    proxy_port = None
    proxy_url = None    

    securityInfo = {}
    securityInfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityInfo['username'] = ""
    securityInfo['password'] = ""
    securityInfo['org_url'] = "http://www.arcgis.com"
    securityInfo['proxy_url'] = proxy_url
    securityInfo['proxy_port'] = proxy_port
    securityInfo['referer_url'] = None
    securityInfo['token_url'] = None
    securityInfo['certificatefile'] = None
    securityInfo['keyfile'] = None
    securityInfo['client_id'] = None
    securityInfo['secret_id'] = None   
   
    shh = securityhandlerhelper.securityhandlerhelper(securityInfo)
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