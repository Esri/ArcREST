"""
   This sample shows how to update an item

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
    import traceback, inspect, sys
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
    securityinfo['username'] = "<User Name>"
    securityinfo['password'] = "<Password>"
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None


    itemId = "<ID if item>"
    upload_file = r"<Path to File>"
    try:

        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if shh.valid == False:
            print shh.message
        else:
            portalAdmin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            item = portalAdmin.content.getItem(itemId=itemId).userItem

            itemParams = arcrest.manageorg.ItemParameter()

            itemParams.filename = upload_file
            res = item.updateItem(itemParameters=itemParams,
                                    clearEmptyFields=True,
                                    data=None,
                                    serviceUrl=None,
                                    text=None
                                    )

            print res

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

if __name__ == "__main__":
    main()
