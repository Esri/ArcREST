
from __future__ import print_function

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

class orgtools(securityhandlerhelper):

    #----------------------------------------------------------------------
    def shareItemsToGroup(self,shareToGroupName,items=None,groups=None):

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
                        print ("%s shared with %s" % (item.title,shareToGroupName))
                    results.append(res)
            if not groups is None:
                for group in groups:
                    group = admin.content.group(groupId=group)
                    if group is None:
                        print ("Group not found")
                    else:
                        for itemJSON in group.items:
                            if 'id' in itemJSON:
                                item = admin.content.getItem(itemId = itemJSON['id'])
                                res = item.shareItem(",".join(group_ids),everyone=False,org=False)
                                if 'error' in res:
                                    print (res)
                                elif 'notSharedWith' in res:
                                    print ("%s shared with %s, not Shared With %s" % \
                                          (item.title,shareToGroupName,",".join(res['notSharedWith'])))
                                else:
                                    print ("%s shared with %s" % (item.title,shareToGroupName))
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
    def getGroupContentItems(self,groupName):

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
    def getGroupContent(self,groupName,onlyInOrg,onlyInUser):

        admin = None
        groups = None
        q = None
        results = None
        res = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            groups = admin.community.groups
            q = groupName
            if onlyInOrg == True:
                q = q + " orgid: %s" % admin.portals.portalSelf.id
            if onlyInUser == True:
                q = q + " owner: %s" % self._securityHandler.username
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
    def getThumbnailForItem(self,itemId,fileName,filePath):

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
        admin = None
        userCommunity = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            userCommunity = admin.community
            try:
                groupExist = userCommunity.getGroupIDs(groupNames=title)
                if len(groupExist) > 0:
                    print ("Group %s already exist" % title)
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
    def createRole(self,
                    name,
                    description="",
                    privileges=None):
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
                    print ("%s role already exist" % name)

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
