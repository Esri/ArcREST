"""
   This sample shows how to copy an item

   Python 2.x
   ArcREST 3.0.1
"""
import arcrest
from arcresthelper import securityhandlerhelper
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

    securityinfoOrg1 = {}
    securityinfoOrg1['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfoOrg1['username'] = "<User Name>"
    securityinfoOrg1['password'] = "<Password>"
    securityinfoOrg1['org_url'] = "http://www.arcgis.com"
    securityinfoOrg1['proxy_url'] = proxy_url
    securityinfoOrg1['proxy_port'] = proxy_port
    securityinfoOrg1['referer_url'] = None
    securityinfoOrg1['token_url'] = None
    securityinfoOrg1['certificatefile'] = None
    securityinfoOrg1['keyfile'] = None
    securityinfoOrg1['client_id'] = None
    securityinfoOrg1['secret_id'] = None

    securityinfoOrg2 = {}
    securityinfoOrg2['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfoOrg2['username'] = "<User Name>"
    securityinfoOrg2['password'] = "<Password>"
    securityinfoOrg2['org_url'] = "http://www.arcgis.com"
    securityinfoOrg2['proxy_url'] = proxy_url
    securityinfoOrg2['proxy_port'] = proxy_port
    securityinfoOrg2['referer_url'] = None
    securityinfoOrg2['token_url'] = None
    securityinfoOrg2['certificatefile'] = None
    securityinfoOrg2['keyfile'] = None
    securityinfoOrg2['client_id'] = None
    securityinfoOrg2['secret_id'] = None

    itemId = "<ID if item>"
    
    try:

        shhOrg1 = securityhandlerhelper.securityhandlerhelper(securityinfoOrg1)
        shhOrg2 = securityhandlerhelper.securityhandlerhelper(securityinfoOrg2)
        
        portalAdmin1 = arcrest.manageorg.Administration(securityHandler=shhOrg1.securityhandler)
        portalAdmin2 = arcrest.manageorg.Administration(securityHandler=shhOrg2.securityhandler)
        
        item = portalAdmin1.content.getItem(itemId=itemId)

        itemParams = arcrest.manageorg.ItemParameter()
        itemParams.title = item.title
        itemParams.type = item.type
        itemParams.description = item.description
        itemParams.tags = item.tags
        itemParams.snippet = item.snippet
        itemParams.typeKeywords = item.typeKeywords
        itemParams.url = item.url
        itemParams.itemData = item.itemData
        
        content = portalAdmin2.content
        userInfo = content.users.user()
        item = userInfo.addItem(
            itemParameters=itemParams,
            overwrite=True,
            relationshipType=None,
            originItemId=None,
            destinationItemId=None,
            serviceProxyParams=None,
            metadata=None)
        print res

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

if __name__ == "__main__":
    main()