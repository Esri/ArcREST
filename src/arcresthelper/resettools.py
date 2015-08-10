
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
            if users is None:
                users = admin.portal.portalSelf.users(start=1, num=100)
            
            if users:
                for user in users['users']:
                    print "Loading groups for user: %s" % user['username']
                    user = admin.content.users.user(user)            
                    for userItem in user.items:

                        print user.deleteItems(items=userItem.id)
                    if user.folders:
                        for userFolder in user.folders:
                            user.currentFolder = userFolder['name']
                            for userItem in user.items:
                                print user.deleteItems(items=userItem['id'])

                            print user.deleteFolder(folderId=userFolder['id'])
       
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "removeUserData",
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
            if users is None:
                users = admin.portal.portalSelf.users(start=1, num=100)
            
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
        
            if users:
                for user in users['users']:
                    print "Loading groups for user: %s" % user['username']
                    userCommData = admin.community.users.user(user)
                    
                    if userCommData.groups:
                        for group in userCommData.groups:
                            if group.owner == user:
                                print group.delete()
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

