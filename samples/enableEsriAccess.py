from arcresthelper import securityhandlerhelper
from arcrest.security import AGOLTokenSecurityHandler
import arcrest

if __name__ == "__main__":

    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = '' #User Name
    securityinfo['password'] = '' #password
    securityinfo['org_url'] = 'https://www.arcgis.com'
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    enableAccess = True #False disables access, True enables access
    usersToSkip = ["scottmooremsl"] #users to skip enabling or disabling.  use all lowercase usernames like "username1", comma separated in double quotes

    shh = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
    if shh.valid == False:
        print (shh.message)
    else:
        admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler, initialize=True)
        portal = admin.portals.portalSelf
        ns = 1
        while (ns > -1):
            commUsers = portal.users(start=ns, num=100)
            ns = commUsers['nextStart']
            commUsers = commUsers['users']
            for commUser in commUsers:
                if not commUser.username.lower() in usersToSkip:
                    user = admin.community.users.user(commUser.username)
                    print commUser.username + ": " + commUser.userType + " {" + commUser.provider + ")"
                    if (enableAccess == True):
                        if commUser.userType == 'arcgisonly':
                            print (user.update(userType='both'))
                            print (commUser.username + ":  enabling Esri Access")
                        else:
                            print (commUser.username + ":  Esri Access already enabled")
                            
                    else:
                        if commUser.userType == 'both':
                            print (user.update(userType='arcgisonly'))
                            print (commUser.username + ":  disabling Esri Access")
                        else:
                            print (commUser.username + ":  Esri Access already disabled")
                else:
                    print (commUser.username + ": skipped")
                        
