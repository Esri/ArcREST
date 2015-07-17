from arcrest.security.security import AGSTokenSecurityHandler
from arcrest.manageags import AGSAdministration

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

if __name__ == "__main__":
    username = "admin"
    password = "admin.account"
    url = "https://arcrestdev1.esri.com/arcgis/admin/"
   
    try:      
        sh = AGSTokenSecurityHandler(username=username, 
                                     password=password, 
                                     org_url="http://arcrestdev1.esri.com/arcgis", 
                                    token_url=None, 
                                    proxy_url=None, 
                                    proxy_port=None)
        print sh.token
        ags = AGSAdministration(url=url,
                          securityHandler=sh,
                          proxy_url=None,
                          proxy_port=None)
        print ags.data

    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)