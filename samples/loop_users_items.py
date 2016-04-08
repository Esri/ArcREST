
"""
   This sample shows how to loop through all users and their
   items

   Python 2/3
   ArcREST version 3.5.x
"""
from __future__ import print_function
import arcrest
from arcrest.security import AGOLTokenSecurityHandler

datetimeformat = '%m/%d/%Y %H:%M:%S'
if __name__ == "__main__":
    username = ""#Username
    password = ""#password
    proxy_port = None
    proxy_url = None

    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)


    admin = arcrest.manageorg.Administration(securityHandler=agolSH)
    content = admin.content
   
    commUsers = admin.portals.portalSelf.users(start=1, num=100)
    commUsers = commUsers['users']
    
    
    for commUser in commUsers:
        user = admin.content.users.user(commUser.username)
        for userItem in user.items:
            msg = "Item: {0}".format(userItem.id)
            msg = msg +  "\n\tName: {0}".format(userItem.name)
            msg = msg +  "\n\tTitle: {0}".format(userItem.title)
            msg = msg +  "\n\tOwned by: {0}".format(commUser.username)
            msg = msg +  "\n\tCreated on: {0}".format(arcrest.general.online_time_to_string(userItem.modified,datetimeformat))
            msg = msg +  "\n\tLast modified on: {0}".format(arcrest.general.online_time_to_string(userItem.modified,datetimeformat))
            msg = msg +  "\n\tNum Views: {0}".format(userItem.numViews)
            msg = msg +  "\n\tModified: {0}".format(arcrest.general.online_time_to_string(userItem.modified,datetimeformat))
            msg = msg +  "\n----------------------------------------------------------"
            print (msg)