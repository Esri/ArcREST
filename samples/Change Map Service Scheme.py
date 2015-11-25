"""
   This sample shows users how to add a map service via URL, then
   update that item's URL from http scheme to https.

   This method will work for both Portal and ArcGIS Online

   Python 2/3
   ArcREST 3.5.x
"""
from __future__ import print_function
import arcrest

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    org_url = "<portal org url>"
    url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/MontgomeryQuarters/MapServer"
    #  Create a security handler for portal
    #
    sh = arcrest.PortalTokenSecurityHandler(username=username,
                                            password=password,
                                            org_url=org_url)
    #  Access the admin side of the site
    #
    admin = arcrest.manageorg.Administration(url=org_url, securityHandler=sh)
    content = admin.content
    users = content.users
    user = users.user(username=username)
    ip = arcrest.manageorg.ItemParameter()
    ip.title = "MontgomeryQuarters"
    ip.description = "Represents a simple map service"
    ip.tags = "MapService"
    ip.type = "Map Service"
    item = user.addItem(itemParameters=ip,
                       url=url)
    item.updateItem(itemParameters=arcrest.manageorg.ItemParameter(), serviceUrl=url.replace("http://", "https://") + "#")
    item.updateItem(itemParameters=arcrest.manageorg.ItemParameter(), serviceUrl=url.replace("http://", "https://"))
