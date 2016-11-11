
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

class orgtools(securityhandlerhelper):

    #----------------------------------------------------------------------
    def shareItemsToGroup(self, shareToGroupName, items=None, groups=None):
        """Share already published items with a group(s).
        
        Args:
            shareToGroupName (list): The name of the group(s) with which the item(s) will be shared.
            items (list): The item(s) that will be shared, referenced by their ID. Defaults to ``None``.
            groups (list): The group(s) whose content will be shared, referenced by their ID. Defaults to ``None``.            
        Notes:
            If you want to share with a single group, ``shareToGroupName`` can be passed as a ``str``.
        
        """
        admin = None
        userCommunity = None
        group_ids = None
        results = None
        item = None
        res = None
        group = None
        groupContent = None
        result = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            userCommunity = admin.community
            group_ids = userCommunity.getGroupIDs(groupNames=shareToGroupName)
            results = []
            if not items is None:
                for item in items:
                    item = admin.content.getItem(itemId = item)
                    res = item.shareItem(",".join(group_ids),everyone=False,org=False)
                    if 'error' in res:
                        print (res)
                    else:
                        print ("'%s' shared with '%s'" % (item.title,shareToGroupName))
                    results.append(res)
            if not groups is None:
                for groupId in groups:
                    group = admin.content.group(groupId=groupId)

                    if group is None:
                        print ("Group with ID {0} was not found".format(groupId))

                    elif group.hasError() == True:
                        print ("Group with ID {0} returned the following error {1}".format(groupId,group.error))
                    else:
                        for itemJSON in group.items:
                            if 'id' in itemJSON:
                                item = admin.content.getItem(itemId = itemJSON['id'])
                                res = item.shareItem(",".join(group_ids),everyone=False,org=False)
                                if 'error' in res:
                                    print (res)
                                elif res.get('notSharedWith', []):
                                    print ("'%s' shared with '%s', not Shared With '%s'" % \
                                          (item.title,shareToGroupName,",".join(res['notSharedWith'])))
                                else:
                                    print ("'%s' shared with '%s'" % (item.title,shareToGroupName))
                                results.append(res)

        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "shareItemsToGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            userCommunity = None
            group_ids = None

            item = None
            res = None
            group = None
            groupContent = None
            result = None

            del admin
            del userCommunity
            del group_ids

            del item
            del res
            del group
            del groupContent
            del result
            gc.collect()
    #----------------------------------------------------------------------
    def getGroupContentItems(self, groupName):
        """Gets all the items owned by a group(s).
        
        Args:
            groupName (list): The name of the group(s) from which to get items.
        Returns:
            list: A list of items belonging to the group(s).
        Notes:
            If you want to get items from a single group, ``groupName`` can be passed as a :py:obj:`str`.
        See Also:
            :py:func:`getGroupContent` for retrieving all content, not just items.
        
        """
        admin = None
        userCommunity = None
        groupIds = None
        groupId = None

        groupContent = None
        result = None
        item = None
        items = []
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            userCommunity = admin.community
            groupIds = userCommunity.getGroupIDs(groupNames=groupName)
            #groupContent = admin.query(q="group:" + group_ids , bbox=None, start=1, num=100, sortField=None,
                       #sortOrder="asc")

            if not groupIds is None:
                for groupId in groupIds:
                    groupContent = admin.content.groupContent(groupId=groupId)
                    if 'error' in groupContent:
                        print (groupContent)
                    else:
                        for result in groupContent['items']:
                            item = admin.content.getItem(itemId = result['id'])
                            items.append(item)
            return items
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "getGroupContent",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                )
        finally:
            admin = None
            userCommunity = None
            groupIds = None
            groupId = None
            groupContent = None
            result = None
            item = None


            del admin
            del userCommunity
            del groupIds
            del groupId
            del groupContent
            del result
            del item

            gc.collect()
    #----------------------------------------------------------------------
    def getGroupContent(self, groupName, onlyInOrg=False, onlyInUser=False):
        """Gets all the content from a group.
        
        Args:
            groupName (str): The name of the group from which to get items.
            onlyInOrg (bool): A boolean value to only return content belonging to the current org.
                Defaults to ``False``.
            onlyInUser (bool): A boolean value to only return content belonging to the current user
                credentials. Defaults to ``False``.
        Returns:
            list: A list of content belonging to the group.        
        See Also:
            :py:func:`getGroupContentItems` for retrieving only items.
            
        """
        admin = None
        groups = None
        q = None
        results = None
        res = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            groups = admin.community.groups
            q = groupName
            #if onlyInOrg is True:
                #q += " orgid: %s" % admin.portals.portalSelf.id
            if onlyInUser is True:
                q += " owner: %s" % self._securityHandler.username
            results = groups.search(q = q)
            if 'total' in results and 'results' in results:
                if results['total'] > 0:
                    for res in results['results']:
                        group = admin.content.group(groupId=res['id'])
                        return group.items

            return None
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "getGroupContent",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            groups = None
            q = None
            results = None
            res = None

            del admin
            del groups
            del q
            del results
            del res

            gc.collect()
    #----------------------------------------------------------------------
    def getThumbnailForItem(self, itemId, fileName, filePath):
        """Gets an item's thumbnail and saves it to disk.
        
        Args:
            itemId (str): The item's ID.
            fileName (str): The name of the output image.
            fileName (str): The directory on disk where to save the thumbnail.
        Returns:
            dict: The result from :py:func:`arcrest.manageorg._content.UserItem.saveThumbnail`
        
        """
        admin = None
        item = None

        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            item = admin.content.getItem(itemId = itemId)
            return item.saveThumbnail(fileName=fileName,filePath=filePath)
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "getThumbnailForItem",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            item = None
            del admin
            del item
            gc.collect()
    #----------------------------------------------------------------------
    def createGroup(self,
                    title,
                    tags,
                    description="",
                    snippet="",
                    phone="",
                    access="org", sortField="title",
                    sortOrder="asc", isViewOnly=False,
                    isInvitationOnly=False, thumbnail=None):
        """Creates a new group.
        
        Args:
            title (str): The name of the new group, limited to 250 characters.
            tags (str): A comma delimited list of tag names.
            description (str): A description of the group that can be any length.
            snippet (str): Snippet or summary of the group that has a character limit of 250 characters.
                Defaults to ``""``.
            phone (str): Group contact information, limited to 250 characters. Defaults to ``""``.
            access (str): Sets the access level for the group. Defaults to ``"org"``.
            sortField (str): Sets sort field for group items. Defaults to ``"title"``.
            sortOrder (str): Sets sort order for group items. Defaults to ``"asc"``.
            isViewOnly (bool): A boolean value to create a view-only group with no sharing. Defaults to ``False``.
            isInvitationOnly (bool): A boolean value to not accept join requests. Defaults to ``False``.
            thumbnail (str): The full pathname to the group thumbnail to upload. Defaults to ``None``.
        Returns:
            If sucessful, the result from :py:func:`arcrest.manageorg._community.Community.createGroup`.
            
            If the group already exists or there is an error, ``None`` is returned.
        
        +------------+----------------------------------------------------------------+
        | Parameters |                      Possible Values                           |
        +------------+----------------------------------------------------------------+
        | access     | ``private|org|public``                                         |
        +------------+----------------------------------------------------------------+
        | sortField  | ``title|owner|avgrating|numviews|created|modified``            |
        +------------+----------------------------------------------------------------+
        | sortOrder  | ``asc|desc``                                                   |
        +------------+----------------------------------------------------------------+
            
        """
        admin = None
        userCommunity = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            userCommunity = admin.community
            try:
                groupExist = userCommunity.getGroupIDs(groupNames=title)
                if len(groupExist) > 0:
                    print ("Group '%s' already exists" % title)
                    return None
                return userCommunity.createGroup(title=title,
                            tags=tags,
                            description=description,
                            snippet=snippet,
                            phone=phone,
                            access=access,
                            sortField=sortField,
                            sortOrder=sortOrder,
                            isViewOnly=isViewOnly,
                            isInvitationOnly=isInvitationOnly,
                            thumbnail=thumbnail)
            except Exception as e:
                print (e)
                return None


        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "createGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            userCommunity = None


            del admin
            del userCommunity


            gc.collect()
    #----------------------------------------------------------------------
    def createRole(self, name, description="", privileges=None):
        """Creates a new role.
        
        Args:
            name (str): The name of the new role.
            description (str): The description of the new role. Defaults to ``""``.
            privileges (str): A comma delimited list of privileges to apply to the new role.
                Defaults to ``None``.
        Returns:
            If ``privileges`` is ``None``, the result from :py:func:`arcrest.manageorg._portals.Portal.createRole`.
            
            If ``privileges`` were succesfully added, the result from :py:func:`arcrest.manageorg._portals.Roles.setPrivileges`.
            
        """
        admin = None
        portal = None
        setPrivResults = None
        roleID = None
        createResults = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            portal = admin.portals.portalSelf
            try:
                roleID = portal.roles.findRoleID(name)
                if roleID is None:
                    createResults = portal.createRole(name=name,description=description)
                    if 'success' in createResults:
                        if createResults['success'] == True:

                            setPrivResults = portal.roles.setPrivileges(createResults['id'],privileges)
                            if 'success' in setPrivResults:
                                print ("%s role created" % name)
                            else:
                                print (setPrivResults)
                        else:
                            print (createResults)
                    else:
                        print (createResults)
                else:
                    print ("'%s' role already exists" % name)

            except Exception as e:
                print (e)
                return None


        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "createGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            portal = None
            setPrivResults = None
            roleID = None
            createResults = None

            del admin
            del portal
            del setPrivResults
            del roleID
            del createResults

            gc.collect()
