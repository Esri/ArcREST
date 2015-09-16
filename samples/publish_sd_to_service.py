"""
   This sample shows how to publish and
   Item to AGOL/Portal as a Hosted Feature Service.

   It assumes you have ALREADY added the item to the site.

"""
import arcrest

if __name__ == "__main__":
    #   Inputs
    #
    username = "<username>"
    password = "<password>"
    url = "<portal or AGOL url>"
    itemId = "<item id>" # item id of SD file
    tags = "Demo, Publishing"
    siteType = "AGOL" # can be AGOL or PORTAL
    #   Logic
    #
    if siteType == "AGOL":
        securityHandler = arcrest.AGOLTokenSecurityHandler(username,
                                                           password)
        admin = arcrest.manageorg.Administration(securityHandler=securityHanlder)
    else:
        securityHandler = arcrest.PortalTokenSecurityHandler(username, password, org_url=url)
        admin = arcrest.manageorg.Administration(url, securityHandler)
    #   Access the User to gain access the the publishItem()
    #
    content = admin.content
    users = content.users()
    user = users.user(username=username)
    #   Provide the Publish parameters
    #
    publishParameters = arcrest.manageorg.PublishSDParmaeters(tags=tags)
    #   Publish the service to the site
    #
    print user.publishItem(
        fileType="serviceDefinition",
        itemId=itemId,
        publishParameters=publishParameters)

    # sample result message
    #   {'services': [{'encodedServiceURL': '<url>', 'jobId': '<job id>',
    #   'serviceurl': '<url>', 'type': 'Feature Service',
    #   'serviceItemId': '<id value>', 'size': <int>}]}