"""
   This sample shows how to add an item to
   AGOL/Portal using ArcREST
   ArcREST version 3.5.x
   Python 2/3
"""
from __future__ import print_function
import arcrest

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    portalId = "<portal Id>"
    url = "<portal or AGOL url>"
    thumbnail_url = "<url to thumbnail>"
    kml_path = r"<path to KML item>"
    securityHandler = arcrest.AGOLTokenSecurityHandler(username,
                                                       password)
    #   Create the administration connection
    #
    admin = arcrest.manageorg.Administration(url, securityHandler)
    #   Access the content properties to add the item
    #
    content = admin.content
    #   Access the user to add the item to
    #
    user = content.users.user() # gets the logged in user.
    #   Provide the item parameters
    #

    itemParams = arcrest.manageorg.ItemParameter()
    itemParams.thumbnailurl = thumbnail_url
    itemParams.title = "KML FILE"
    itemParams.type = "KML"
    itemParams.tags = "KML,Google,test"
    #   Add the item
    #
    print (user.addItem(filePath=kml_path,
                       itemParameters=itemParams))
