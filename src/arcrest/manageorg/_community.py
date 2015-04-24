from ..security.security import OAuthSecurityHandler, AGOLTokenSecurityHandler
from .._abstract.abstract import BaseAGOLClass
import urlparse
import json
import os
########################################################################
class Community(BaseAGOLClass):
    """
       This set of resources contains operations related to users and groups.
    """
    _baseURL = None
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    def checkUserName(self, username):
        """
        Checks if a username is able to be used.

        Inputs:
           username - name of user to create.
        Output:
           JSON as string
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "usernames" : username
        }
        url = self._url + "/checkUsernames"
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def userInformation(self):
        """ returns information about the user """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=self._url + "/self",
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getUserCommunity(self, username=None):
            """
            The user's community are items

            Inputs:
               username - name of user to query
            """
            if username is None:
                username = self._securityHandler.username

            url = self._url + "/users/%s" % username

            params = {
                "f" : "json",
                "token" : self._securityHandler.token
            }
            return self._do_get(url=url,
                                 header=("Accept-Encoding",""),
                                 param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port,
                                 compress=False)
    #----------------------------------------------------------------------
    def groupSearch(self, q, t=None,
                    start=1, num=10,
                    sortField="title", sortOrder="asc"):
        """
        The Group Search operation searches for groups in the portal. The
        search index is updated whenever groups and organizations are
        created, updated, or deleted. There can be a lag between the time
        that a group is updated and the time when it's reflected in the
        search results. The results only contain groups that the user has
        permission to access.
        Inputs:
           q - query string to search
           t - type search
           start - number of the first entry in response results. The
                   default is 1
           num - maximum number of results to return.  The maximum is 100.
           sortField - field to sort by. Allowed values: title, owner or
                       created.
           sortOrder - Order of result values returned.  Values: asc or desc
        """
        params = {
            "f" : "json",
            "q" : q,
            "num" : num,
            "start" : start
        }
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        if not t is None:
            params['t'] = t
        if not sortField is None:
            params['sortField'] = sortField
        if not sortOrder is None:
            params['sortOrder'] = sortOrder
        url = self._url + "/groups"
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getGroupIDs(self, groupNames,communityInfo=None):
        """
           This function retrieves the group IDs

           Inputs:
              group_names - tuple of group names

           Output:
              dict - list of group IDs
        """
        group_ids=[]
        if communityInfo is None:
            communityInfo = self.getUserCommunity()

        if 'groups' in communityInfo:
            for gp in communityInfo['groups']:
                if gp['title'] in groupNames:
                    group_ids.append(gp['id'])
        del communityInfo
        return group_ids
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
        """
        The Create Group operation (POST only) creates a new group in the
        Portal community. Only authenticated users can create groups. The
        user who creates the group automatically becomes the owner of the
        group. The owner of the group is automatically an administrator of
        the group. The calling user provides the title for the group, while
        the group ID is generated by the system.

        Inputs:
           title - The group title must be unique for the username, and the
                   character limit is 250.
           tags - Tags are words or short phrases that describe the group.
                  Separate terms with commas.
           description -  A description of the group that can be any length
           snippet - Snippet or summary of the group that has a character
                     limit of 250 characters.
           phone - group contact information
           access - Sets the access level for the group. private is the
                    default. Setting to org restricts group access to
                    members of your organization. If public, all users can
                    access the group.
                    Values: private | org |public
           sortField -  Sets sort field for group items.
                        Values: title | owner | avgRating |numViews
                                | created | modified
           sortOrder - sets sort order for group items. Values: asc or desc
           isViewOnly -  Allows the group owner or dmin to create view-only
                         groups where members are not able to share items.
                         If members try to share, view-only groups are
                         returned in the notshared response property. false
                         is the default.
           isInvitationOnly - If true, this group will not accept join
                              requests. If false, this group does not
                              require an invitation to join. Only group
                              owners and admins can invite users to the
                              group. false is the default.
           thumbnail - Enter the pathname to the thumbnail image to be used
                       for the group. The recommended image size is 200
                       pixels wide by 133 pixels high. Acceptable image
                       formats are PNG, GIF, and JPEG. The maximum file size
                       for an image is 1 MB. This is not a reference to
                       the file but the file itself, which will be stored
                       in the Portal.
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "title" : title,
            "description" : description,
            "snippet" : snippet,
            "tags" : tags,
            "phone" : phone,
            "access" : access,
            "sortField" : sortField,
            "sortOrder" : sortOrder,
            "isViewOnly" : isViewOnly,
            "isInvitationOnly" : isInvitationOnly
        }
        files = []
        url = self._url + "/createGroup"
        parsed = urlparse.urlparse(url)

        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))
            res = self._post_multipart(host=parsed.hostname,
                                       port=parsed.port,
                                       selector=parsed.path,
                                       fields=params,
                                       files=files,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_url=self._proxy_url,
                                       proxy_port=self._proxy_port)
            return res
        else:
            return self._do_post(url=url, param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def communityRoot(self):
        """ returns the community root URL """
        return self._url
    #----------------------------------------------------------------------
    @property
    def groups(self):
        """ returns the group object """
        return Groups(url="%s/groups" % self.communityRoot,
                       securityHandler=self._securityHandler,
                       proxy_url=self._proxy_url,
                       proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def user(self):
        """
           returns the user class object for current session
        """
        return User(url="%s/users" % self.communityRoot,
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port)

########################################################################
class Groups(BaseAGOLClass):
    """
        The Group resource represents a group (for example, San Bernardino
        Fires) within the portal.
        The owner is automatically an administrator and is returned in the
        list of admins. Administrators can invite, add to, or remove
        members from a group as well as update or delete the group. The
        administrator for an organization can also reassign the group to
        another member of the organization.
        Group members can leave the group. Authenticated users can apply to
        join a group unless the group is by invitation only.
        The visibility of the group by other users is determined by the
        access property. If the group is private, no one other than the
        administrators and members of the group will be able to see it. If
        the group is shared with an organization, all members of the
        organization will be able to find it.

        Inputs:
           url - group URL to site/agol
           securityHandler - Oauth or AGOL security handler
           proxy_url - optional - URL of proxy
           proxy_port - optional - port of the proxy
    """
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    def acceptGroupInvitation(self, groupId, username):
        """
        When a user applies to join a group, a group application is
        created. Group administrators choose to accept this application
        using the Accept Group Application operation (POST only). This
        operation adds the applying user to the group then deletes the
        application. This operation also creates a notification for the
        user indicating that the user's group application was accepted.
        Available only to group owners and admins.

        Inputs:
           groupId - unique Id of the group to join
           username - name of user that will accept the invite

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/%s/applications/%s/accept" % (groupId,
                                                                             username),
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def addUsersToGroups(self, users, groupID):
        """
        The operation to Add Users to Group (POST only) is available only
        to the group administrators, including the owner, and to the
        administrator of the organization if the user is a member. Both
        users and admins can be added using this operation. This is useful
        if you wish to add users directly within an organization without
        requiring them to accept an invitation. For example, a member of an
        organization can add only other organization members but not public
        users.

        Inputs:
           users - comma seperates list of users to add to a group
           groupID - Unique id of a group
        Output:
           A JSON array of usernames that were not added.
        """
        url = self._url + "/%s/addUsers" % groupID
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "users" : users,
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    def deleteGroup(self, groupID):
        """
        deletes a group based on it's ID
        Inputs:
           groupID - Unique id of a group
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/%s/delete" % groupID,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    ##----------------------------------------------------------------------
    def groupInformation(self, groupId):
        """
        The Group resource represents a group (for example, San Bernardino
        Fires) within the portal.
        The owner is automatically an administrator and is returned in the
        list of admins. Administrators can invite, add to, or remove
        members from a group as well as update or delete the group. The
        administrator for an organization can also reassign the group to
        another member of the organization.
        Group members can leave the group. Authenticated users can apply to
        join a group unless the group is by invitation only.
        The visibility of the group by other users is determined by the
        access property. If the group is private, no one other than the
        administrators and members of the group will be able to see it. If
        the group is shared with an organization, all members of the
        organization will be able to find it.
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/%s" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def searchGroup(self, q, start=1, num=10, sortField="title",
                    sortOrder="asc"):
        """
        The Group Search operation searches for groups in the portal. The
        search index is updated whenever groups and organizations are
        created, updated, or deleted. There can be a lag between the time
        that a group is updated and the time when it's reflected in the
        search results. The results only contain groups that the user has
        permission to access.

        Inputs:
        q - The query string to search the groups against.
        start - The number of the first entry in the result set response.
                The index number is 1-based. The default value of start is
                1 (for example, the first search result).The start
                parameter, along with the num parameter, can be used to
                paginate the search results.
        num - The maximum number of results to be included in the result
              set response.The start parameter, along with the num
              parameter, can be used to paginate the search results. The
              actual number of returned results may be less than num. This
              happens when the number of results remaining after start is
              less than num.
        sortField - Field to sort by. The allowed field names are title,
                    owner, and created.
        sortOrder - Describes whether order returns in ascending or
                    descending order. Default is ascending.
                    Values: asc | desc
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "q" : q,
            "start" : start,
            "num" : num,
            "sortOrder" : sortOrder,
            "sortField" : sortField
        }
        return self._do_get(url=self._url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def groupUsers(self, groupId):
        """
        Lists the users, owner, and administrators of a given group. Only
        available to members or administrators of the group.

        Input:
        groupId - id of group
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
            }
        return self._do_get(url=self._url + "/%s/users" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def inviteToGroup(self, groupId, users, role, expiration=1440):
        """
        A group administrator can invite users to join their group using
        the Invite to Group operation. This creates a new user invitation,
        which the users accept or decline. The role of the user and the
        invitation expiration date can be set in the invitation.
        A notification is created for the user indicating that they were
        invited to join the group. Available only to authenticated users.

        Inputs:
           groupId - unique identifier of the group
           users - A comma separated list of usernames to be invited to the
                   group. If a user is already a member of the group or an
                   invitation has already been sent, the call still returns
                   a success.
                   Example: users=regularusername1,regularusername2
           role	- Allows administrators to set the user's role in the group
                  Roles are:
                     group_member: Ability to view and share items with
                                   group.
                     group_admin: In addition to viewing and sharing items,
                                  the group_admin has the same capabilities
                                  as the group owner-invite users to the
                                  group, accept or decline group
                                  applications, delete content, and remove
                                  users.
           expiration - Expiration date on the invitation can be set for
                        one day, three days, one week, or two weeks, in
                        minutes. Default is 1440
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "users" : users,
            "role" : role,
            "expiration" : expiration
        }
        return self._do_post(url=self._url + "/%s/invite" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def declineGroupApplication(self, groupId, username):
        """
        When a user applies to join a group, a group application is created
        Group administrators can decline this application using the Decline
        Group Application operation (POST only). This operation deletes the
        application and creates a notification for the user indicating that
        the user's group application was declined. The applying user will
        not be added to the group. Available only to group owners and
        admins.

        Inputs:
           groupId - unique Id of the group to join
           username - name of user that will decline the invite

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/%s/applications/%s/decline" % (groupId,
                                                                             username),
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def groupApplication(self, groupId, applicationUsername):
        """
        When an individual user applies to join a group, a group
        application is created. The group administrators can accept or
        decline the application. Available only to the group administrators
        and the administrator of the organization if the group belongs to
        an organization.

        Inputs:
           groupId - unique identifier of the group
           applicationUsername - Name of user that applied to group
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=self._url + "/%s/applications/%s" % (groupId, applicationUsername),
                                     param_dict=params,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def groupApplications(self, groupId):
        """
        Lists the group applications for the given group. Available to
        administrators of the group or administrators of an organization if
        the group is part of one.
        Inputs:
           groupId - unique identifier of the group
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        return self._do_get(url=self._url + "/%s/applications" % groupId,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def joinGroup(self, groupId):
        """
        Users apply to join a group using the Join Group operation. This
        creates a new group application, which the group administrators
        accept or decline. This operation also creates a notification for
        the user indicating that they have applied to join this group.
        Available only to authenticated users.

        Users can only apply to join groups to which they have access. If
        the group is private, users will not be able to find it to ask to
        join it.

        Information pertaining to the applying user, such as their full
        name and username, can be sent as part of the group application.

        Inputs:
           groupId - unique identifier of the group
        """
        params = {
                            "f" : "json",
                            "token" : self._securityHandler.token
                        }
        return self._do_post(url=self._url + "/%s/join" % groupId,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def leaveGroup(self, groupId):
        """
        The Leave Group operation (POST only) is available to all group
        members other than the group owner. Leaving a group automatically
        results in the unsharing of all items the user has shared with the
        group.

        Inputs:
           groupId - unique identifier of the group
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/%s/leave" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def reassignGroup(self, groupId, targetUsername):
        """
        The Reassign Group operation (POST only) allows the administrator
        of an organization to reassign a group to another member of the
        organization.

        Inputs:
           groupId - unique identifier of the group
           targetUsername - The target username of the new owner of the
                            group.
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token,
                    "targetUsername" : targetUsername
                }
        return self._do_post(url=self._url + "/%s/reassign" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUsersFromGroup(self, groupId, users):
        """
        The operation to Remove Users From Group (POST only) is available
        only to the group administrators, including the owner, and to the
        administrator of the organization if the user is a member. Both
        users and admins can be removed using this operation. Group owners
        cannot be removed from the group.

        Inputs:
           groupId - unique identifier of the group
           users - A comma-separated list of usernames (both admins and
                   regular users) to be removed from the group.
                   Example: users=regularusername1,adminusername1,
                                  adminusername2,regularusername2
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "users" : users
        }
        return self._do_post(url=self._url + "/%s/removeUsers" % groupId,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateGroup(self,
                    groupId,
                    clearEmptyFields=True,
                    title=None,
                    description=None,
                    snippet=None,
                    tags=None,
                    phone=None,
                    access=None,
                    sortField=None,
                    sortOrder=None,
                    isViewOnly=None,
                    isInvitationOnly=None,
                    thumbnail=None):
        """
        The Update Group operation (POST only) modifies properties such as
        the group title, tags, description, sort field and order, and
        member sharing capabilities. Available only to the group
        administrators or to the administrator of the organization if the
        user is a member.

        Only the properties that are to be updated need to be specified in
        the request. Properties not specified will not be affected.

        The group ID cannot be modified.

        Inputs:
           groupId - unique identifier of the group
           title - The group title must be unique for the username, and the
                   character limit is 250.
                   Example: title=Redlands Fire Department
           description - A description of the group that can be any length.
           snippet - Snippet or summary of the group that has a character
                     limit of 250 characters.
           tags	- Tags are words or short phrases that describe the group.
                  Separate terms with commas.
           phone - Phone is the group contact information. It can be a
                   combination of letters and numbers. The character limit
                   is 250.
           access - Sets the access level for the group. private is the
                    default. Setting to org restricts group access to
                    members of your organization. If public, all users can
                    access the group.
                    Values: private | org |public
           sortField - Sets sort field for group items.
                       Values: title | owner | avgRating |
                               numViews| created | modified
           sortOrder - Sets sort order for group items.
                       Values: asc | desc
           isViewOnly - Allows the group owner or admin to create view-only
                        groups where members are not able to share items.
                        If members try to share, view-only groups are
                        returned in the notshared response property.
                        Values: false | true

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        if title is not None:
            params['title'] = title
        if description is not None:
            params['description'] = description
        if snippet is not None:
            params['snippet'] = snippet
        if tags is not None:
            params['tags'] = tags
        if phone is not None:
            params['phone'] = phone
        if access is not None:
            params['access'] = access
        if sortField is not None:
            params['sortField'] = sortField
        if isViewOnly is not None:
            params['isViewOnly'] = isViewOnly
        if isInvitationOnly is not None:
            params['isInvitationOnly'] = isInvitationOnly
        if clearEmptyFields is not None:
            params['clearEmptyFields'] = clearEmptyFields
        files = []
        url = self._url + "/%s/update" % groupId
        parsed = urlparse.urlparse(url)


        files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))
        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            res = self._post_multipart(host=parsed.hostname,
                                       port=parsed.port,
                                       selector=parsed.path,
                                       fields=params,
                                       files=files,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_url=self._proxy_url,
                                       proxy_port=self._proxy_port)
            return res
        else:
            return self._do_post(url=url, param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)







########################################################################
class User(BaseAGOLClass):
    """ represents the Group Functions """
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    def getUserInformation(self, username):
        """
           A user resource representing a registered user of the portal.
           Personal details of the user, such as e-mail and groups, are
           returned only to the user or the administrator of the user's
           organization.

           A user is not visible to any other user (except the
           organization's administrator) if their access setting is set to
           "private."

           Inputs:
              username - name of user to query
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(
            url = self._url + "/%s" % username,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def declineInvitation(self, username, invitationId):
        """
        When a group administrator invites a user to their group, it
        results in a group invitation. The invited user can decline the
        invitation using the Decline Invitation operation (POST only). The
        operation deletes the invitation and creates a notification for
        the user indicating that they declined the invitation. The invited
        user is not added to the group. Available only to authenticated
        users.
        Inputs:
           username - name of user to decline invitation
           invitationId - unique invitation identifier

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(
            url = self._url + "/%s/invitations/%s/decline" % (username,
                                                              invitationId),
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def acceptInvitation(self, username, invitationId):
        """
        When a group owner or an administrator invites a user to their
        group, it results in a user invitation. The invited user accepts
        the invitation using the Accept Invitation operation (POST only).
        This operation adds the invited user to the group, and the
        invitation is deleted. This operation also creates a notification
        for the user indicating that the user's invitation was accepted.
        Available only to authenticated users.
        Inputs:
           username - name of user to decline invitation
           invitationId - unique invitation identifier

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(
            url = self._url + "/%s/invitations/%s/accept" % (username,
                                                              invitationId),
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def deleteUser(self, username):
        """
        The Delete User operation (POST only) is available only to the user
        in question or to the administrator of the user's organization.
        If deleting a user who is part of an organization, their content
        and groups must be transferred to another member or deleted prior
        to deleting the user.
        If the user is not part of an organization, all content and groups
        of the user must first be deleted.
        Deleting a user whose identity provider is the Esri Global Account
        will not delete the user from the Esri Global Account system.

        Inputs:
           username - name of user to erase
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        url = self._url + "/%s/delete" % username
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def disable(self, username):
        """
        The Disable operation (POST only) disables login access for the
        user. It is only available to the administrator of the organization.

        Inputs:
           username - username to disable
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        return self._do_get(
            url = self._url + "/%s/disable" % username,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def enable(self, username):
        """
        The Enable operation (POST only) enables login access for the user.
        It is only available to the administrator of the organization.

        Inputs:
           username - username to disable
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        return self._do_get(
            url = self._url + "/%s/enable" % username,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getNotification(self, username, notificationId):
        """
        An individual notification for the given user that can be of
        different types as described in the Notification types section
        below. Available only to the user recipient of the notification.
        In the JSON response for a notification, the data property will
        vary based on the notification type.

        Inputs:
           username - name of user to get notification for
           notificationId - notification identifier to look up

        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        url = self._url + "/%s/notifications/%s" % (username, notificationId)
        return self._do_get(
            url = url,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getAllNotifications(self, username):
        """
        The list of notifications available for the given user. These can
        have different types as described in the documentation for the
        Notification resource.

        Inputs:
           username - name of the user to query
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        url = self._url + "/%s/notifications" % username
        return self._do_get(
            url = url,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateUser(self,
                   username,
                   clearEmptyFields=None,
                   tags=None,
                   thumbnail=None,
                   password=None,
                   fullname=None,
                   email=None,
                   securityQuestionIdx=None,
                   securityAnswer=None,
                   culture=None,
                   region=None
                   ):
        """
        The Update User operation (POST only) modifies properties such as
        description, preferred view, tags, access, and thumbnail. The user
        name cannot be modified. For the "ecas" identity provider, password,
        e-mail, and full name must be modified by editing your Esri Global
        Account. For the "arcgis" identity provider, password, full name,
        security question, and security answer can be updated with Update
        User. Update User is available only to the user or to the
        administrator of the user's organization.
        Only the properties that are to be updated need to be specified in
        the request. Properties not specified will not be affected.

        Inputs:

        username - name of user to update
        clearEmptyFields - Clears any fields that are passed in empty (for
                           example, description, tags).
        tags - Tags are words or short phrases that describe the user.
               Separate terms with commas.
               Example: tags=GIS Analyst, Redlands, cloud GIS
        thumbnail - Enter the pathname to the thumbnail image to be used
                    for the user. The recommended image size is 200 pixels
                    wide by 133 pixels high. Acceptable image formats are
                    PNG, GIF, and JPEG. The maximum file size for an image
                    is 1 MB. This is not a reference to the file but the
                    file itself, which will be stored on the sharing
                    servers.
                    Example: thumbnail=subfolder/thumbnail.jpg
        password -Password for the user. Only applicable for the arcgis
                  identity provider.
        fullname - The full name of the user. Only applicable for the
                   arcgis identity provider.
        email - The e-mail address of the user. Only applicable for the
                arcgis identity provider.
        securityQuestionIdx - The index of the security question the user
                wants to use. The security question is used for password
                recovery. Only applicable for the arcgis identity provider.
        securityAnswer - The answer to the security question for the user.
                         Only applicable for the arcgis identity provider.
        culture - Specifies the locale for which content is returned. The
                  browser/machine language setting is the default.
                  Authenticated users can set the culture and overwrite the
                  browser/machine language setting.
        region - Specifies the region of featured maps and apps and the
                 basemap gallery.
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        if region is not None:
            params['region'] = region
        if culture is not None:
            params['culture'] = culture
        if clearEmptyFields is not None:
            params['clearEmptyFields'] = clearEmptyFields
        if tags is not None:
            params['tags'] = tags
        if password is not None:
            params['password'] = password
        if fullname is not None:
            params['fullname'] = fullname
        if email is not None:
            params['email'] = email
        if securityQuestionIdx is not None:
            params['securityQuestionIdx'] = securityQuestionIdx
        if securityAnswer is not None:
            params['securityAnswer'] = securityAnswer

        files = []


        url =  self._url + "/%s/update" % username
        parsed = urlparse.urlparse(url)
        files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))
        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            res = self._post_multipart(host=parsed.hostname,
                                       port=parsed.port,
                                       selector=parsed.path,
                                       fields=params,
                                       files=files,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_url=self._proxy_url,
                                       proxy_port=self._proxy_port)
            return res
        else:
            return self._do_post(url=url, param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def user(self, username):
        """
        A user resource representing a registered user of the portal.
        Personal details of the user, such as e-mail and groups, are
        returned only to the user or the administrator of the user's
        organization (the properties in the Response Properties table
        below).
        A user is not visible to any other user (except the organization's
        administrator) if their access setting is set to "private."
        """
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        return self._do_get(
            url = self._url + "/%s" % username,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def userInvitation(self, username, invitationId):
        """
        An individual invitation to join a given group. The user can accept
        the invitation or decline the invitation.
        Invitations are currently only to join groups but may be extended
        in the future to allow for other targetTypes. Developers should
        design their applications so that targetTypes is checked and
        unknown targetTypes are ignored.
        Invitations are also currently only sent to usernames. This is
        determined by the type property of the invitation. In the future,
        other types of invitations may be introduced. Developers should
        design their applications to make sure they check type and ignore
        unknown types.

        Inputs:
           username - name of the user to query
           invitationId - ID of invitation
        """
        url = self._url + "/%s/invitations/%s" % (username, invitationId)
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(
            url = url,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def userInvitations(self, username):
        """
        Shows the invitations sent to the authenticated user.

        Inputs:
           username - user invitations to query

        """
        url = self._url + "/%s/invitations" % username
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(
            url = url,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def userSearch(self,
                   q,
                   start=1,
                   num=10,
                   sortField="username",
                   sortOrder="asc"):
        """
        The User Search operation searches for users in the portal. The
        search index is updated whenever users are created, updated, or
        deleted. There can be a lag between the time that the user is
        updated and the time when it's reflected in the search results. The
        results only contain users that the calling user has permissions to
        see. Users can control this visibility by changing the access
        property of their user.

        Inputs:
        q -The query string to search the users against.
        start - The number of the first entry in the result set response.
                The index number is 1-based. The default value of start is
                1 (for example, the first search result). The start
                parameter, along with the num parameter can be used to
                paginate the search results.
        num - The maximum number of results to be included in the result
              set response. The default value is 10, and the maximum
              allowed value is 100. The start parameter, along with the num
              parameter can be used to paginate the search results. The
              actual number of returned results may be less than num. This
              happens when the number of results remaining after start is
              less than num.
        sortField - Field to sort by. The allowed field names are username
                    and created.
        sortOrder - Describes whether the returned results are in ascending
                    or descending order. Default is ascending.
                    Values: asc | desc
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "q" : q,
            "start" : start,
            "num" : num,
            "sortField" : sortField,
            "sortOrder" : sortOrder
        }
        url = self._url
        return self._do_get(
            url = url,
            param_dict=params,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def userTags(self, username):
        """
        Users tag the content they publish in their portal via the add and
        update item calls. This resource lists all the tags used by the
        user along with the number of times the tags have been used.

        Inputs:
           username - name of the user to query
        """
        url = self._url + "/%s/tags" % username
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }