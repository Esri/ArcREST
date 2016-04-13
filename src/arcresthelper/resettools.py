from __future__ import print_function
from __future__ import absolute_import

from .securityhandlerhelper import securityhandlerhelper

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
from . import common
import gc

#----------------------------------------------------------------------
def trace():
    """Determines information about where an error was thrown.

    Returns:
        tuple: line number, filename, error message
    Examples:
        >>> try:
        ...     1/0
        ... except:
        ...     print("Error on '{}'\\nin file '{}'\\nwith error '{}'".format(*trace()))
        ...        
        Error on 'line 1234'
        in file 'C:\\foo\\baz.py'
        with error 'ZeroDivisionError: integer division or modulo by zero'
        
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
    def removeUserData(self, users=None):
        """Removes users' content and data.
        
        Args:
            users (str): A comma delimited list of user names.
                Defaults to ``None``.
        
        Warning:
            When ``users`` is not provided (``None``), all users
            in the organization will have their data deleted!
        
        """ 
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
                print ("You have selected to remove all users data, you must modify the code to do this")
                usersObj = []
                commUsers = admin.portals.portalSelf.users(start=1, num=100)
                commUsers = commUsers['users']
                for user in commUsers:
                    usersObj.append(user.userContent)
                return
            else:
                usersObj = []
                userStr = users.split(',')
                for user in userStr:
                    try:
                        user = admin.content.users.user(str(user).strip())
                        usersObj.append(user)
                    except:
                        print ("%s does not exist" % str(user).strip())

            if usersObj:
                for user in usersObj:
                    print ("Loading content for user: %s" % user.username)

                    itemsToDel = []
                    for userItem in user.items:
                        itemsToDel.append(userItem.id)
                    if len(itemsToDel) > 0:
                        print (user.deleteItems(items=",".join(itemsToDel)))
                    if user.folders:
                        for userFolder in user.folders:
                            if (user.currentFolder['title'] != userFolder['title']):
                                user.currentFolder = userFolder['title']
                                itemsToDel = []
                                for userItem in user.items:
                                    itemsToDel.append(userItem.id)
                                if len(itemsToDel) > 0:
                                    print (user.deleteItems(items=",".join(itemsToDel)))

                                print (user.deleteFolder())

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
    def removeUserGroups(self, users=None):
        """Removes users' groups.
        
        Args:
            users (str): A comma delimited list of user names.
                Defaults to ``None``.
        
        Warning:
            When ``users`` is not provided (``None``), all users
            in the organization will have their groups deleted!
        
        """ 
        admin = None
        userCommunity = None
        portal = None
        groupAdmin = None
        user = None
        userCommData = None
        group = None
        try:

            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            if users is None:
                print ("You have selected to remove all users groups, you must modify the code to do this")
                usersObj = []
                commUsers = admin.portals.portalSelf.users(start=1, num=100)
                usersObj = commUsers['users']

                return
            else:
                usersObj = []
                userStr = users.split(',')
                for user in userStr:
                    try:
                        user = admin.community.users.user(str(user).strip())
                        usersObj.append(user)
                    except:
                        print ("%s does not exist" % str(user).strip())
            if usersObj:
                for userCommData in usersObj:
                    print ("Loading groups for user: %s" % userCommData.username)

                    if userCommData.groups:
                        for group in userCommData.groups:
                            groupObj = admin.community.groups.group(groupId=group['id'])
                            if groupObj.owner == userCommData.username:
                                print (groupObj.delete())
                    else:
                        print ("No Groups Found")
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "removeUserGroups",
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
