from __future__ import absolute_import
from __future__ import print_function
from ..packages.six.moves import urllib_parse as urlparse

from .._abstract.abstract import BaseAGOLClass
from datetime import datetime, timedelta
from ..common.general import local_time_to_online

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
    def __str__(self):
        """returns the raw json string from the class"""
        return ""
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the key/values of an object"""
        for k,v in {}.items():
            yield k,v
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
            "usernames" : username
        }
        url = self._url + "/checkUsernames"
        return self._post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def communitySelf(self):
        """ This resource allows discovery of the current authenticated
        user identified by the token. """
        params = {
            "f" : "json",
        }
        return self._get(url=self._url + "/self",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def search(self,
               q,
               t=None,
               start=1,
               num=10,
               sortField="title",
               sortOrder="asc"):
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
        if not t is None:
            params['t'] = t
        if not sortField is None:
            params['sortField'] = sortField
        if not sortOrder is None:
            params['sortOrder'] = sortOrder
        url = self._url + "/groups"
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            communityInfo = self.communitySelf

        if isinstance(groupNames,list):
            groupNames = map(str.upper, groupNames)
        else:
            groupNames = groupNames.upper()
        if 'groups' in communityInfo:
            for gp in communityInfo['groups']:

                if str(gp['title']).upper() in groupNames:
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
                    access="org",
                    sortField="title",
                    sortOrder="asc",
                    isViewOnly=False,
                    isInvitationOnly=False,
                    thumbnail=None):
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
        url = self._url + "/createGroup"

        groups = self.groups
        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            res = self._post(url=url,
                             param_dict=params,
                             files={'thumbnail': thumbnail},
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
        else:
            res = self._post(url=url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)

        if "group" not in res:
            raise Exception("%s" % res)
        if "id" not in res['group']:
            raise Exception("%s" % res)
        groupId = res['group']['id']
        url = "%s/groups/%s" % (self.root, groupId)
        return Group(url=url,
                     securityHandler=self._securityHandler,
                     proxy_url=self._proxy_url,
                     proxy_port=self._proxy_port,
                     initalize=False)

    #----------------------------------------------------------------------
    @property
    def root(self):
        """ returns the community root URL """
        return self._url
    #----------------------------------------------------------------------
    @property
    def groups(self):
        """ returns the group object """
        return Groups(url="%s/groups" % self.root,
                       securityHandler=self._securityHandler,
                       proxy_url=self._proxy_url,
                       proxy_port=self._proxy_port,
                       initalize=False)
    #----------------------------------------------------------------------
    @property
    def users(self):
        """
           returns the user class object for current session
        """
        return Users(url="%s/users" % self.root,
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port,
                    )
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
    _json = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initalize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initalize:
            self.__init()

    _currentUser = None
    _portalId = None
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""

        if self._portalId is None:

            from .administration import Administration
            portalSelf = Administration(url=self._securityHandler.org_url,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port).portals.portalSelf

            self._portalId = portalSelf.id
            self._currentUser = portalSelf.user['username']
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns the url for the class"""
        return self._url
    #----------------------------------------------------------------------
    def __str__(self):
        """returns raw JSON response as string"""
        if self._json is None:
            self.__init()
        return ""
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns Group objects"""
        self.__init()
        q = " orgid: %s" % self._portalId

        nextStart = 0
        while nextStart > -1:
            results = self.search(q=q, start=nextStart, num=100)
            grps = results['results']
            for grp in grps:
                yield self.group(grp['id'])
            nextStart = results['nextStart']
    #----------------------------------------------------------------------
    def search(self, q, start=1, num=10, sortField="title",
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
            "q" : q,
            "start" : start,
            "num" : num,
            "sortOrder" : sortOrder,
            "sortField" : sortField
        }
        return self._get(url=self._url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def group(self, groupId):
        """
        gets a group based on it's ID
        """
        url = "%s/%s" % (self.root, groupId)
        return Group(url=url,
                     securityHandler=self._securityHandler,
                     proxy_url=self._proxy_url,
                     proxy_port=self._proxy_port,
                     initalize=False)

########################################################################
class Group(BaseAGOLClass):
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
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    _json_dict = None
    _snippet = None
    _isFav = None
    _description = None
    _title = None
    _isReadOnly = None
    _sortField = None
    _id = None
    _isViewOnly = None
    _modified = None
    _created = None
    _access = None
    _phone = None
    _providerGroupName = None
    _sortOrder = None
    _provider = None
    _owner = None
    _userMembership = None
    _isInvitationOnly = None
    _thumbnail = None
    _featuredItemsId = None
    _isPublic = None
    _isOrganization = None
    _tags = None
    _capabilities = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initalize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initalize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in Group class.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns raw JSON response as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns properties (key/values) from the JSON response"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        '''gets the property value for snippet'''
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def snippet(self):
        '''gets the property value for snippet'''
        if self._snippet is None:
            self.__init()
        return self._snippet

    #----------------------------------------------------------------------
    @property
    def isFav(self):
        '''gets the property value for isFav'''
        if self._isFav is None:
            self.__init()
        return self._isFav

    #----------------------------------------------------------------------
    @property
    def description(self):
        '''gets the property value for description'''
        if self._description is None:
            self.__init()
        return self._description

    #----------------------------------------------------------------------
    @property
    def title(self):
        '''gets the property value for title'''
        if self._title is None:
            self.__init()
        return self._title

    #----------------------------------------------------------------------
    @property
    def isReadOnly(self):
        '''gets the property value for isReadOnly'''
        if self._isReadOnly is None:
            self.__init()
        return self._isReadOnly

    #----------------------------------------------------------------------
    @property
    def sortField(self):
        '''gets the property value for sortField'''
        if self._sortField is None:
            self.__init()
        return self._sortField

    #----------------------------------------------------------------------
    @property
    def id(self):
        '''gets the property value for id'''
        if self._id is None:
            self.__init()
        return self._id

    #----------------------------------------------------------------------
    @property
    def isViewOnly(self):
        '''gets the property value for isViewOnly'''
        if self._isViewOnly is None:
            self.__init()
        return self._isViewOnly

    #----------------------------------------------------------------------
    @property
    def modified(self):
        '''gets the property value for modified'''
        if self._modified is None:
            self.__init()
        return self._modified

    #----------------------------------------------------------------------
    @property
    def created(self):
        '''gets the property value for created'''
        if self._created is None:
            self.__init()
        return self._created

    #----------------------------------------------------------------------
    @property
    def access(self):
        '''gets the property value for access'''
        if self._access is None:
            self.__init()
        return self._access

    #----------------------------------------------------------------------
    @property
    def phone(self):
        '''gets the property value for phone'''
        if self._phone is None:
            self.__init()
        return self._phone

    #----------------------------------------------------------------------
    @property
    def providerGroupName(self):
        '''gets the property value for providerGroupName'''
        if self._providerGroupName is None:
            self.__init()
        return self._providerGroupName

    #----------------------------------------------------------------------
    @property
    def sortOrder(self):
        '''gets the property value for sortOrder'''
        if self._sortOrder is None:
            self.__init()
        return self._sortOrder

    #----------------------------------------------------------------------
    @property
    def provider(self):
        '''gets the property value for provider'''
        if self._provider is None:
            self.__init()
        return self._provider

    #----------------------------------------------------------------------
    @property
    def owner(self):
        '''gets the property value for owner'''
        if self._owner is None:
            self.__init()
        return self._owner

    #----------------------------------------------------------------------
    @property
    def userMembership(self):
        '''gets the property value for userMembership'''
        if self._userMembership is None:
            self.__init()
        return self._userMembership

    #----------------------------------------------------------------------
    @property
    def isInvitationOnly(self):
        '''gets the property value for isInvitationOnly'''
        if self._isInvitationOnly is None:
            self.__init()
        return self._isInvitationOnly

    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        '''gets the property value for thumbnail'''
        if self._thumbnail is None:
            self.__init()
        return self._thumbnail

    #----------------------------------------------------------------------
    @property
    def featuredItemsId(self):
        '''gets the property value for featuredItemsId'''
        if self._featuredItemsId is None:
            self.__init()
        return self._featuredItemsId

    #----------------------------------------------------------------------
    @property
    def isPublic(self):
        '''gets the property value for isPublic'''
        if self._isPublic is None:
            self.__init()
        return self._isPublic

    #----------------------------------------------------------------------
    @property
    def isOrganization(self):
        '''gets the property value for isOrganization'''
        if self._isOrganization is None:
            self.__init()
        return self._isOrganization

    #----------------------------------------------------------------------
    @property
    def tags(self):
        '''gets the property value for tags'''
        if self._tags is None:
            self.__init()
        return self._tags
    #----------------------------------------------------------------------
    def reassign(self, targetUsername):
        """
        The Reassign Group operation (POST only) allows the administrator
        of an organization to reassign a group to another member of the
        organization.

        Inputs:
           targetUsername - The target username of the new owner of the
                            group.
        """
        params = {
                    "f" : "json",
                    "targetUsername" : targetUsername
                }
        return self._post(url=self._url + "/reassign",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def update(self,
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
            "f" : "json"
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
        files = {}
        url = self._url + "/update"

        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            files['thumbnail'] =thumbnail
        res = None
        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            res = self._post(url=url,
                             param_dict=params,
                             files=files,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
            return res
        else:
            res = self._post(url=url, param_dict=params,
                                securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self.__init()
        return res
    #----------------------------------------------------------------------
    def delete(self):
        """
        deletes the current group
        """
        params = {
            "f" : "json",
        }
        return self._post(url=self._url + "/delete",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def join(self):
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

        Output:
           JSON response as dictionary
        """
        params = {
            "f" : "json",
        }
        return self._post(url=self._url + "/join",
                             securityHandler=self._securityHandler,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def invite(self, users, role, expiration=1440):
        """
        A group administrator can invite users to join their group using
        the Invite to Group operation. This creates a new user invitation,
        which the users accept or decline. The role of the user and the
        invitation expiration date can be set in the invitation.
        A notification is created for the user indicating that they were
        invited to join the group. Available only to authenticated users.

        Inputs:
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
            "users" : users,
            "role" : role,
            "expiration" : expiration
        }
        return self._post(url=self._url + "/invite",
                             securityHandler=self._securityHandler,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def leave(self):
        """
        The Leave Group operation (POST only) is available to all group
        members other than the group owner. Leaving a group automatically
        results in the unsharing of all items the user has shared with the
        group.

        Output:
        JSON response as a dictionary
        """
        params = {
            "f" : "json"
        }
        return self._post(url=self._url + "/leave",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUsersFromGroup(self, users):
        """
        The operation to Remove Users From Group (POST only) is available
        only to the group administrators, including the owner, and to the
        administrator of the organization if the user is a member. Both
        users and admins can be removed using this operation. Group owners
        cannot be removed from the group.

        Inputs:
           users - A comma-separated list of usernames (both admins and
                   regular users) to be removed from the group.
                   Example: users=regularusername1,adminusername1,
                                  adminusername2,regularusername2
        """
        params = {
            "f" : "json",
            "users" : users
        }
        return self._post(url=self._url + "/removeUsers",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def addUsersToGroups(self, users):
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
        Output:
           A JSON array of usernames that were not added.
        """
        url = self._url + "/addUsers"
        params = {
            "f" : "json",
            "users" : users,
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def groupUsers(self):
        """
        Lists the users, owner, and administrators of a given group. Only
        available to members or administrators of the group.
        """
        params = {
            "f" : "json"
            }
        return self._get(url=self._url + "/users",
                            securityHandler=self._securityHandler,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def applications(self):
        """returns all the group applications to join"""
        url = self._url + "/applications"
        params = {"f" : "json"}
        res = self._get(url=url,
                           param_dict=params,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        items = []
        if "applications" in res.keys():
            for apps in res['applications']:
                items.append(
                    self.Application(url="%s/%s" % (self._url, apps['username']),
                                     securityHandler=self._securityHandler,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)
                )
        return items
    ########################################################################
    class Application(BaseAGOLClass):
        """reprsents a single group application to join a site"""
        _url = None
        _securityHandler = None
        _proxy_url = None
        _proxy_port = None
        _fullname = None
        _received = None
        _username = None
        _json = None
        _json_dict = None
        #----------------------------------------------------------------------
        def __init__(self, url, securityHandler,
                     proxy_url=None, proxy_port=None,
                     initialize=False):
            """Constructor"""
            self._url = url
            self._securityHandler = securityHandler
            if not securityHandler is None:
                self._referer_url = securityHandler.referer_url
            self._proxy_port = proxy_port
            self._proxy_url = proxy_url
            if initialize:
                self.__init()
        #----------------------------------------------------------------------
        def __init(self):
            """loads the property data into the class"""
            params = {
                "f" : "json"
            }
            json_dict = self._get(url=self._url,
                                     param_dict=params,
                                     securityHandler=self._securityHandler,
                                     proxy_port=self._proxy_port,
                                     proxy_url=self._proxy_url)
            self._json_dict = json_dict
            self._json = json.dumps(json_dict)
            attributes = [attr for attr in dir(self)
                          if not attr.startswith('__') and \
                          not attr.startswith('_')]
            for k,v in json_dict.items():
                if k in attributes:
                    setattr(self, "_"+ k, json_dict[k])
                else:
                    print (k, " - attribute not implemented in Group.Application class.")
        #----------------------------------------------------------------------
        @property
        def username(self):
            """gets the application username"""
            if self._username is None:
                self.__init()
            return self._username
        #----------------------------------------------------------------------
        @property
        def fullname(self):
            """gets the user's full name"""
            if self._fullname is None:
                self.__init()
            return self._fullname
        #----------------------------------------------------------------------
        @property
        def received(self):
            """gets the UTC timestamp when the application was submitted"""
            if self._received is None:
                self.__init()
            return self._received
        #----------------------------------------------------------------------
        @property
        def root(self):
            """returns the current url of the class"""
            return self._url
        #----------------------------------------------------------------------
        def __str__(self):
            """returns object as string"""
            if self._json is None:
                self.__init()
            return self._json
        #----------------------------------------------------------------------
        def __iter__(self):
            """returns JSON as [key,value] objects"""
            if self._json_dict is None:
                self.__init()
            for k,v in self._json_dict.items():
                yield [k,v]
        #----------------------------------------------------------------------
        def accept(self):
            """
            When a user applies to join a group, a group application is
            created. Group administrators choose to accept this application
            using the Accept Group Application operation (POST only). This
            operation adds the applying user to the group then deletes the
            application. This operation also creates a notification for the
            user indicating that the user's group application was accepted.
            Available only to group owners and admins.
            """
            params = {
                "f" : "json",
            }
            return self._post(url="%s/accept" % (self.root),
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        #----------------------------------------------------------------------
        def decline(self):
            """
            When a user applies to join a group, a group application is created
            Group administrators can decline this application using the Decline
            Group Application operation (POST only). This operation deletes the
            application and creates a notification for the user indicating that
            the user's group application was declined. The applying user will
            not be added to the group. Available only to group owners and
            admins.
            """
            params = {
                "f" : "json",
            }
            return self._post(url="%s/decline" % self.root,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
########################################################################
class Users(BaseAGOLClass):
    """represents the users on a given portal or agol system"""
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor"""
        if url.endswith('/users'):
            self._url = url
        else:
            self._url = url + "/users"
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
    #----------------------------------------------------------------------
    @property
    def root(self):
        """gets the url for the class"""
        return self._url
    #----------------------------------------------------------------------
    def __str__(self):
        """gets the object as a string (user list)"""
        return ""
    #----------------------------------------------------------------------
    def search(self,
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
            "q" : q,
            "start" : start,
            "num" : num,
            "sortField" : sortField,
            "sortOrder" : sortOrder
        }
        url = self._url
        return self._get(
            url = url,
            param_dict=params,
            securityHandler=self._securityHandler,
            proxy_url=self._proxy_url,
            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def __getUsername(self):
        """tries to parse the user name from various objects"""

        if self._securityHandler is not None and \
           not self._securityHandler._username is None:
            return self._securityHandler._username
        elif self._securityHandler is not None and \
               hasattr(self._securityHandler, "org_url") and \
               self._securityHandler.org_url is not None:
            from .administration import Administration
            user = Administration(url=self._securityHandler.org_url,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port).portals.portalSelf.user
            return user['username']
        else:
            from .administration import Administration
            url = self._url.lower().split('/content/')[0]
            user = Administration(url=url,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port).portals.portalSelf.user
            return user['username']

    #----------------------------------------------------------------------
    def user(self, username=None):
        """A user resource that represents a registered user in the portal."""
        if username is None:
            username = self.__getUsername() 
        parsedUsername = urlparse.quote(username)
        url = self.root + "/%s" % parsedUsername
        return User(url=url,
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port,
                    initialize=False)
########################################################################
class User(BaseAGOLClass):
    """
    A user resource that represents a registered user in the portal.
    """
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _disabled = None
    _culture = None
    _storageUsage = None
    _favGroupId = None
    _privileges = None
    _access = None
    _role = None
    _idpUsername = None
    _provider = None
    _units = None
    _mfaEnabled = None
    _email = None
    _username = None
    _storageQuota = None
    _description = None
    _tags = None
    _groups = None
    _fullName = None
    _userType = None
    _created = None
    _region = None
    _modified = None
    _thumbnail = None
    _orgId = None
    _preferredView = None
    _lastLogin = None
    _validateUserProfile = None
    _assignedCredits = None
    _availableCredits = None
    _firstName = None
    _lastName = None
    _clientApps = None
    _accountId = None
    _privacy = None
    _defaultGroupId = None
    _organization = None
    _roleId = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
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
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in User class.")
    #----------------------------------------------------------------------
    @property
    def root(self):
        """gets the url of the class"""
        return self._url
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as raw string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterates through json and returns values as [key, value]"""
        if self._json_dict is None:
            self._json_dict = {}
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def userContent(self):
        """allows access into the individual user's content to get at the
        items owned by the current user"""
        replace_start = self._url.lower().find("/community/")
        len_replace = len("/community/")
        url = self._url.replace(self._url[replace_start:replace_start+len_replace],
                                '/content/')
        from ._content import User as UserContent
        return UserContent(url=url,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def lastName(self):
        '''gets the property value for username'''
        if self._lastName is None:
            self.__init()
        return self._lastName
    #----------------------------------------------------------------------
    @property
    def firstName(self):
        '''gets the property value for username'''
        if self._firstName is None:
            self.__init()
        return self._firstName
    #----------------------------------------------------------------------
    @property
    def assignedCredits(self):
        """returns the assignedCredits value"""
        if self._assignedCredits is None:
            self.__init()
        return self._assignedCredits
    #----------------------------------------------------------------------
    @property
    def availableCredits(self):
        """gets the availableCredits value"""
        if self._availableCredits is None:
            self.__init()
        return self._availableCredits
    #----------------------------------------------------------------------
    @property
    def disabled(self):
        '''gets disabled value'''
        if self._disabled is None:
            self.__init()
        return self._disabled
    #----------------------------------------------------------------------
    @property
    def culture(self):
        '''gets culture value'''
        if self._culture is None:
            self.__init()
        return self._culture
    #----------------------------------------------------------------------
    @property
    def storageUsage(self):
        '''gets storageUsage value'''
        if self._storageUsage is None:
            self.__init()
        return self._storageUsage
    #----------------------------------------------------------------------
    @property
    def favGroupId(self):
        '''gets favGroupId value'''
        if self._favGroupId is None:
            self.__init()
        return self._favGroupId
    #----------------------------------------------------------------------
    @property
    def privileges(self):
        '''gets privileges value'''
        if self._privileges is None:
            self.__init()
        return self._privileges
    #----------------------------------------------------------------------
    @property
    def access(self):
        '''gets access value'''
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def role(self):
        '''gets role value'''
        if self._role is None:
            self.__init()
        return self._role
    #----------------------------------------------------------------------
    @property
    def idpUsername(self):
        '''gets idpUsername value'''
        if self._idpUsername is None:
            self.__init()
        return self._idpUsername
    #----------------------------------------------------------------------
    @property
    def provider(self):
        '''gets provider value'''
        if self._provider is None:
            self.__init()
        return self._provider
    #----------------------------------------------------------------------
    @property
    def units(self):
        '''gets units value'''
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def mfaEnabled(self):
        '''gets mfaEnabled value'''
        if self._mfaEnabled is None:
            self.__init()
        return self._mfaEnabled
    #----------------------------------------------------------------------
    @property
    def email(self):
        '''gets email value'''
        if self._email is None:
            self.__init()
        return self._email
    #----------------------------------------------------------------------
    @property
    def username(self):
        '''gets username value'''
        if self._username is None:
            self.__init()
        return self._username
    #----------------------------------------------------------------------
    @property
    def storageQuota(self):
        '''gets storageQuota value'''
        if self._storageQuota is None:
            self.__init()
        return self._storageQuota
    #----------------------------------------------------------------------
    @property
    def description(self):
        '''gets description value'''
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def tags(self):
        '''gets tags value'''
        if self._tags is None:
            self.__init()
        return self._tags
    #----------------------------------------------------------------------
    @property
    def groups(self):
        '''gets groups value'''
        if self._groups is None:
            self.__init()
        return self._groups
    #----------------------------------------------------------------------
    @property
    def fullName(self):
        '''gets fullName value'''
        if self._fullName is None:
            self.__init()
        return self._fullName
    #----------------------------------------------------------------------
    @property
    def userType(self):
        '''gets userType value'''
        if self._userType is None:
            self.__init()
        return self._userType
    #----------------------------------------------------------------------
    @property
    def created(self):
        '''gets created value'''
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def region(self):
        '''gets region value'''
        if self._region is None:
            self.__init()
        return self._region
    #----------------------------------------------------------------------
    @property
    def roleId(self):
        '''gets the roleId value'''
        if self._roleId is None:
            self.__init()
        return self._roleId
    #----------------------------------------------------------------------
    @property
    def modified(self):
        '''gets modified value'''
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        '''gets thumbnail value'''
        if self._thumbnail is None:
            self.__init()
        return self._thumbnail
    #----------------------------------------------------------------------
    @property
    def clientApps(self):
        '''gets clientApps value'''
        if self._clientApps is None:
            self.__init()
        return self._clientApps
    #----------------------------------------------------------------------
    @property
    def accountId(self):
        '''gets accountId value'''
        if self._accountId is None:
            self.__init()
        return self._accountId
    #----------------------------------------------------------------------
    @property
    def privacy(self):
        '''gets privacy value'''
        if self._privacy is None:
            self.__init()
        return self._privacy
    #----------------------------------------------------------------------
    @property
    def defaultGroupId(self):
        '''gets defaultGroupId value'''
        if self._defaultGroupId is None:
            self.__init()
        return self._defaultGroupId
    #----------------------------------------------------------------------
    @property
    def organization(self):
        '''gets organization value'''
        if self._organization is None:
            self.__init()
        return self._organization
    #----------------------------------------------------------------------
    @property
    def orgId(self):
        '''gets orgId value'''
        if self._orgId is None:
            self.__init()
        return self._orgId
    #----------------------------------------------------------------------
    @property
    def preferredView(self):
        '''gets preferredView value'''
        if self._preferredView is None:
            self.__init()
        return self._preferredView
    #----------------------------------------------------------------------
    @property
    def lastLogin(self):
        '''gets lastLogin value'''
        if self._lastLogin is None:
            self.__init()
        return self._lastLogin
    #----------------------------------------------------------------------
    @property
    def validateUserProfile(self):
        '''gets validateUserProfile value'''
        if self._validateUserProfile is None:
            self.__init()
        return self._validateUserProfile
    #----------------------------------------------------------------------
    @property
    def userTags(self):
        """gets a list of current user's tags"""
        url = "%s/tags" % self.root
        params = {
            "f" : "json"
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def invitations(self):
        """returns a class to access the current user's invitations"""
        url = "%s/invitations" % self.root
        return Invitations(url=url,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def notifications(self):
        """The notifications that are available for the given user.
        Notifications are events that need the user's attention-application
        for joining a group administered by the user, acceptance of a group
        membership application, and so on. A notification is initially
        marked as new. The user can mark it as read or delete the notification.
        """
        params = {"f": "json"}
        url = "%s/notifications" % self.root
        return Notifications(url=url,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def invalidateSessions(self):
        """
        forces a given user to have to re-login into portal/agol
        """
        url = "%s/invalidateSessions" % self.root
        params = {"f": "json"}
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def resetPassword(self, email=True):
        """
        resets a users password for an account.  The password will be randomly
        generated and emailed by the system.

        Input:
           email - boolean that an email password will be sent to the
                   user's profile email address.  The default is True.

        """
        url = self.root + "/reset"
        params = {
            "f" : "json",
            "email" : email
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def expirePassword(self,
                       hours="now"):
        """sets a time when a user must reset their password"""

        params = {
            "f" : "json"
        }
        expiration = -1
        if isinstance(hours, str):
            if expiration == "now":
                expiration = -1
            elif expiration == "never":
                expiration = 0
            else:
                expiration = -1
        elif isinstance(expiration, (int, long)):
            dt = datetime.now() + timedelta(hours=hours)
            expiration = local_time_to_online(dt=dt)
        else:
            expiration = -1
        params['expiration'] = expiration
        url = "%s/expirePassword" % self.root
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def disable(self):
        """
        The Disable operation (POST only) disables login access for the
        user. It is only available to the administrator of the organization.
        """
        params = {
                    "f" : "json"
                }
        url = "%s/disable" % self.root
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def enable(self):
        """
        The Enable operation (POST only) enables login access for the user.
        It is only available to the administrator of the organization.

        Inputs:
           username - username to disable
        """
        params = {
            "f" : "json"
        }
        url = self.root + "/enable"
        return self._post(url=url,
                   param_dict=params,
                   securityHandler=self._securityHandler,
                   proxy_url=self._proxy_url,
                   proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def update(self,
               clearEmptyFields=None,
               tags=None,
               thumbnail=None,
               password=None,
               fullname=None,
               email=None,
               securityQuestionIdx=None,
               securityAnswer=None,
               culture=None,
               region=None,
               userType=None
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
        userType - if the value is set to "both", then the value will allow
                   users to access both ArcGIS Org and the forums from this
                   account.  'arcgisorg' means the account is only valid
                   for the organizational site.  This is an AGOL only
                   parameter.
        """
        params = {
            "f" : "json"
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
        if userType is not None and \
           userType.lower() in ['both', 'arcgisorg','arcgisonly']:
            params['userType'] = userType.lower()
        files = {}


        url =  "%s/update" % self.root

        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))
        res = None
        if thumbnail is not None and \
           os.path.isfile(thumbnail):
            res = self._post(url=url,
                             param_dict=params,
                             files=files,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
        else:
            res = self._post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self.__init()
        return res
    #----------------------------------------------------------------------
    def delete(self):
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
        """
        params = {
            "f" : "json"
        }
        url = self.root + "/delete"
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
########################################################################
class Invitations(BaseAGOLClass):
    """Manages the invitations sent to the authenticated user."""
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    _json_dict = None
    _userInvitations = None
    class Invitation(BaseAGOLClass):
        """represents a single invitation for a given user."""
        _url = None
        _securityHandler = None
        _proxy_port = None
        _proxy_url = None
        _json = None
        _json_dict = None
        _username = None
        _targetType = None
        _fromUsername = None
        _created = None
        _mustApprove = None
        _received = None
        _targetId = None
        _id = None
        _dateAccepted = None
        _role = None
        _expiration = None
        _group = None
        _accepted = None
        _type = None
        _email = None
        #----------------------------------------------------------------------
        def __init__(self,
                     url,
                     securityHandler,
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
            if initialize:
                self.__init()
        #----------------------------------------------------------------------
        def __init(self):
            """loads the property data into the class"""
            params = {
                "f" : "json"
            }
            json_dict = self._get(url=self._url,
                                     param_dict=params,
                                     securityHandler=self._securityHandler,
                                     proxy_port=self._proxy_port,
                                     proxy_url=self._proxy_url)
            self._json_dict = json_dict
            self._json = json.dumps(json_dict)
            attributes = [attr for attr in dir(self)
                          if not attr.startswith('__') and \
                          not attr.startswith('_')]
            for k,v in json_dict.items():
                if k in attributes:
                    setattr(self, "_"+ k, json_dict[k])
                else:
                    print( k, " - attribute not implemented in Invitation class.")
        #----------------------------------------------------------------------
        @property
        def root(self):
            """returns the current url of the class"""
            return self._url
        #----------------------------------------------------------------------
        def __str__(self):
            """returns object as string"""
            if self._json is None:
                self.__init()
            return self._json
        #----------------------------------------------------------------------
        def __iter__(self):
            """returns JSON as [key,value] objects"""
            if self._json_dict is None:
                self.__init()
            for k,v in self._json_dict.items():
                yield [k,v]
        #----------------------------------------------------------------------
        @property
        def username(self):
            '''gets the property value for username'''
            if self._username is None:
                self.__init()
            return self._username
        #----------------------------------------------------------------------
        @property
        def targetType(self):
            '''gets the property value for targetType'''
            if self._targetType is None:
                self.__init()
            return self._targetType
        #----------------------------------------------------------------------
        @property
        def fromUsername(self):
            '''gets the property value for fromUsername'''
            if self._fromUsername is None:
                self.__init()
            return self._fromUsername

        #----------------------------------------------------------------------
        @property
        def created(self):
            '''gets the property value for created'''
            if self._created is None:
                self.__init()
            return self._created

        #----------------------------------------------------------------------
        @property
        def mustApprove(self):
            '''gets the property value for mustApprove'''
            if self._mustApprove is None:
                self.__init()
            return self._mustApprove

        #----------------------------------------------------------------------
        @property
        def received(self):
            '''gets the property value for received'''
            if self._received is None:
                self.__init()
            return self._received

        #----------------------------------------------------------------------
        @property
        def targetId(self):
            '''gets the property value for targetId'''
            if self._targetId is None:
                self.__init()
            return self._targetId

        #----------------------------------------------------------------------
        @property
        def id(self):
            '''gets the property value for id'''
            if self._id is None:
                self.__init()
            return self._id

        #----------------------------------------------------------------------
        @property
        def dateAccepted(self):
            '''gets the property value for dateAccepted'''
            if self._dateAccepted is None:
                self.__init()
            return self._dateAccepted

        #----------------------------------------------------------------------
        @property
        def role(self):
            '''gets the property value for role'''
            if self._role is None:
                self.__init()
            return self._role

        #----------------------------------------------------------------------
        @property
        def expiration(self):
            '''gets the property value for expiration'''
            if self._expiration is None:
                self.__init()
            return self._expiration

        #----------------------------------------------------------------------
        @property
        def group(self):
            '''gets the property value for group'''
            if self._group is None:
                self.__init()
            return self._group

        #----------------------------------------------------------------------
        @property
        def accepted(self):
            '''gets the property value for accepted'''
            if self._accepted is None:
                self.__init()
            return self._accepted

        #----------------------------------------------------------------------
        @property
        def type(self):
            '''gets the property value for type'''
            if self._type is None:
                self.__init()
            return self._type

        #----------------------------------------------------------------------
        @property
        def email(self):
            '''gets the property value for email'''
            if self._email is None:
                self.__init()
            return self._email
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
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
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Invitations class.")
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns the current url of the class"""
        return self._url
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns JSON as [key,value] objects"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def userInvitations(self):
        """gets all user invitations"""
        self.__init()
        items = []
        for n in self._userInvitations:
            if "id" in n:
                url = "%s/%s" % (self.root, n['id'])
                items.append(self.Invitation(url=url,
                                             securityHandler=self._securityHandler,
                                             proxy_url=self._proxy_url,
                                             proxy_port=self._proxy_port,
                                             initialize=True))
        return items
########################################################################
class Notifications(BaseAGOLClass):
    """
    A user notification resource available only to the user in question. A
    notification has the following fields:
    {id : string, type : enum, data: string, status : enum }
    Status is either new or read.
    Type is the type of notification, e.g., application to join group or
    invitation to join group.
    """
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    _json_dict = None
    _notifications = None
    class Notification(BaseAGOLClass):
        """represents a single notification inside the notification list"""
        _url = None
        _securityHandler = None
        _proxy_port = None
        _proxy_url = None
        _json = None
        _json_dict = None
        _targetType = None
        _target = None
        _received = None
        _data = None
        _type = None
        _id = None
        def __init__(self, url, securityHandler,
                     proxy_url=None, proxy_port=None,
                     initialize=False):
            """Constructor"""
            self._url = url
            self._securityHandler = securityHandler
            if not securityHandler is None:
                self._referer_url = securityHandler.referer_url
            self._proxy_port = proxy_port
            self._proxy_url = proxy_url
            if initialize:
                self.__init()
        #----------------------------------------------------------------------
        def __init(self):
            """loads the property data into the class"""
            params = {
                "f" : "json"
            }
            json_dict = self._get(url=self._url,
                                     param_dict=params,
                                     securityHandler=self._securityHandler,
                                     proxy_port=self._proxy_port,
                                     proxy_url=self._proxy_url)
            self._json_dict = json_dict
            self._json = json.dumps(json_dict)
            attributes = [attr for attr in dir(self)
                          if not attr.startswith('__') and \
                          not attr.startswith('_')]
            for k,v in json_dict.items():
                if k in attributes:
                    setattr(self, "_"+ k, json_dict[k])
                else:
                    print( k, " - attribute not implemented in Notification class.")
        #----------------------------------------------------------------------
        @property
        def targetType(self):
            '''gets property targetType'''
            if self._targetType is None:
                self.__init()
            return self._targetType

        #----------------------------------------------------------------------
        @property
        def target(self):
            '''gets property target'''
            if self._target is None:
                self.__init()
            return self._target

        #----------------------------------------------------------------------
        @property
        def received(self):
            '''gets property received'''
            if self._received is None:
                self.__init()
            return self._received

        #----------------------------------------------------------------------
        @property
        def data(self):
            '''gets property data'''
            if self._data is None:
                self.__init()
            return self._data

        #----------------------------------------------------------------------
        @property
        def type(self):
            '''gets property type'''
            if self._type is None:
                self.__init()
            return self._type

        #----------------------------------------------------------------------
        @property
        def id(self):
            '''gets property id'''
            if self._id is None:
                self.__init()
            return self._id
        #----------------------------------------------------------------------
        @property
        def root(self):
            """returns the current url of the class"""
            return self._url
        #----------------------------------------------------------------------
        def __str__(self):
            """returns object as string"""
            if self._json is None:
                self.__init()
            return self._json
        #----------------------------------------------------------------------
        def __iter__(self):
            """returns JSON as [key,value] objects"""
            if self._json_dict is None:
                self.__init()
            for k,v in self._json_dict.items():
                yield [k,v]
        #----------------------------------------------------------------------
        def delete(self):
            """deletes the current notification from the user"""
            url = "%s/delete" % self.root
            params = {"f":"json"}
            return self._post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
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
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Notifications class.")
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns the current url of the class"""
        return self._url
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns JSON as [key,value] objects"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def notifications(self):
        """gets the user's notifications"""
        self.__init()
        items = []
        for n in self._notifications:
            if "id" in n:
                url = "%s/%s" % (self.root, n['id'])
                items.append(self.Notification(url=url,
                                               securityHandler=self._securityHandler,
                                               proxy_url=self._proxy_url,
                                               proxy_port=self._proxy_port))
        return items


