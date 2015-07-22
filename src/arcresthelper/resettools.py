
from securityhandlerhelper import securityhandlerhelper

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
import common 
import gc

#----------------------------------------------------------------------
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

class resetTools(securityhandlerhelper):
  
    #----------------------------------------------------------------------
    def removeUserData(self,users=None):
        admin = None
        portal = None
        user = None
        adminusercontent = None
        userFolder = None
        userContent = None
        userItem = None
        folderContent = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            portal = admin.portals(portalId='self')
            if users is None:
                users = portal.users(start=1, num=100)
            if users:
                for user in users['users']:
                    print user['username']
                    adminusercontent = admin.content.usercontent(username=user['username'])

                    userContent = admin.content.getUserContent(username=user['username'])
                    for userItem in userContent['items']:

                        print adminusercontent.deleteItems(items=userItem['id'])
                    if 'folders' in userContent:
                        for userFolder in userContent['folders']:
                            folderContent = admin.content.getUserContent(username=user['username'],folderId=userFolder['id'])
                            if 'items' in folderContent:
                                for userItem in folderContent['items']:
                                    print adminusercontent.deleteItems(items=userItem['id'])

                            print adminusercontent.deleteFolder(folderId=userFolder['id'])
       
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            portal = None
            user = None
            adminusercontent = None
            userFolder = None
            userContent = None
            userItem = None
            folderContent = None

            del admin
            del portal
            del user
            del adminusercontent
            del userFolder
            del userContent
            del userItem
            del folderContent

            gc.collect()


    #----------------------------------------------------------------------
    def removeUserGroups(self,users=None):
        admin = None
        userCommunity = None
        portal = None
        groupAdmin = None
        user = None
        userCommData = None
        group = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            userCommunity = admin.community


            portal = admin.portals(portalId='self')
            if users is None:
                users = portal.users(start=1, num=100)

            groupAdmin = userCommunity.groups
            if users:
                for user in users['users']:
                    print "Loading groups for user: %s" % user['username']
                    userCommData = userCommunity.getUserCommunity(username=user['username'])

                    if 'groups' in userCommData:
                        if len(userCommData['groups']) == 0:
                            print "No Groups Found"
                        else:
                            for group in userCommData['groups']:
                                if group['owner'] == user['username']:
                                    print groupAdmin.deleteGroup(groupID=group['id'])
                    else:
                        print "No Groups Found"

       
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            userCommunity = None
            portal = None
            groupAdmin = None
            user = None
            userCommData = None
            group = None

            del admin
            del userCommunity
            del portal
            del groupAdmin
            del user
            del userCommData
            del group

            gc.collect()

