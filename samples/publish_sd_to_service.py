"""
   This sample shows how to publish and
   Item to AGOL as a Hosted Feature Service

"""
import arcrest

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    portalId = "<portal Id>"
    url = "<portal or AGOL url>"
    itemId = "<item id>"
    tags = "Demo, Publishing"
    securityHandler = arcrest.AGOLTokenSecurityHandler(username,
                                                       password)
    #   Create the administration connection
    #
    admin = arcrest.manageagol.Administration(url, securityHandler)
    #   Connect to the portal
    #
    portal = admin.portals(portalId)
    #   Access the content properties to add the item
    #
    content = admin.content
    #   Provide the Publish parameters
    #

    publishParameters = arcrest.manageagol.PublishSDParmaeters(tags=tags)
    #   Enter in the username you wish to load the item to
    #
    usercontent = content.usercontent(username=username)
    print usercontent.publishItem(
        fileType="serviceDefinition",
        itemId=itemId,
        publishParameters=publishParameters)

    # sample result message
    #   {'services': [{'encodedServiceURL': '<url>', 'jobId': '<job id>',
    #   'serviceurl': '<url>', 'type': 'Feature Service',
    #   'serviceItemId': '<id value>', 'size': <int>}]}