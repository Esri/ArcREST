"""
   This sample shows how to update tan item
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

    securityInfo = {}
    securityInfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityInfo['username'] = "<User Name>"
    securityInfo['password'] = "<Password>"
    securityInfo['org_url'] = "http://www.arcgis.com"
    securityInfo['proxy_url'] = proxy_url
    securityInfo['proxy_port'] = proxy_port
    securityInfo['referer_url'] = None
    securityInfo['token_url'] = None
    securityInfo['certificatefile'] = None
    securityInfo['keyfile'] = None
    securityInfo['client_id'] = None
    securityInfo['secret_id'] = None   


    itemId = "<ID if item>"    
    upload_file = r"<Path to File>"
    try:      

        shh = securityhandlerhelper.securityhandlerhelper(securityInfo)
        if shh.valid == False:
            print shh.message
        else:        
            portalAdmin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            uc = portalAdmin.content.usercontent()
            itemParams = arcrest.manageorg.ItemParameter()
            
            itemParams.filename = upload_file        
            res = uc.updateItem(itemId=itemId,
                                              updateItemParameters=itemParams,
                                              folderId=None,
                                              clearEmptyFields=True,
                                              filePath=upload_file,
                                              url=None,
                                              text=None,
                                              multipart = False
                                              )

            print res

    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)

if __name__ == "__main__":
    main()