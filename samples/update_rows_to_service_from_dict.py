
"""
   This sample shows how update a row based on its objectID

   Python 2.x
   ArcREST 3.0.1
"""

from arcresthelper import securityhandlerhelper

from arcrest.common.general import Feature

if __name__ == "__main__":
    url = ''# URL to Service
    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = "" #User Name
    securityinfo['password'] = "" #Password
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
        fl= FeatureLayer(
            url=url,
            securityHandler=shh.securityhandler,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            initialize=True)

        features = []
        json_string={'geometry':
                        {
                            'y': 1885855.2531960313,
                            'x': 1034495.0035156211}
                        ,
                     'attributes':
                     {  'NAME': 'NameChange',
                        'OBJECTID': 1
                     }}

        features.append(Feature(json_string=json_string))


        print fl.updateFeature(features=features)