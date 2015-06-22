from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class Security(BaseAGSServer):
    """ The security resource is a container for all resources and
        operations that deal with security for your site. Under this
        resource, you will find resources that represent the users and
        roles in your current security configuration.
        Since the content sent to and from this resource (and operations
        within it) could contain confidential data like passwords, it is
        recommended that this resource be accessed over HTTPS protocol.
    """
    _url = None
    _securityHandler = None
    _resources = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - manages site security
               username - admin username
               password - admin password
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented."
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """ returns the resources """
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    def addRole(self, name, description=""):
        """ Adds a role to the role store. This operation is available only
            when the role store is a read-write store such as the default
            ArcGIS Server store.
            If the name of the role exists in the role store, an error will
            be returned.
            Input:
               name - The name of the role. The name must be unique in the
                      role store.
               description - An optional field to add comments or a
                             description for the role.
            Output:
               JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "name" : name,
            "description" : description
        }
        aURL = self._url + "/roles/add"
        return self._do_post(url=aURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def addUser(self, username, password,
                fullname=None, description=None, email=None):
        """ Add a user account to the user store
           Input:
              username - The name of the user. The name must be unique in
                         the user store.
              password - The password for this user
              fullname - an optional full name for the user
              description - an option field to add comments or description
                            for the user account
              email - an optional email for the user account
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username,
            "password" : password,
        }
        if fullname is not None:
            params['fullname'] = fullname
        if description is not None:
            params['description'] = description
        if email is not None:
            params['email'] = email
        aURL = self._url + "/users/add"
        return self._do_post(url=aURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def addUsersToRole(self, rolename, users):
        """ Assigns a role to multiple users """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "rolename" : rolename,
            "users" : users
        }
        rURL = self._url + "/roles/addUsersToRole"
        return self._do_post(url=rURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def assignPrivilege(self, rolename, privilege="ACCESS"):
        """
           Administrative access to ArcGIS Server is modeled as three broad
           tiers of privileges:
               ADMINISTER - A role that possesses this privilege has
                           unrestricted administrative access to ArcGIS
                          Server.
               PUBLISH - A role with PUBLISH privilege can only publish GIS
                       services to ArcGIS Server.
               ACCESS-No administrative access. A role with this privilege
                      can only be granted permission to access one or more
                      GIS services.
           By assigning these privileges to one or more roles in the role
           store, ArcGIS Server's security model supports role-based access
           control to its administrative functionality.
           These privilege assignments are stored independent of ArcGIS
           Server's role store. As a result, you don't need to update your
           enterprise identity stores (like Active Directory).
           Inputs:
              rolename - The name of the role.
              privilege - The capability to assign to the role. The default
                          capability is ACCESS.
                          Values: ADMINISTER | PUBLISH | ACCESS
           Output:
              JSON Message
        """
        aURL = self._url + "/roles/assignPrivilege"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "rolename" : rolename,
            "privilege" : privilege
        }
        return self._do_post(url=aURL,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def assignRoles(self, username, roles):
        """
           You must use this operation to assign roles to a user account
           when working with an user and role store that supports reads and
           writes.
           By assigning a role to a user, the user account automatically
           inherits all the permissions that have been assigned to the role
           Inputs:
              username - The name of the user.
              roles - A comma-separated list of role names. Each of role
                      names must exist in the role store.
           Output:
              returns JSON messages
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username,
            "roles" : roles
        }
        uURL = self._url + "/users/assignRoles"
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def disablePrimarySiteAdministrator(self):
        """
           You can use this operation to disable log in privileges for the
           primary site administrator account. This operation can only be
           invoked by an administrator in the system. To re-enable this
           account, use the Enable Primary Site Administrator operation.
        """
        dURL = self._url + "/psa/disable"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=dURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def enablePrimarySiteAdministrator(self):
        """
           You can use this operation to enable log in privileges for the
           primary site administrator account. This operation can only be
           invoked by an another administrator in the system.
           However, if you did not have any other administrators in the
           system and accidentally disabled the primary site administrator
           account, you can re-enable the account by running the password
           reset utility. This utility is shipped in <ArcGIS Server
           installation directory>//Server//tools//passwordreset. Use the -e
           option to re-enable the primary site administrator. This utility
           is described in more detail in the ArcGIS Server Help.
        """
        eURL = self._url + "/psa/enable"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=eURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getPrivilegeForRole(self, rolename):
        """
           Returns the privilege associated with a role.
           Input:
              rolename - name of the role
           Output:
              JSON Messages
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "rolename" : rolename
        }
        pURL = self._url + "/roles/getPrivilege"
        return self._do_post(url=pURL,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getPrivilegeForUser(self, username):
        """
           Returns the privilege associated with a user
           Input:
              username - name of the user
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username
        }
        url = self._url + "/users/getPrivilege"
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getRoles(self, startIndex=0, pageSize=10):
        """ This operation gives you a pageable view of roles in the role
            store. It is intended for iterating through all available role
            accounts. To search for specific role accounts instead, use the
            Search Roles operation.
            Inputs:
               startIndex - The starting index (zero-based) from the roles
                            list that must be returned in the result page.
                            The default is 0.
               pageSize - The maximum number of roles to return in the
                          result page. The default size is 10.
            Output:
               returns JSON messages as dictionary
        """
        uURL = self._url + "/roles/getRoles"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "startIndex" : startIndex,
            "pageSize" : pageSize
        }
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getRolesByPrivilege(self, privilege):
        """
           Returns the roles associated with a pribilege.
           Input:
              privilege - name of the privilege
           Output:
              JSON response as dictionary
        """
        uURL = self._url + "/roles/getRolesByPrivilege"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "privilege" : privilege
        }
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getRolesForUser(self, username, filter=None, maxCount=None):
        """
           This operation returns a list of role names that have been
           assigned to a particular user account.
           Inputs:
              username - name of the user for whom the returned roles
              filter - filter to be applied to the resultant role set.
              maxCount - maximum number of results to return for this query
        """
        uURL = self._url + "/roles/getRolesForUser"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username
        }
        if filter is not None:
            params['filter'] = filter

        if maxCount is not None:
            params['maxCount'] = maxCount
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getUsers(self, startIndex=0, pageSize=10):
        """
           This operation gives you a pageable view of users in the user
           store. It is intended for iterating over all available user
           accounts. To search for specific user accounts instead, use the
           Search Users operation.
           Inputs:
              startIndex - The starting index (zero-based) from the users
                           list that must be returned in the result page.
                           The default is 0.
              pageSize - The maximum number of user accounts to return in
                         the result page.
           Output:
              JSON response message as dictionary
        """
        uURL = self._url + "/users/getUsers"
        params={
            "f" : "json",
            "token" : self._securityHandler.token,
            "startIndex" : startIndex,
            "pageSize" : pageSize
        }
        return self._do_post(url=uURL,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getUsersWithinRole(self, rolename, filter=None, maxCount=20):
        """
           You can use this operation to conveniently see all the user
           accounts to whom this role has been assigned.
           Inputs:
              rolename - name of the role
              filter - filter to be applied to the resultant user set
              maxCount - maximum number of results to return
           Output:
              JSON Message as dictionary
        """
        uURL = self._url + "/roles/getUsersWithinRole"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "rolename" : rolename,
            "maxCount" : maxCount
        }
        if filter is not None and \
           isinstance(filter, str):
            params['filter'] = filter
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def primarySiteAdministrator(self):
        """ returns if the primary site admin has been disabled """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/psa"
        return self._do_get(url=uURL, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeRole(self, rolename):
        """
           Removes an existing role from the role store. This operation is
           available only when the role store is a read-write store such as
           the default ArcGIS Server store.
           Input:
              rolename - name of role to remove
           Output:
              JSON message if any
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "rolename" : rolename
        }
        uURL = self._url + "/roles/remove"
        return self._do_post(url=uURL,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeRoles(self, username, roles):
        """
           This operation removes roles that have been previously assigned
           to a user account. This operation is supported only when the
           user and role store supports reads and writes.
           Inputs:
              username - name of the user
              roles - comma seperated list of the role names
           Ouput:
              JSON Messages as dictionary
        """
        uURL = self._url + "/users/removeRoles"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username,
            "roles" : roles
        }
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUser(self, username):
        """
           returns a username from the user store
           Inputs:
              username - name of the user to remove
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : 'json',
            "token" : self._securityHandler.token,
            "username" : username
        }
        uURL = self._url + "/users/remove"
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUsersFromRole(self, rolename, users):
        """
           Removes a role assignment from multiple users.
           Inputs:
              rolename - name of the rolename
              users - comma seperated list of usernames.  They must exist
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : 'json',
            "token" : self._securityHandler.token,
            "rolename" : rolename,
            "users" : users
        }
        uURL = self._url + "/roles/removeUsersFromRole"
        return self._do_post(url=uURL, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def roles(self):
        """
           returns the number of roles for AGS
        """
        params = {
        "f" : "json",
        "token" : self._securityHandler.token
        }
        uURL = self._url + "/roles"
        return self._do_get(url=uURL, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def searchRoles(self, filter="", maxCount=""):
        """
           You can use this operation to search a specific role or a group
           of roles from the role store. The size of the search results can
           be controlled with the maxCount parameter.
           Inputs:
              filter - a filter string to search for the roles
              maxCount - maximum size of the result
           Ouput:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "filter" : filter,
            "maxCount" : maxCount
        }
        uURL = self._url + "/roles/search"
        return self._do_get(url=uURL, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def searchUsers(self, filter="", maxCount=""):
        """
           You can use this operation to search a specific user or a group
           of users from the user store. The size of the search result can
           be controlled with the maxCount parameter.
           Inputs:
              filter - a filter string to search for the users
              maxCount - maximum size of the result
           Ouput:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "filter" : filter,
            "maxCount" : maxCount
        }
        uURL = self._url + "/users/search"
        return self._do_get(url=uURL, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)