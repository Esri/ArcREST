
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
                    item = admin.content.item(itemId = item)
                    res = item.shareItem(",".join(group_ids),everyone=False,org=False)
                    if 'error' in res:
                        print res
                    else:
                        print "%s shared with %s" % (item.title,shareToGroupName)
                    results.append(res)
            if not groups is None:
                for group in groups:
                    groupContent = admin.content.groupContent(groupId=group)
                    if 'error' in groupContent:
                        print groupContent
                    else:
                        for result in groupContent['items']:
                            item = admin.content.item(itemId = result['id'])
                            res = item.shareItem(",".join(group_ids),everyone=False,org=False)
                            if 'error' in res:
                                print res
                            else:
                                print "%s shared with %s" % (result['title'],shareToGroupName)
                            results.append(res)
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "shareItemsToGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
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
                        print groupContent
                    else:
                        for result in groupContent['items']:
                            item = admin.content.item(itemId = result['id'])
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
    def getGroupContent(self,groupName):

        admin = None
        userCommunity = None
        groupIds = None
        groupId = None

        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            userCommunity = admin.community
            groupIds = userCommunity.getGroupIDs(groupNames=groupName)
            if not groupIds is None:
                for groupId in groupIds:

                    return admin.query(q="group:" + groupId , bbox=None, start=1, num=100, sortField=None,
                               sortOrder="asc")
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
    def getThumbnailForItem(self,itemId,fileName,filePath):

        admin = None

        item = None

        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            item = admin.content.item(itemId = itemId)
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
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "createGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
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
