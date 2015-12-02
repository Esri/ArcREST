"""
   This sample shows how to add users to an org
   version 3.0.1
   Python 2
"""
import arcrest
from arcresthelper import securityhandlerhelper
from arcrest import manageorg

def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

def main():
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

    try:

        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if shh.valid == False:
            print shh.message
        else:
            admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            portal = admin.portals.portalSelf
            invList = manageorg.InvitationList()
            #Make sure to adhere to the password requirements
            #Make sure the user name is available
            invList.addUser(username="MyFakeUser", password="1TestTestTestTest", firstname="Test", lastname="Test", 
                            email="test@test.com", role="account_user")
            res = portal.addUser(invitationList=invList,
                        subject="test", html="test")
            print res
          

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

if __name__ == "__main__":
    main()