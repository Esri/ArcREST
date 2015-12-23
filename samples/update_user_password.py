"""
   Update a users passwords

   Python 2.x
   ArcREST 3.0.1
"""
from arcresthelper import securityhandlerhelper
import arcrest

if __name__ == "__main__":

    username = ''# Username

    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = "" #User Name
    securityinfo['password'] = "" #password
    securityinfo['org_url'] = "https://www.arcgis.com"
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
        admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler, initialize=True)
        user = admin.community.users.user(str(username).strip())
        print user.update(password="1234testtest")
