
from _abstract import abstract

class resetTools(abstract.baseToolsClass):
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
                            for userItem in folderContent['items']:
                                print adminusercontent.deleteItems(items=userItem['id'])

                            print adminusercontent.deleteFolder(folderId=userItem['id'])
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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

        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
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

