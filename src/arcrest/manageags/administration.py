"""
   Python tools for access ArcGIS Servers' REST API.
   Use at you own risk.  This package can be dangerous.
"""

from .._abstract.abstract import BaseAGSServer
from datetime import datetime
import csv, os
########################################################################
class ArcGISServerSite(BaseAGSServer):
    """ instance of arcgis server admin pages """
    _securityHandler = None
    _url = None
    _acceptLanguage = None
    _currentVersion = None
    _resources = None
    _fullVersion = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - manages AGS' site security
               username - admin username
               password - admin password
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        #if not securityHandler is None:
        #    self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def log(self):
        """ returns the log object for server """
        return Log(url=self._url + "/logs",
                   securityHandler=self._securityHandler,
                   proxy_port=self._proxy_port,
                   proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def services(self):
        """ gets the object that works on services """
        return Services(url=self._url + "/services",
                        securityHandler=self._securityHandler,
                        proxy_port=self._proxy_port,
                        proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def security(self):
        """ returns the class that works on the site security """
        return Security(url=self._url + "/security",
                        securityHandler=self._securityHandler,
                        proxy_port=self._proxy_port,
                        proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def info(self):
        """ returns the class info that gives information about AGS """
        return Info(url=self._url + "/info",
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def kml(self):
        """ returns the KML class """
        return KML(url=self._url + "/kml",
                   securityHandler=self._securityHandler,
                   initialize=False,
                   proxy_port=self._proxy_port,
                   proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def data(self):
        """ returns the operations that work on the data store """
        return Data(url=self._url + "/data",
                    securityHandler=self._securityHandler,
                    proxy_port=self._proxy_port,
                    proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def uploads(self):
        """ returns the Uploads class that handles uploaded items """
        return Uploads(url=self._url + "/uploads",
                       securityHandler=self._securityHandler,
                       proxy_url=self._proxy_url,
                       proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    @property
    def acceptLanguage(self):
        if self._acceptLanguage is None:
            self.__init()
        return self._acceptLanguage
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """ gets all the resources for the server """
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    @property
    def fullVersion(self):
        """ returns the full version of ags"""
        if self._fullVersion is None:
            self.__init()
        return self._fullVersion
    #----------------------------------------------------------------------
    @property
    def machines(self):
        """ returns the machine information for a server instace"""
        mURL = self._url + "/machines"
        return Machines(url=mURL,
                        securityHandler=self._securityHandler,
                        initialize=False,
                        proxy_port=self._proxy_port,
                        proxy_url=self._proxy_url)

    @property
    def clusters(self):
        """ returns information about the current cluster """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        cURL = self._url + "/clusters"
        return self._do_get(url=cURL, param_dict=params)
    @property
    def folders(self):
        """ returns a list of folders on AGS """
        cURL = self._url + "/services"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }

        return self._do_get(url=cURL, param_dict=params)['folders']
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
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
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
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
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
        return self._do_post(url=aURL, param_dict=params)
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
        return self._do_post(url=aURL, param_dict=params)
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
        return self._do_post(url=rURL, param_dict=params)
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
                             param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_post(url=dURL, param_dict=params)
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
           installation directory>\Server\tools\passwordreset. Use the -e
           option to re-enable the primary site administrator. This utility
           is described in more detail in the ArcGIS Server Help.
        """
        eURL = self._url + "/psa/enable"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=eURL, param_dict=params)
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
                             param_dict=params)
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
        return self._do_post(url=url, param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
                             param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    @property
    def primarySiteAdministrator(self):
        """ returns if the primary site admin has been disabled """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/psa"
        return self._do_get(url=uURL, param_dict=params)
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
                             param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_post(url=uURL, param_dict=params)
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
        return self._do_get(url=uURL, param_dict=params)
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
        return self._do_get(url=uURL, param_dict=params)
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
        return self._do_get(url=uURL, param_dict=params)
########################################################################
class Services(BaseAGSServer):
    """ returns information about the services on AGS """
    _currentURL = None
    _url = None
    _securityHandler = None
    _folderName = None
    _folders = None
    _foldersDetail = None
    _folderDetail = None
    _webEncrypted = None
    _description = None
    _isDefault = None
    _services = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._currentURL = url
        self._securityHandler = securityHandler
        #if not securityHandler is None:
        #    self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._currentURL,
                                 param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def webEncrypted(self):
        """ returns if the server is web encrypted """
        if self._webEncrypted is None:
            self.__init()
        return self._webEncrypted
    #----------------------------------------------------------------------
    @property
    def folderName(self):
        """ returns current folder """
        return self._folderName
    #----------------------------------------------------------------------
    @folderName.setter
    def folderName(self, folder):
        if folder in self.folders:
            self._currentURL = self._url + "/%s" % folder
            self._services = None
            self._description = None
            self._folderName = None
            self._webEncrypted = None
            self.__init()
            self._folderName = folder
        elif folder == "" or\
             folder == "/":
            self._currentURL = self._url
            self._services = None
            self._description = None
            self._folderName = None
            self._webEncrypted = None
            self.__init()
            self._folderName = folder
    #----------------------------------------------------------------------
    @property
    def folders(self):
        """ returns a list of all folders """
        if self._folders is None:
            self.__init()
        if "/" not in self._folders:
            self._folders.append("/")
        return self._folders
    #----------------------------------------------------------------------
    @property
    def foldersDetail(self):
        """returns the folder's details"""
        if self._foldersDetail is None:
            self.__init()
        return self._foldersDetail
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the decscription """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def isDefault(self):
        """ returns the is default property """
        if self._isDefault is None:
            self.__init()
        return self._isDefault
    #----------------------------------------------------------------------
    @property
    def services(self):
        """ returns the services in the current folder """
        self._services = []
        params = {
                    "f" : "json",
                    "token" : self._securityHandler.token
                }
        json_dict = self._do_get(url=self._currentURL,
                                 param_dict=params)
        if "services" in json_dict.keys():
            for s in json_dict['services']:
                uURL = self._currentURL + "/%s.%s" % (s['serviceName'], s['type'])
                self._services.append(
                    AGSService(url=uURL,
                               securityHandler=self._securityHandler,
                               proxy_url=self._proxy_url,
                               proxy_port=self._proxy_port)
                )
        return self._services
    #----------------------------------------------------------------------
    def find_services(self, service_type="*"):
        """
            returns a list of a particular service type on AGS
            Input:
              service_type - Type of service to find.  The allowed types
                             are: ("GPSERVER", "GLOBESERVER", "MAPSERVER",
                             "GEOMETRYSERVER", "IMAGESERVER",
                             "SEARCHSERVER", "GEODATASERVER",
                             "GEOCODESERVER", "*").  The default is *
                             meaning find all service names.
            Output:
              returns a list of service names as <folder>/<name>.<type>
        """
        allowed_service_types = ("GPSERVER", "GLOBESERVER", "MAPSERVER",
                                 "GEOMETRYSERVER", "IMAGESERVER",
                                 "SEARCHSERVER", "GEODATASERVER",
                                 "GEOCODESERVER", "*")
        lower_types = [l.lower() for l in service_type.split(',')]
        for v in lower_types:
            if v.upper() not in allowed_service_types:
                return {"message" : "%s is not an allowed service type." % v}
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        type_services = []
        folders = self.folders
        folders.append("")
        baseURL = self._url
        for folder in folders:
            if folder == "":
                url = baseURL
            else:
                url = baseURL + "/%s" % folder
            res = self._do_get(url, params)
            if res.has_key("services"):
                for service in res['services']:
                    #if service_type == "*":
                        #service['URL'] = url + "/%s.%s" % (service['serviceName'],
                                                           #service_type)
                        #type_services.append(service)
                    if service['type'].lower() in lower_types:
                        service['URL'] = url + "/%s.%s" % (service['serviceName'],
                                                           service_type)
                        type_services.append(service)
                    del service
            del res
            del folder
        return type_services
    #----------------------------------------------------------------------
    def addFolderPermission(self, principal, isAllowed=True, folder=None):
        """
           Assigns a new permission to a role (principal). The permission
           on a parent resource is automatically inherited by all child
           resources
           Input:
              principal - name of role to assign/disassign accesss
              isAllowed -  boolean which allows access
           Output:
              JSON message as dictionary
        """
        if folder is not None:
            uURL = self._url + "/%s/%s" % (folder, "/permissions/add")
        else:
            uURL = self._url + "/permissions/add"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "principal" : principal,
            "isAllowed" : isAllowed
        }
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def cleanPermsissions(self, principal):
        """
           Cleans all permissions that have been assigned to a role
           (principal). This is typically used when a role is deleted.
           Input:
              principal - name of the role to clean
           Output:
              JSON Message as Dictionary
        """
        uURL = self._url + "/permissions/clean"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "principal" : principal
        }
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def createFolder(self, folderName, description=""):
        """
           Creates a unique folder name on AGS
           Inputs:
              folderName - name of folder on AGS
              description - describes the folder
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "folderName" : folderName,
            "description" : description
        }
        uURL = self._url + "/createFolder"
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def deleteFolder(self, folderName):
        """
           deletes a folder on AGS
           Inputs:
              folderName - name of folder to remove
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
        }
        if folderName in self.folders:
            uURL = self._url + "/%s/delete" % folderName
            return self._do_post(url=uURL, param_dict=params)
        else:
            return {"error" : "folder does not exist"}
    #----------------------------------------------------------------------
    def deleteService(self, serviceName, serviceType, folder=None):
        """
           deletes a service from AGS
           Inputs:
              serviceName - name of the service
              serviceType - type of the service
              folder - name of the folder the service resides, leave None
                       for root.
           Output:
              JSON message as dictionary
        """
        if folder is None:
            uURL = self._url + "/%s.%s/delete" % (serviceName,
                                                  serviceType)
        else:
            uURL = self._url + "/%s/%s.%s/delete" % (folder,
                                                     serviceName,
                                                     serviceType)
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=uURL, param_dict=params)
    def service_report(self, folder=None):
        """
           provides a report on all items in a given folder
           Inputs:
              folder - folder to report on given services. None means root
        """
        items = ["description", "status",
                 "instances", "iteminfo",
                 "properties"]
        if folder is None:
            uURL = self._url + "/report"
        else:
            uURL = self._url + "/%s/report" % folder
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "parameters" : items
        }
        return self._do_get(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    @property
    def types(self):
        """ returns the allowed services types """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/types"
        return self._do_get(url=uURL,
                            param_dict=params)
    #----------------------------------------------------------------------
    def rename_service(self, serviceName, serviceType,
                       serviceNewName, folder=None):
        """
           Renames a published AGS Service
           Inputs:
              serviceName - old service name
              serviceType - type of service
              serviceNewName - new service name
              folder - location of where the service lives, none means
                       root folder.
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "serviceName" : serviceName,
            "serviceType" : serviceType,
            "serviceNewName" : serviceNewName
        }
        if folder is None:
            uURL = self._url + "/renameService"
        else:
            uURL = self._url + "/%s/renameService" % folder
        return self._do_post(url=uURL, param_dict=params)


########################################################################
class Info(BaseAGSServer):
    """
       A read-only resource that returns meta information about the server.
    """
    _url = None
    _securityHandler = None
    _timezone = None
    _loggedInUser = None
    _loggedInUserPrivilege = None
    _currentBuild = None
    _currentVersion = None
    _fullVersion = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def fullVersion(self):
        """ returns the full version """
        if self._fullVersion is None:
            self.__init()
        return self._fullVersion
    #----------------------------------------------------------------------
    @property
    def currentversion(self):
        """ returns the current vesrion """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def loggedInUser(self):
        """ get the logged in user """
        if self._loggedInUser is None:
            self.__init()
        return self._loggedInUser
    #----------------------------------------------------------------------
    @property
    def currentbuild(self):
        """ returns the current build """
        if self._currentBuild is None:
            self.__init()
        return self._currentBuild
    #----------------------------------------------------------------------
    @property
    def timezone(self):
        """ returns the server's defined time zone """
        if self._timezone is None:
            self.__init()
        return self._timezone
    #----------------------------------------------------------------------
    @property
    def loggedInUserPrivilege(self):
        """ gets the logged in user's privileges """
        if self._loggedInUserPrivilege is None:
            self.__init()
        return self._loggedInUserPrivilege
    #----------------------------------------------------------------------
    def getAvailableTimeZones(self):
        """
           Returns an enumeration of all the time zones of which the server
           is aware. This is used by the GIS service publishing tools
        """
        url = self._url + "/getAvailableTimeZones"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url, params)

########################################################################
class Log(BaseAGSServer):
    """ Log of a server """
    _url = None
    _securityHandler = None
    _operations = None
    _resources = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - Handler that handles site security
               username - admin username
               password - admin password
        """
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        self._securityHandler = securityHandler
        #if not securityHandler is None:
        #    self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def operations(self):
        """ returns the operations """
        if self._operations is None:
            self.__init()
        return self._operations
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """ returns the log resources """
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    def countErrorReports(self, machine="*"):
        """ This operation counts the number of error reports (crash
            reports) that have been generated on each machine.
            Input:
               machine - name of the machine in the cluster.  * means all
                         machines.  This is default
            Output:
               dictionary with report count and machine name
        """
        params = {
            "f": "json",
            "token" : self._securityHandler.token,
            "machine" : machine
        }
        return self._do_post(url=self._url + "/countErrorReports",
                            param_dict=params)
    #----------------------------------------------------------------------
    def clean(self):
        """ Deletes all the log files on all server machines in the site.  """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=self._url + "/clean",
                             param_dict=params)
    #----------------------------------------------------------------------
    @property
    def logSettings(self):
        """ returns the current log settings """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        sURL = self._url + "/settings"
        return self._do_get(url=sURL, param_dict=params)['settings']
    #----------------------------------------------------------------------
    def editLogSettings(self,
                        logLevel="WARNING",
                        logDir=None,
                        maxLogFileAge=90,
                        maxErrorReportsCount=10):
        """
           The log settings are for the entire site.
           Inputs:
             logLevel -  Can be one of [OFF, SEVERE, WARNING, INFO, FINE,
                         VERBOSE, DEBUG].
             logDir - File path to the root of the log directory
             maxLogFileAge - number of days that a server should save a log
                             file.
             maxErrorReportsCount - maximum number of error report files
                                    per machine
        """
        lURL = self._url + "/settings/edit"
        allowed_levels =  ("OFF", "SEVERE", "WARNING", "INFO", "FINE", "VERBOSE", "DEBUG")
        currentSettings= self.logSettings
        currentSettings["f"] ="json"
        currentSettings["token"] = self._securityHandler.token

        if logLevel.upper() in allowed_levels:
            currentSettings['logLevel'] = logLevel.upper()
        if logDir is not None:
            currentSettings['logDir'] = logDir
        if maxLogFileAge is not None and \
           isinstance(maxLogFileAge, int):
            currentSettings['maxLogFileAge'] = maxLogFileAge
        if maxErrorReportsCount is not None and \
           isinstance(maxErrorReportsCount, int) and\
           maxErrorReportsCount > 0:
            currentSettings['maxErrorReportsCount'] = maxErrorReportsCount
        return self._do_post(url=lURL, param_dict=currentSettings)
    #----------------------------------------------------------------------
    def query(self,
              startTime=None,
              endTime=None,
              sinceServerStart=False,
              level="WARNING",
              services="*",
              machines="*",
              server="*",
              codes=[],
              processIds=[],
              export=False,
              exportType="CSV", #CSV or TAB
              out_path=None
              ):
        """
           The query operation on the logs resource provides a way to
           aggregate, filter, and page through logs across the entire site.
           Inputs:

        """
        allowed_levels = ("SEVERE", "WARNING", "INFO",
                          "FINE", "VERBOSE", "DEBUG")
        qFilter = {
            "services": "*",
            "machines": "*",
            "server" : "*"
        }
        if len(processIds) > 0:
            qFilter['processIds'] = processIds
        if len(codes) > 0:
            qFilter['codes'] = codes
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "sinceServerStart" : sinceServerStart,
            "pageSize" : 10000
        }
        if startTime is not None and \
           isinstance(startTime, datetime):
            params['startTime'] = startTime.strftime("%Y-%m-%dT%H:%M:%S")
        if endTime is not None and \
           isinstance(endTime, datetime):
            params['endTime'] = endTime.strftime("%Y-%m-%dT%H:%M:%S")
        if level.upper() in allowed_levels:
            params['level'] = level
        if server != "*":
            qFilter['server'] = server.split(',')
        if services != "*":
            qFilter['services'] = services.split(',')
        if machines != "*":
            qFilter['machines'] = machines.split(",")
        params['filter'] = qFilter
        if export == True and \
           out_path is not None:
            messages = self._do_post(self._url + "/query", params)

            with open(name=out_path, mode='wb') as f:
                hasKeys = False
                if exportType == "TAB":
                    csvwriter = csv.writer(f, delimiter='\t')
                else:
                    csvwriter = csv.writer(f)
                for message in messages['logMessages']:
                    if hasKeys == False:
                        csvwriter.writerow(message.keys())
                        hasKeys = True
                    csvwriter.writerow(message.values())
                    del message
            del messages
            return out_path
        else:
            return self._do_post(self._url + "/query", params)

########################################################################
class AGSService(BaseAGSServer):
    """ Defines a AGS Admin Service """
    _proxy_port = None
    _proxy_url = None
    _securityHandler = None
    _recycleInterval = None
    _instancesPerContainer = None
    _maxWaitTime = None
    _extensions = None
    _minInstancesPerNode = None
    _maxIdleTime = None
    _maxUsageTime = None
    _allowedUploadFileTypes = None
    _datasets = None
    _properties = None
    _recycleStartTime = None
    _clusterName = None
    _description = None
    _isDefault = None
    _type = None
    _serviceName = None
    _isolationLevel = None
    _capabilities = None
    _loadBalancing = None
    _configuredState = None
    _maxStartupTime = None
    _private = None
    _maxUploadFileSize = None
    _keepAliveInterval = None
    _maxInstancesPerNode = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - manages site security
               proxy_url - url of proxy
               proxy_port - port value of proxy
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._currentURL = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._currentURL,
                                 param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    @property
    def recycleInterval(self):
        if self._recycleInterval is None:
            self.__init()
        return self._recycleInterval
    @property
    def instancesPerContainer(self):
        if self._instancesPerContainer is None:
            self.__init()
        return self._instancesPerContainer
    @property
    def maxWaitTime(self):
        if self._maxWaitTime is None:
            self.__init()
        return self._maxWaitTime
    @property
    def extensions(self):
        if self._extensions is None:
            self.__init()
        return self._extensions
    @property
    def minInstancesPerNode(self):
        if self._minInstancesPerNode is None:
            self.__init()
        return self._minInstancesPerNode
    @property
    def maxIdleTime(self):
        if self._maxIdleTime is None:
            self.__init()
        return self._maxIdleTime
    @property
    def maxUsageTime(self):
        if self._maxUsageTime is None:
            self.__init()
        return self._maxUsageTime
    @property
    def allowedUploadFileTypes(self):
        if self._allowedUploadFileTypes is None:
            self.__init()
        return self._allowedUploadFileTypes
    @property
    def datasets(self):
        if self._datasets is None:
            self.__init()
        return self._datasets
    @property
    def properties(self):
        if self._properties is None:
            self.__init()
        return self._properties
    @property
    def recycleStartTime(self):
        if self._recycleStartTime is None:
            self.__init()
        return self._recycleStartTime
    @property
    def clusterName(self):
        if self._clusterName is None:
            self.__init()
        return self._clusterName
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    @property
    def isDefault(self):
        if self._isDefault is None:
            self.__init()
        return self._isDefault
    @property
    def type(self):
        if self._type is None:
            self.__init()
        return self._type
    @property
    def maxUploadFileSize(self):
        if self._maxUploadFileSize is None:
            self.__init()
        return self._maxUploadFileSize
    @property
    def keepAliveInterval(self):
        if self._keepAliveInterval is None:
            self.__init()
        return self._keepAliveInterval
    @property
    def maxInstancesPerNode(self):
        if self._maxInstancesPerNode is None:
            self.__init()
        return self._maxInstancesPerNode
    @property
    def private(self):
        if self._private is None:
            self.__init()
        return self._private
    @property
    def maxStartupTime(self):
        if self._maxStartupTime is None:
            self.__init()
        return self._maxStartupTime
    @property
    def loadBalancing(self):
        if self._loadBalancing is None:
            self.__init()
        return self._loadBalancing
    @property
    def configuredState(self):
        if self._configuredState is None:
            self.__init()
        return self._configuredState
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    @property
    def isolationLevel(self):
        if self._isolationLevel is None:
            self.__init()
        return self._isolationLevel
    @property
    def serviceName(self):
        if self._serviceName is None:
            self.__init()
        return self._serviceName
    #----------------------------------------------------------------------
    def start_service(self):
        """ starts the specific service """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/start"
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def stop_service(self):
        """ stops the current service """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/stop"
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def restart_services(self):
        """ restarts the current service """
        self.stop_service()
        self.start_service()
        return {'status': 'success'}
    @property
    def status(self):
        """ returns the status of the service """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/status"
        return self._do_get(url=uURL, param_dict=params)
    @property
    def statistics(self):
        """ returns the stats for the service """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/statistics"
        return self._do_get(url=uURL, param_dict=params)
    @property
    def permissions(self):
        """ returns the permissions for the service """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/permissions"
        return self._do_get(url=uURL, param_dict=params)
    @property
    def iteminfo(self):
        """ returns the item information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/iteminfo"
        return self._do_get(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def addPermission(self, principal, isAllowed=True):
        """
           Assigns a new permission to a role (principal). The permission
           on a parent resource is automatically inherited by all child
           resources.
           Inputs:
              principal - role to be assigned
              isAllowed - access of resource by boolean
           Output:
              JSON message as dictionary
        """
        uURL = self._url + "/permissions/add"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "principal" : principal,
            "isAllowed" : isAllowed
        }
        return self._do_post(url=uURL, param_dict=params)
########################################################################
class Machines(BaseAGSServer):
    """
       his resource represents a collection of all the server machines that
       have been registered with the site. It other words, it represents
       the total computing power of your site. A site will continue to run
       as long as there is one server machine online.
       For a server machine to start hosting GIS services, it must be
       grouped (or clustered). When you create a new site, a cluster called
       'default' is created for you.
       The list of server machines in your site can be dynamic. You can
       register additional server machines when you need to increase the
       computing power of your site or unregister them if you no longer
       need them.
    """
    _machines = None
    _proxy_port = None
    _proxy_url = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - manages site security
               initialize - loads the machine information
               proxy_url - proxy server web address
               proxy_port - proxy server port
        """
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url,
                                 param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k == "machines":
                self._machines = []
                for m in v:
                    self._machines.append(
                        Machine(url=self._url +"/%s" % m['machineName'],
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
                    )
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented for Machines"
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def machines(self):
        """  returns the list of machines in the cluster """
        if self._machines is None:
            self.__init()
        return self._machines
    #----------------------------------------------------------------------
    def registerMachine(self, machineName, adminURL):
        """
           For a server machine to participate in a site, it needs to be
           registered with the site. The server machine must have ArcGIS
           Server software installed and authorized.
           Registering machines this way is a "pull" approach to growing
           the site and is a convenient way when a large number of machines
           need to be added to a site. In contrast, a server machine can
           choose to join a site.
           Inputs:
              machineName - name of the server machine
              adminURL - URL wher ethe Administrator API is running on the
                         server machine.
                         Example: http://<machineName>:6080/arcgis/admin
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "machineName" : machineName,
            "adminURL" : adminURL
        }
        uURL = "%s/register" % self._url
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def renameMachine(self, machineName, newMachineName):
        """
           You must use this operation if one of the registered machines
           has undergone a name change. This operation updates any
           references to the former machine configuration.
           By default, when the server is restarted, it is capable of
           identifying a name change and repairing itself and all its
           references. This operation is a manual call to handle the
           machine name change.
           Input:
              machineName - The former name of the server machine that is
                            registered with the site.
              newMachineName - The new name of the server machine.
           Output:
              JSON messages as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "machineName" : machineName,
            "newMachineName" : newMachineName
        }
        uURL = self._url + "/rename"
        return self._do_post(url=uURL, param_dict=params)
########################################################################
class Machine(BaseAGSServer):
    """
       A server machine represents a machine on which ArcGIS Server
       software has been installed and licensed. A site is made up one or
       more of such machines that work together to host GIS services and
       data and provide administrative capabilities for the site. Each
       server machine is capable of performing all these tasks and hence a
       site can be thought of as a distributed peer-to-peer network of such
       machines.
       A server machine communicates with its peers over a range of TCP and
       UDP ports that can be configured using the edit operation. For a
       server machine to host GIS services, it needs to be added to a
       cluster. Starting and stopping the server machine enables and
       disables, respectively, its ability to host GIS services.
       The administrative capabilities of the server machine are available
       through the ArcGIS Server Administrator API that can be accessed
       over HTTP(S). For a server machine to participate in a site, it must
       be registered with the site. A machine can participate in only one
       site at a time. To remove a machine permanently from the site, you
       can use the unregister operation.
    """
    _appServerMaxHeapSize = None
    _webServerSSLEnabled = None
    _webServerMaxHeapSize = None
    _platform = None
    _adminURL = None
    _machineName = None
    _ServerStartTime = None
    _webServerCertificateAlias = None
    _socMaxHeapSize = None
    _synchronize = None
    _configuredState = None
    _ports = None
    _proxy_port = None
    _proxy_url = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - handles site security
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._currentURL = url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._currentURL,
                                 param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented for Machine"
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def appServerMaxHeapSize(self):
        """ returns the app server max heap size """
        if self._appServerMaxHeapSize is None:
            self.__init()
        return self._appServerMaxHeapSize
    #----------------------------------------------------------------------
    @property
    def webServerSSLEnabled(self):
        """ SSL enabled """
        if self._webServerSSLEnabled is None:
            self.__init()
        return self._webServerSSLEnabled
    #----------------------------------------------------------------------
    @property
    def webServerMaxHeapSize(self):
        """ returns the web server max heap size """
        if self._webServerMaxHeapSize is None:
            self.__init()
        return self._webServerMaxHeapSize
    #----------------------------------------------------------------------
    @property
    def platform(self):
        """ returns the platform information """
        if self._platform is None:
            self.__init()
        return self._platform
    #----------------------------------------------------------------------
    @property
    def adminURL(self):
        """ returns the administration URL """
        if self._adminURL is None:
            self.__init()
        return self._adminURL
    #----------------------------------------------------------------------
    @property
    def machineName(self):
        """ returns the machine name """
        if self._machineName is None:
            self.__init()
        return self._machineName
    #----------------------------------------------------------------------
    @property
    def ServerStartTime(self):
        """ returns the server start date/time """
        if self._ServerStartTime is None:
            self.__init()
        return self._ServerStartTime
    #----------------------------------------------------------------------
    @property
    def webServerCertificateAlias(self):
        """ returns the webserver cert alias"""
        if self._webServerCertificateAlias is None:
            self.__init()
        return self._webServerCertificateAlias
    #----------------------------------------------------------------------
    @property
    def socMaxHeapSize(self):
        """ returns the soc's max heap size """
        if self._socMaxHeapSize is None:
            self.__init()
        return self._socMaxHeapSize
    #----------------------------------------------------------------------
    @property
    def synchronize(self):
        """synchronize value"""
        if self._synchronize is None:
            self.__init()
        return self._synchronize
    #----------------------------------------------------------------------
    @property
    def ports(self):
        """ returns the used ports """
        if self._ports is None:
            self.__init()
        return self._ports
    #----------------------------------------------------------------------
    @property
    def configuredState(self):
        """ returns the configured state """
        if self._configuredState is None:
            self.__init()
        return self._configuredState
    #----------------------------------------------------------------------
    @property
    def status(self):
        """ returns the state """
        uURL = self._url + "/status"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def startMachine(self):
        """ Starts the server machine """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/start"
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def stopMachine(self):
        """ Stops the server machine """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/stop"
        return self._do_post(url=uURL, param_dict=params)
    #----------------------------------------------------------------------
    def unregisterMachine(self):
        """
           This operation causes the server machine to be deleted from the
           Site.
           The server machine will no longer participate in the site or run
           any of the GIS services. All resources that were acquired by the
           server machine (memory, files, and so forth) will be released.
           Typically, you should only invoke this operation if the machine
           is going to be shut down for extended periods of time or if it
           is being upgraded.
           Once a machine has been unregistered, you can create a new site
           or join an existing site.
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        uURL = self._url + "/start"
        return self._do_post(url=uURL, param_dict=params)
########################################################################
class Data(BaseAGSServer):
    """
       This resource provides information about the data holdings of the
       server. This information is used by ArcGIS for Desktop and other
       clients to validate data paths referenced by GIS services.
       You can register new data items with the server by using the
       Register Data Item operation. Use the Find Data Items operation to
       search through the hierarchy of data items.
       The Compute Ref Count operation counts and lists all references to a
       specific data item. This operation helps you determine if a
       particular data item can be safely deleted or refreshed.
    """
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - handles site security
        """
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url

    #----------------------------------------------------------------------
    @property
    def datastoreConfiguration(self):
        """
           The data store configuration properties affect the behavior of
           the data holdings of the server. The properties include:
           blockDataCopy - When this property is false, or not set at all,
           copying data to the site when publishing services from a client
           application is allowed. This is the default behavior. When this
           property is true, the client application is not allowed to copy
           data to the site when publishing. Rather, the publisher is
           required to register data items through which the service being
           published can reference data. Values: true | false
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        dURL = self._url + "/config"
        return self._do_get(url=dURL, param_dict=params)
    #----------------------------------------------------------------------
    def updateDatastoreConfiguration(self, datastoreConfig={}):
        """
           This operation allows you to update the data store configuration
           You can use this to allow or block the automatic copying of data
           to the server at publish time
           Input:
              datastoreConfig - the JSON object containing the data
                                configuration
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "datastoreConfig" : datastoreConfig
        }
        url = self._url + "/config/update"
        return self._do_post(url=url, param_dict=params)
    #----------------------------------------------------------------------
    def computeTotalRefCount(self, path):
        """
           Computes the total number of references to a given data item
           that exist on the server. You can use this operation to
           determine if a data resource can be safely deleted (or taken
           down for maintenance).
           Input:
              path - The complete hierarchical path to the item
           Output:
              JSON message as dictionary
        """
        cURL = self._url + "/computeTotalRefCount"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "path" : path
        }
        return self._do_post(url=cURL,
                             param_dict=params)
    #----------------------------------------------------------------------
    def findDataItems(self, parentPath, ancestorPath=None,
                      type=None, id=None):
        """
           You can use this operation to search through the various data
           items registered in the server's data store.
           Inputs:
              parentPath - The path of the parent under which to find items
              ancestorPath - The path of the ancestor under which to find
                             items.
              type - A filter for the type of the items
              id - A filter to search by the ID of the item
           Output:
              dictionary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "parentPath" : parentPath
        }
        if ancestorPath is not None:
            params['ancestorPath'] = ancestorPath
        if type is not None:
            params['type'] = type
        if id is not None:
            params['id'] = id
        fURL = self._url + "/findItems"
        return self._do_post(url=fURL, param_dict=params)
    #----------------------------------------------------------------------
    def registerDataItem(self, item):
        """
           Registers a new data item with the server's data store.
           Input
              item - The JSON representing the data item.
                     See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r3000001s9000000
           Output:
              dictionary
        """
        params = {
            "item" : item,
            "f" : "json",
            "token" : self._securityHandler.token
        }
        rURL = self._url + "/registerItem"
        return self._do_post(url=rURL, param_dict=params)
    #----------------------------------------------------------------------
    @property
    def rootDataItems(self):
        """ This resource lists data items that are the root of all other
            data items in the data store.
        """
        url = self._url + "/items"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params)
    #----------------------------------------------------------------------
    @property
    def validateAllDataItems(self):
        """ validates all the items in the datastore """
        params = {
        "f" : "json",
        "token": self._securityHandler.token}
        url = self._url + "/validateAllDataItems"
        return self._do_get(url=url, param_dict=params)
    #----------------------------------------------------------------------
    def validateDataItem(self, item):
        """
           In order for a data item to be registered and used successfully
           within the server's data store, you need to make sure that the
           path (for file shares) or connection string (for databases) is
           accessible to every server node in the site. This can be done by
           invoking the Validate Data Item operation on the JSON object
           representing the data store.
           Validating a data item does not automatically register it for
           you. You need to explicitly register your data item by invoking
           the Register Data Item operation.
           Input:
              item - The JSON representing the data item.
           Output:
              dicationary
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "item" : item
        }
        url = self._url + "/ validateDataItem"
        return self._do_post(url=url,
                             param_dict=params)
########################################################################
class KML(BaseAGSServer):
    """
       This resource is a container for all the KMZ files created on the
       server.
    """
    _securityHandler = None
    _items = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - handles site security
        """
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        json_dict = self._do_get(url=self._url,
                                 param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented for KML"
            del k
            del v
    #----------------------------------------------------------------------
    def createKMZ(self, kmz_as_json):
        """
           Creates a KMZ file from json.
           See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Create_Kmz/02r3000001tm000000/
           for more information.
        """
        kmlURL = self._url + "/createKmz"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "kml" : kmz_as_json
        }
        return self._do_post(url=kmlURL, param_dict=params)
    #----------------------------------------------------------------------
    @property
    def items(self):
        """ returns list of KMZ/KML on server """
        if self._items is None:
            self.__init()
        return self._items

########################################################################
class Uploads(BaseAGSServer):
    """
    This resource is a collection of all the items that have been uploaded
    to the server.
    See: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Uploads/02r3000001qr000000/
    """
    _uploads = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None):
        """Constructor"""
        if url.lower().find("uploads") < -1:
            self._url = url + "/uploads"
        else:
            self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    @property
    def uploads(self):
        """
        returns a collection of all the items that have been uploaded to
        the server.
        """
        params = {
            "f" :"json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=self._url,
                            param_dict=params,
                            header={},
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    def deleteItem(self, itemId):
        """
           Deletes the uploaded item and its configuration.
           Inputs:
              itemId - unique ID of the item
        """
        url = self._url + "/%s/delete" % itemId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def item(self, itemId):
        """
        This resource represents an item that has been uploaded to the
        server. Various workflows upload items and then process them on the
        server. For example, when publishing a GIS service from ArcGIS for
        Desktop or ArcGIS Server Manager, the application first uploads the
        service definition (.SD) to the server and then invokes the
        publishing geoprocessing tool to publish the service.
        Each uploaded item is identified by a unique name (itemID). The
        pathOnServer property locates the specific item in the ArcGIS
        Server system directory.
        The committed parameter is set to true once the upload of
        individual parts is complete.
        """
        url = self._url + "/%s" % itemId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def uploadItem(self, filePath, description):
        """"""
        import urlparse
        url = self._url + "/upload"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        files = []
        files.append(('itemFile', filePath, os.path.basename(filePath)))
        parsed = urlparse.urlparse(url)
        return self._post_multipart(host=parsed.hostname,
                                       selector=parsed.path,
                                       files = files,
                                       fields=params,
                                       port=parsed.port,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url)




