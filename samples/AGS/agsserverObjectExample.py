"""
Demonstrates some simple usage of the ags.agsserver object.
New at version 3 of ArcREST
"""
import arcrest

url = "https://<my server>:6443/arcgis"
sh = arcrest.AGSTokenSecurityHandler(username="<username>", password="<password>", org_url=url)
server = arcrest.ags.server.Server(url=url,
                                   securityHandler=sh)
#  Access the AGSAdminstration Class
#
adminAGS = server.admin
print adminAGS.currentVersion
print adminAGS.clusters
#  Walk all the folders and
#  print out the raw JSON response
#  for each service and the url
for folder in server.folders:
    server.currentFolder = folder
    for service in server.services:
        print '----------------------'
        print service.url
        print str(service)
        print '----------------------'