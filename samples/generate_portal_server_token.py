"""
   This show is used to test the generation
   of a portal and server token

   Python 2/3
   ArcREST version 3.5.0

"""
from __future__ import print_function
import arcrest

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

if __name__ == "__main__":

    username = ""
    password = ""
    url = "www.arcgis.com"
    try:
        sh = arcrest.PortalTokenSecurityHandler(username=username, password=password, org_url=url)
        admin = arcrest.manageorg.Administration(url=url,
                                             securityHandler=sh)

        hostingServers = admin.hostingServers()
        for server in hostingServers:
            print( server.currentVersion)
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror