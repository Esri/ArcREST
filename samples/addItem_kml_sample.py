"""
   This sample shows how to add an item to
   AGOL/Portal using ArcREST

"""
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
    #   Connect to the portal
    #
    portal = admin.portals(portalId)
    #   Access the content properties to add the item
    #
    content = admin.content
    #   Provide the item parameters
    #

    itemParams = arcrest.manageorg.ItemParameter()
    itemParams.thumbnailurl = thumbnail_url
    itemParams.title = "KML FILE"
    itemParams.type = "KML"
    itemParams.tags = "KML,Google,test"
    #   Enter in the username you wish to load the item to
    #
    usercontent = content.usercontent(username=username)
    print usercontent.addItem(filePath=kml_path,
                              itemParameters=itemParams)

    # sample result message
    #   {"success" : true,"id" : "<item id>","folder" : null}
