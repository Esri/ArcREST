from arcresthelper import securityhandlerhelper
from arcresthelper import featureservicetools
import os

if __name__ == "__main__":

    proxy_port = None
    proxy_url = None    

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = ''
    securityinfo['password'] = ''
    securityinfo['org_url'] = "https://www.arcgis.com"

    serviceUrl = ''#URL to service, make sure to not include a layer
    shh = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
    if shh.valid == False:
        print shh.message
    else:
        fst = featureservicetools.featureservicetools(securityinfo=securityinfo)
        if fst.valid:
            print fst.EnableEditingOnService(url=serviceUrl)