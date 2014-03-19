from datetime import datetime
import httplib
import urlparse
import urllib
import urllib2
import json
import csv
import os
########################################################################
class BaseAGSServer(object):
    """ base class from which all service inherit """
    _username = None
    _password = None
    _token = None
    _url = None
    _token_url = None
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value
    @property
    def token_url(self):
        """ gets the token url"""
        return self._token_url
    @token_url.setter
    def token_url(self, value):
        """ sets the service's token url"""
        self._token_url = value
    def _reset(self):
        """ resets the class all values to None """
        self._url = None
        self._token = None
        self._username = None
        self._password = None
    @property
    def password(self):
        """ password is never returned """
        return "*******"
    @password.setter
    def password(self, value):
        """ sets the password """
        self._password = value
    @property
    def username(self):
        """ gets the username """
        return self._username
    @username.setter
    def username(self, value):
        """ sets the username """
        self._username = value
    #----------------------------------------------------------------------
    def _download_file(self, url, save_path, file_name):
        """ downloads a file """
        file_data = urllib2.urlopen(url)
        with open(save_path + os.sep + file_name, 'wb') as writer:
            writer.write(file_data.read())
        return save_path + os.sep + file_name    
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict):
        """ performs the POST operation and returns dictionary result """
        request = urllib2.Request(url, urllib.urlencode(param_dict))
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres) 
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header={}):
        """ performs a get operation """
        url = url + "?%s" % urllib.urlencode(param_dict)
        request = urllib2.Request(url, headers=header)
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _post_multipart(self, host, selector, 
                       filename, filetype, 
                       content, fields):
        """ performs a multi-post to AGOL or AGS 
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               filename - string - name file will be called on server
               filetype - string - mimetype of data uploading
               content - binary data - derived from open(<file>, 'rb').read()
               fields - dictionary - additional parameters like token and format information
            Output:
               response as string
        """
        body = ''
        for field in fields.keys():
            body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="' + field + '"\r\n\r\n' + fields[field] + '\r\n'
        body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="file"; filename="'
        body += filename + '"\r\nContent-Type: ' + filetype + '\r\n\r\n'
        body = body.encode('utf-8')
        body += content + '\r\n------------ThIs_Is_tHe_bouNdaRY_$--\r\n'
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$')
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()
    #----------------------------------------------------------------------
    def generate_token(self):#, username, password, tokenURL
        """ generates a token for AGS """
        #params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})
        params = urllib.urlencode({'username': self._username,
                                   'password': self._password,
                                   'client': 'requestip',
                                   'f': 'json'})        
        parsed_url = urlparse.urlparse(self._token_url)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        port = parsed_url.port
        if port is None:
            port = 80
        # Connect to URL and post parameters
        if parsed_url.scheme.lower() == "https":
            httpConn = httplib.HTTPSConnection(parsed_url.hostname, port)
        else:
            httpConn = httplib.HTTPConnection(parsed_url.hostname, port)
        httpConn.request("POST", parsed_url.path, params, headers)
        response = httpConn.getresponse()
        data = self._unicode_convert(json.loads(response.read()))
        httpConn.close()        
        del httpConn
        del response
        self._token = data['token']
        return  data['token'], data['expires']
    #----------------------------------------------------------------------
    def _unicode_convert(self, obj):
        """ converts unicode to anscii """
        if isinstance(obj, dict):
            return {self._unicode_convert(key): self._unicode_convert(value) for key, value in obj.iteritems()}
        elif isinstance(obj, list):
            return [self._unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj  

########################################################################
class ArcGISServer(BaseAGSServer):
    """ instance of arcgis server admin pages """
    _token = None
    _token_url = None
    _username = None
    _password = None
    _url = None
    _acceptLanguage = None
    _currentVersion = None
    _resources = None
    _fullVersion = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url, username, password):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self.generate_token()
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._token
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
    #----------------------------------------------------------------------
    @property
    def log(self):
        """ returns the log object for server """
        return Log(url=self._url + "/logs", 
                   token_url=self._token_url, 
                   username=self._username, 
                   password=self._password) 
    #----------------------------------------------------------------------
    @property
    def services(self):
        """ gets the object that works on services """
        return Services(url=self._url + "/services", 
                        token_url=self._token_url, 
                        username=self._username, 
                        password=self._password) 
    #----------------------------------------------------------------------
    @property
    def security(self):
        """ returns the class that works on the site security """
        return Security(url=self._url + "/security", 
                        token_url=self._token_url, 
                        username=self._username, 
                        password=self._password)
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
        params = {
            "f" : "json",
            "token" : self._token
        }
        mURL = self._url + "/machines"
        return self._do_get(url=mURL, param_dict=params)
    @property
    def clusters(self):
        """ returns information about the current cluster """
        params = {
            "f" : "json",
            "token" : self._token
        }
        cURL = self._url + "/clusters"
        return self._do_get(url=cURL, param_dict=params)        
    @property
    def folders(self):
        """ returns a list of folders on AGS """
        cURL = self._url + "/services"
        params = {
            "f" : "json",
            "token" : self._token
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
    _token = None
    _username = None
    _password = None
    _token_url = None
    _resources = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url, username, password):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self.generate_token()
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._token
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
            "token" : self._token
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
            "token" : self._token,
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
            "token" : self._token,
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
               ADMINISTER—A role that possesses this privilege has 
                          unrestricted administrative access to ArcGIS 
                          Server.
               PUBLISH—A role with PUBLISH privilege can only publish GIS 
                       services to ArcGIS Server.
               ACCESS—No administrative access. A role with this privilege 
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token
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
            "token" : self._token
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token
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
            "token" : self._token
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token,
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
            "token" : self._token,
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
        "token" : self._token
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
            "token" : self._token,
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
            "token" : self._token,
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
    _token = None
    _username = None
    _password = None
    _token_url = None
    _folderName = None
    _folders = None
    _folderDetail = None
    _webEncrypted = None
    _description = None
    _isDefault = None
    _services = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url, username, password):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._currentURL = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self.generate_token()
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._token
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
        self.__init()
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
            "token" : self._token
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
########################################################################
class Log(BaseAGSServer):
    """ Log of a server """
    _url = None
    _token = None
    _username = None
    _password = None
    _token_url = None
    _operations = None
    _resources = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url, username, password):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self.generate_token()
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._token
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
            "token" : self._token,
            "machine" : machine
        }
        return self._do_post(url=self._url + "/countErrorReports", 
                            param_dict=params) 
    #----------------------------------------------------------------------
    def clean(self):
        """ Deletes all the log files on all server machines in the site.  """
        params = {
            "f" : "json",
            "token" : self._token
        }
        return self._do_post(url=self._url + "/clean", 
                             param_dict=params)
    #----------------------------------------------------------------------
    @property
    def logSettings(self):
        """ returns the current log settings """
        params = {
            "f" : "json",
            "token" : self._token
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
        currentSettings["token"] = self._token
        
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
        params = {
            "f" : "json",
            "token" : self._token,
            "sinceServerStart" : sinceServerStart,
            "pageSize" : 10000
        }
        if startTime is not None and \
           isinstance(startTime, datetime):
            params['startTime'] = startTime.strftime("%Y-%m-%dT%H:%M:%S")
        if endTime is not None and \
           isinstance(endTime, datetime):
            params['startTime'] = endTime.strftime("%Y-%m-%dT%H:%M:%S")      
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
class GPServer(BaseAGSServer):
    """ Instance of GPServer Object """
    _token = None
    _token_url = None
    _username = None
    _password = None
    _url = None
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
    _configuredState = None
    _loadBalancing = None
    _maxStartupTime = None
    _private = None
    _maxUploadFileSize = None
    _keepAliveInterval = None
    _maxInstancesPerNode = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url, username, password):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self.generate_token()
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",
            "token" : self._token
        }
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self) 
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]          
        for k,v in json_dict.iteritems(): 
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k#, " - attribute not implmented."  
    #----------------------------------------------------------------------
    def start_service(self):
        """ starts the service """
        params = {"f":"json", "token": self._token}
        url = self._url + "/start"
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def stop_service(self):
        """stops a service"""
        params = {"f":"json", "token": self._token}
        url = self._url + "/stop"
        return self._do_post(url, params)        
    #----------------------------------------------------------------------
    def delete_service(self):
        """ deletes the service """
        params = {"f":"json", "token": self._token}
        url = self._url + "/delete"
        return self._do_post(url, params)     
    @property
    def status(self):
        """ returns the service status """
        params = {"f":"json", "token": self._token}
        url = self._url + "/status"
        return self._do_get(url, params)     
    @property 
    def statistics(self):
        """ returns the service statistics """
        params = {"f":"json", "token": self._token}
        url = self._url + "/statistics"
        return self._do_get(url, params)             
    @property 
    def permissions(self):
        """ returns the service permissions """
        params = {"f":"json", "token": self._token}
        url = self._url + "/permissions"
        return self._do_get(url, params)             
    @property
    def itemInfo(self):
        """ returns the service permissions """
        params = {"f":"json", "token": self._token}
        url = self._url + "/iteminfo"
        return self._do_get(url, params)             


if __name__ == "__main__":
    ags = ArcGISServer(url="http://chronus:6080/arcgis/admin", 
                       token_url="http://chronus:6080/arcgis/admin/generateToken", 
                       username="andrew", 
                       password="andrew")
    security = ags.security
    if isinstance(security, Security):
        print security.getUsers()
        print security.getRoles(0,10)
        print security.removeRoles(username="john", roles="publisher")
    else:
        print type(security)