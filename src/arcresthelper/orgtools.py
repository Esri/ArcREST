
from _abstract import abstract

class orgtools(abstract.baseToolsClass):
    _username = None
    _password = None
    _org_url = None
    _proxy_url = None
    _proxy_port = None
    _token_url = None
    _securityHandler = None
    _valid = True
    _message = ""
    #----------------------------------------------------------------------
    def __init__(self,
                 username,
                 password,
                 org_url=None,
                 token_url = None,
                 proxy_url=None,
                 proxy_port=None):

        """Constructor"""
        self._org_url = org_url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._token_url = token_url
        if self._org_url is None or self._org_url =='':
            self._org_url = 'http://www.arcgis.com'
        if self._org_url is None or '.arcgis.com' in  self._org_url:
            self._securityHandler = arcrest.AGOLTokenSecurityHandler(username=self._username,
                                                              password=self._password,
                                                              org_url=self._org_url,
                                                              token_url=self._token_url,
                                                              proxy_url=self._proxy_url,
                                                              proxy_port=self._proxy_port)
        else:

            self._securityHandler = arcrest.PortalTokenSecurityHandler(username=self._username,
                                                              password=self._password,
                                                              org_url=self._org_url,
                                                              proxy_url=self._proxy_url,
                                                              proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def dispose(self):
        self._username = None
        self._password = None
        self._org_url = None
        self._proxy_url = None
        self._proxy_port = None
        self._token_url = None
        self._securityHandler = None
        self._valid = None
        self._message = None

        del self._username
        del self._password
        del self._org_url
        del self._proxy_url
        del self._proxy_port
        del self._token_url
        del self._securityHandler
        del self._valid
        del self._message
    #----------------------------------------------------------------------
    @property
    def message(self):
        """ returns any messages """
        return self._message
    #----------------------------------------------------------------------
    @property
    def valid(self):
        """ returns boolean wether handler is valid """

        return self._valid
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
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "shareItemsToGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "createGroup",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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
