"""
   This sample shows how to publish and
   Item to AGOL/Portal as a Hosted Feature Service.

   It assumes you have ALREADY added the item to the site.

   Python 2/3
   ArcREST 3.5.0

"""
from __future__ import print_function
import arcrest

if __name__ == "__main__":
    #   Inputs
    #
    username = ""
    password = ""
    url = "" #URL to ArcGIS Online or your portal
    itemId = "" # item id of SD file
    itemFolder = None # If you item is in a folder, you need to specify its name here
    tags = "Demo, Publishing"
    siteType = "AGOL" # can be AGOL or PORTAL
    #   Logic
    #
    if siteType == "AGOL":
        securityHandler = arcrest.AGOLTokenSecurityHandler(username,
                                                           password)
        admin = arcrest.manageorg.Administration(securityHandler=securityHandler)
    else:
        securityHandler = arcrest.PortalTokenSecurityHandler(username, password, org_url=url)
        admin = arcrest.manageorg.Administration(url=url, securityHandler=securityHandler)
    #   Access the User to gain access the the publishItem()
    #
    content = admin.content
    users = content.users
    user = users.user(username=username)
    if itemFolder is not None:
        user.currentFolder = itemFolder
    #   Provide the Publish parameters
    #
    publishParameters = arcrest.manageorg.PublishSDParmaeters(tags=tags)
    #   Publish the service to the site
    #
    print (user.publishItem(
        fileType="serviceDefinition",
        itemId=itemId,
        publishParameters=publishParameters))

    #a UserItem is a valid return object