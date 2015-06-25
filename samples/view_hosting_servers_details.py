from arcrest.security import AGSTokenSecurityHandler,PortalTokenSecurityHandler
from arcrest.manageags import AGSAdministration
import arcrest
if __name__ == "__main__":
    username = "<Username>"
    password = "<Password>"
    url = "<Org URL>"
    proxy_port = None
    proxy_url = None
  
    sH  = PortalTokenSecurityHandler(username=username,
                                            password=password,
                                            org_url=url,
                                            proxy_url=proxy_url,
                                            proxy_port=proxy_port)
   
    admin = arcrest.manageorg.Administration(url=url,
                                             securityHandler=sH)
    try:
        hostingServers = admin.hostingServers()
        for hostingServer in hostingServers:
            if isinstance(hostingServer, AGSAdministration):
                print str(hostingServer.data.rootDataItems)
                print str(hostingServer.clusters)
                print str(hostingServer.services)
                print str(hostingServer.usagereports)
                print str(hostingServer.logs)
                print str(hostingServer.kml.items)
                print str(hostingServer.security.resources)
                print str(hostingServer.system)
               
    except Exception,e:
        print e
    try:
        username = "<UserName>"
        password = "<Password>"
        token_url = "https://<ServerURL>/<Instance>/sharing/rest/generateToken"
        url = "http://<ServerURL>/arcgis/admin"
        proxy_port = None
        proxy_url = None  
        
        sH = AGSTokenSecurityHandler(username=username,
                                     password=password,
                                     token_url=token_url)   
        
        hostingServer = AGSAdministration(url=url, securityHandler=sH, 
                                         proxy_url=None, 
                                         proxy_port=None, 
                                         initialize=False)
        print str(hostingServer.data.rootDataItems)
        print str(hostingServer.clusters)
        print str(hostingServer.services)
        print str(hostingServer.usagereports)
        print str(hostingServer.logs)
        print str(hostingServer.kml.items)
        print str(hostingServer.security.resources)
        print str(hostingServer.system)
    except Exception,e:
        print e        