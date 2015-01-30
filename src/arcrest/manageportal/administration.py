"""
The ArcREST API allows you to perform administrative tasks not available in
the Portal for ArcGIS website. The API is organized into resources and
operations. Resources are entities within Portal for ArcGIS that hold some
information and have a well-defined state. Operations act on these
resources and update their information or state. Resources and operations
are hierarchical and have unique universal resource locators (URLs).
"""
from .._abstract.abstract import BaseAGOLClass
from ..security import PortalTokenSecurityHandler
########################################################################
class _Security(BaseAGOLClass):
    """
       The security resource is the root of all the security configurations
       and operations in the portal. Through this resource, you can change
       the identity providers and the authentication mode for your portal.
    """
    _securityHandler = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if securityHandler is None:
            pass
        elif isinstance(securityHandler, PortalTokenSecurityHandler):
            self._securityHandler = securityHandler

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
    #----------------------------------------------------------------------
    def createUser(self,
                   username,
                   password,
                   fullname,
                   email,
                   role="org_user",
                   provider="arcgis",
                   description=""):
        """
        This operation is used to create a new user account in the portal.
        Inputs:
           username - The name of the user account.
           password - The password for the account. This is a required
                      parameter only if the provider is arcgis; otherwise,
                      the password parameter is ignored.
           fullname - The full name for the user account.
           email - The email address for the user account.
           description - An optional description string for the user
                         account.
           role - The role for the user account. The default value is
                  org_user.
                  Values: org_user | org_publisher | org_admin
           provider - The provider for the account. The default value is
                      arcgis.
                      Values: arcgis | webadaptor
        """
        url = self._url + "/users/create"
        params = {
            "f" : "json",
            "token": self._securityHandler.token,
            "username" : username,
            "password" : password,
            "fullname" : fullname,
            "email" : email,
            "role" : role,
            "provider" : provider,
            "description" : description
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateSecurityConfiguration(self,
                                    enableAutomaticAccountCreation=False,
                                    disableServicesDirectory=False
                                    ):
        """
        This operation can be used to update the portal's security settings
        such as whether or not enterprise accounts are automatically
        registered as members of your ArcGIS organization the first time
        they accesses the portal.
        The security configuration is stored as a collection of properties
        in a JSON object. The following properties are supported:
           enableAutomaticAccountCreation
           disableServicesDirectory
        The automatic account creation flag (enableAutomaticAccountCreation)
        determines the behavior for unregistered enterprise accounts the
        first time they access the portal. When the value for this property
        is set to false, first time users are not automatically registered
        as members of your ArcGIS organization, and have the same access
        privileges as other nonmembers. For these accounts to sign in, an
        administrator must register the enterprise accounts using the
        Create User operation.
        The default value for the enableAutomaticAccountCreation property
        is false. When this value is set to true, portal will add
        enterprise accounts automatically as members of your ArcGIS
        organization.
        The disableServicesDirectory property controls whether the HTML
        pages of the services directory should be accessible to the users.
        The default value for this property is false, meaning the services
        directory HTML pages are accessible to everyone.
        """
        url = self._url + "/config/update"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "enableAutomaticAccountCreation": enableAutomaticAccountCreation,
            "disableServicesDirectory" : disableServicesDirectory
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateIdenityStore(self,
                           userPassword,
                           user,
                           userFullnameAttribute,
                           ldapURLForUsers,
                           userEmailAttribute,
                           usernameAttribute,
                           isPasswordEncrypted=False,
                           caseSensitive=True):
        """
        You can use this operation to change the identity provider
        configuration in your portal. When Portal for ArcGIS is first
        installed, it supports token-based authentication using the
        built-in identity store for accounts. To configure your portal to
        connect to your enterprise authentication mechanism, it must be
        configured to use an enterprise identity store such as Windows
        Active Directory or LDAP.

        Inputs:
           userPassword -The password for the domain account, for example,
                         secret.
           isPasswordEncrypted - Indicates if the userPassword property is
                                 an encrypted password or plain text. If
                                 the property is false, the API will
                                 encrypt the password automatically.
           user - A user account with at least read permissions to look up
                  the email addresses and user names of users in your
                  organization. If possible, use an account whose password
                  does not expire.
                  Windows Active Directory example: mydomain\\winaccount
                  LDAP example: uid=admin\,ou=system
           userFullnameAttribute - The attribute in Windows Active
                                   Directory or LDAP that contains the full
                                   name of the users, for example, cn.
           ldapURLForUsers - The URL to your LDAP that points to the user
                             accounts, for example,
                             ldap://bar2:10389/ou=users\,ou=ags\,dc=example\,dc=com.
                             The URL to your LDAP will need to be provided
                             by your LDAP administrator.
                             This property is not applicable when
                             configuring Windows Active Directory.
           userEmailAttribute - The attribute in Windows Active Directory
                                or LDAP that contains the email addresses
                                of the users, for example, email.
           usernameAttribute - The LDAP attribute of the user entry that is
                               to be treated as the user name, for example, cn.
                               This property is not applicable when
                               configuring Windows Active Directory.
           caseSensitive - In the rare case where your Windows Active
                           Directory is configured to be case sensitive,
                           set this property to true.
                           If your LDAP is configured to be case
                           insensitive, set parameter to false.
        """
        url = self._url + "/config/updateIdentityStore"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "userPassword" : userPassword,
            "isPasswordEncrypted" : isPasswordEncrypted,
            "user" : user,
            "userFullnameAttribute": userFullnameAttribute,
            "ldapURLForUsers" : ldapURLForUsers,
            "userEmailAttribute" : userEmailAttribute,
            "usernameAttribute" : usernameAttribute,
            "caseSensitive" : caseSensitive
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateTokenConfiguration(self, sharedKey):
        """
        You can use this operation to change the shared key for the token
        configuration. Shared keys are used to generate tokens and must be
        of a suitable length to ensure strong encryption.

        Input:
           sharedKey - key used to generate token
        """
        url = self._url + "/tokens/update"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "tokenConfig" : {"sharedKey" : sharedKey}
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def tokenConfigurations(self):
        """
        This resource represents the token configuration within your portal
        Use the Update Token Configuration operation to change the
        configuration properties of the token service.
        """
        url = self._url + "/tokens"
        params = {
            "f" : "json",
            "token": self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def securityConfiguration(self):
        """
        The security configuration consists of the identity store
        configuration.
        If your portal will be authenticated through ArcGIS Web Adaptor,
        you must set up your preferred authentication on your web server.
        Use the Update Identity Store operation to configure your portal to
        connect to your enterprise identity provider such as Windows Domain
        or LDAP. By default, Portal for ArcGIS is configured to use the
        built-in store and token-based authentication.
        """
        url = self._url + "/config"
        params = {
            "f" : "json",
            "token": self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def users(self):
        """ returns the number of registered users on site """
        url = self._url + "/users"
        params = {
            "f" : "json",
            "token": self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
########################################################################
class _System(BaseAGOLClass):
    """
       This resource is an umbrella for a collection of system-wide
       resources for your portal. This resource provides access to the
       ArcGIS Web Adaptor configuration, portal directories, database
       management server, indexing capabilities, license information, and
       the properties of your portal.
    """
    _securityHandler = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if securityHandler is None:
            pass
        elif isinstance(securityHandler, PortalTokenSecurityHandler):
            self._securityHandler = securityHandler

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
    #----------------------------------------------------------------------
    @property
    def webAdaptors(self):
        """
        The Web Adaptors resource lists the ArcGIS Web Adaptor configured
        with your portal. You can configure the Web Adaptor by using its
        configuration web page or the command line utility provided with
        the installation.
        """
        url = self._url + "/webadaptors"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def webAdaptor(self, webAdaptorID):
        """
        The ArcGIS Web Adaptor is a web application that runs in a
        front-end web server. One of the Web Adaptor's primary
        responsibilities is to forward HTTP requests from end users to
        Portal for ArcGIS. The Web Adaptor acts a reverse proxy, providing
        the end users with an entry point to the system, hiding the
        back-end servers, and providing some degree of immunity from
        back-end failures.
        The front-end web server can authenticate incoming requests against
        your enterprise identity stores and provide specific authentication
        schemes such as Integrated Windows Authentication (IWA), HTTP Basic,
        or Digest.
        Most importantly, a Web Adaptor provides your end users with a
        well-defined entry point to your system without exposing the
        internal details of your portal. Portal for ArcGIS will trust
        requests being forwarded by the Web Adaptor and will not challenge
        the user for any credentials. However, the authorization of the
        request (by looking up roles and permissions) is still enforced by
        the portal's sharing rules.

        Input:
           webAdaptorID - id of the web adaptor
        """
        url = self._url + "/webadaptors/%s" % webAdaptorID
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)

    #----------------------------------------------------------------------
    def unregisterWebAdaptor(self, webAdaptorID):
        """
        You can use this operation to unregister the ArcGIS Web Adaptor
        from your portal. Once a Web Adaptor has been unregistered, your
        portal will no longer trust the Web Adaptor and will not accept any
        credentials from it. This operation is typically used when you want
        to register a new Web Adaptor or when your old Web Adaptor needs to
        be updated.

        Input:
           webAdaptorID - id of the web adaptor
        """
        url = self._url + "/webadaptors/%s/unregister" % webAdaptorID
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateWebAdaptorsConfiguration(self, webAdaptorsConfig):
        """
        This operation is used to change the common properties and
        configuration of the ArcGIS Web Adaptor configured with the portal.
        The properties are stored as a JSON object and, therefore, every
        update must include all the necessary properties.
        Inputs:
           webAdaptorsConfig - The JSON object containing all the properties
                               in the configuration.
        """
        url = self._url + "/webadaptors/config/update"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
            "webAdaptorsConfig" : webAdaptorsConfig
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def webAdaptorsConfiguration(self):
        """
        This resource is a collection of configuration properties that
        apply to the ArcGIS Web Adaptor configured with the portal. The Web
        Adaptor fetches these properties periodically, which alters its
        behavior. Only one property is supported:
           sharedSecret - This property represents credentials that are
                          shared with the Web Adaptor. The Web Adaptor uses
                          these credentials to communicate with the portal.
        """
        url = self._url + "/webadaptors/config"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def directories(self):
        """
        The directories resource is a collection of directories that are
        used by the portal to store and manage content. At 10.2.1, Portal
        for ArcGIS supports five types of directories:
           Content directory-The content directory contains the data
                             associated with every item in the portal.
           Database directory-The built-in security store and sharing rules
                              are stored in a Database server that places
                              files in the database directory.
           Temporary directory-The temporary directory is used as a scratch
                               workspace for all the portal's runtime
                               components.
           Index directory-The index directory contains all the indexes
                           associated with the content in the portal. The
                           indexes are used for quick retrieval of
                           information and for querying purposes.
           Logs directory-Errors and warnings are written to text files in
                          the log file directory. Each day, if new errors
                          or warnings are encountered, a new log file is
                          created.
        If you would like to change the path for a directory, you can use
        the Edit Directory operation.
        """
        url = self._url + "/directories"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def directory(self, directoryName):
        """
        A directory is a file system-based folder that contains a specific
        type of content for the portal. The physicalPath property of a
        directory locates the actual path of the folder on the file system.
        At 10.2.1, Portal for ArcGIS supports local directories and network
        shares as valid locations.
        During the Portal for ArcGIS installation, the setup program asks
        you for the root portal directory (that will contain all the
        portal's sub directories). However, you can change each registered
        directory through this API.

        Input:
           directoryName - name of diretory category
        """
        url = self._url + "/directories/%s" % directoryName
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def editDirectory(self, directoryName, physicalPath, description):
        """
        The edit operation on a directory can be used to change the
        physical path and description properties of the directory. This is
        useful when changing the location of a directory from a local path
        to a network share. However, the API does not copy your content and
        data from the old path to the new path. This has to be done
        independently by the system administrator.

        Input:
           directoryName - name of the directory to change
           physicalPath - new path for directroy
           description - new description of the directory
        """
        url = self._url + "/directories/%s/edit" % directoryName
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
            "physicalPath": physicalPath,
            "description" : description
        }
        return self._do_post(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def database(self):
        """
        The database resource represents the database management system
        (DBMS) that contains all of the portal's configuration and
        relationship rules. This resource also returns the name and version
        of the database server currently running in the portal.
        You can use the Update Database Account operation to edit the
        administrative database account that is used by components within
        the portal to communicate with the database server.
        """
        url = self._url + "/database"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateDatabaseAccount(self, username,
                              password):
        """
        By default, the initial administrator account you define during the
        Create Site operation is used as the database administrator
        account. However, you can use this operation to change the database
        administrator account credentials. To change just the password for
        the account, provide the password parameter. If you want to create
        a completely new account for the database, provide new values for
        the username and password parameters.

        Input:
           username - database user name
           password - database user password
        """
        url = self._url + "/database/updateAdminAccount"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
            "username" : username,
            "password" : password
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def indexer(self):
        """
        The indexer resource contains connection information to the default
        indexing service. You can change its configuration properties such
        as the port number and host name if you want the portal sharing API
        to connect to and access another indexing service.
        """
        url = self._url + "/indexer"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def indexerStatus(self):
        """
        The status resource allows you to view the status of the indexing
        service. You can view the number of users, groups, relationships,
        and search items in both the database (store) and the index.
        If the database and index do not match, indexing is either in
        progress or there is a problem with the index. It is recommended
        that you reindex to correct any issues. If indexing is in progress,
        you can monitor the status by refreshing the page.
        """
        url = self._url + "/indexer/status"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def reindex(self, mode, includes=""):
        """
        This operation allows you to generate or update the indexes for
        content; such as users, groups, and items stored in the database
        (store). During the process of upgrading an earlier version of
        Portal for ArcGIS, you are required to update the indexes by
        running this operation. You can check the status of your indexes
        using the status resource.

        Input:
           mode - The mode in which the indexer should run.
                  Values: USER_MODE | GROUP_MODE | RELATION_MODE |
                          SEARCH_MODEL | FULL
           includes  An optional comma separated list of elements to
                     include in the index. This is useful if you want to
                     only index certain items or user accounts.
        """
        url = self._url + "/indexer/reindex"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
            "mode" : mode,
            "includes" : includes
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateIndexConfiguration(self,
                                 indexerHost="localhost",
                                 indexerPort=7199):
        """
        You can use this operation to change the connection information for
        the indexing service. By default, Portal for ArcGIS runs an
        indexing service that runs on port 7199. If you want the sharing
        API to refer to the indexing service on another instance, you need
        to provide the host and port parameters.

        Input:
           indexerHost - The name of the server (hostname) on which the
                         index service runs. The default value is localhost
           indexerPort - The port number on which the index service is
                         listening. The default value is 7199
        """
        url = self._url + "/indexer/update"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json",
            "indexerHost": indexerHost,
            "indexerPort": indexerPort
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def licenses(self):
        """
        Portal for ArcGIS requires a valid license to function correctly.
        This resource returns the current status of the license.
        """
        url = self._url + "/licenses"
        params = {
            "token" : self._securityHandler.token,
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)

########################################################################
class PortalAdministration(BaseAGOLClass):
    """
    This is the root resource for administering your portal. Starting from
    this root, all of the portal's environment is organized into a
    hierarchy of resources and operations.

    After installation, the portal can be configured using the Create Site
    operation. Once initialized, the portal environment is available
    through System and Security resources.
    """
    _securityHandler = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self, admin_url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if securityHandler is None:
            pass
        elif isinstance(securityHandler, PortalTokenSecurityHandler):
            self._securityHandler = securityHandler

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = admin_url
    #----------------------------------------------------------------------
    def createSite(self,
                   username,
                   password,
                   fullname,
                   email,
                   securityQuerstionIdx,
                   securityQuestionAns,
                   description=""
                   ):
        """
        The create site operation initializes and configures Portal for
        ArcGIS for use. It must be the first operation invoked after
        installation.
        Creating a new site involves:
           Creating the initial administrator account
           Creating a new database administrator account (which is same as
           the initial administrator account)
           Creating token shared keys
           Registering directories
        This operation is time consuming, as the database is initialized
        and populated with default templates and content. If the database
        directory is not empty, this operation attempts to migrate the
        database to the current version while keeping its data intact. At
        the end of this operation, the web server that hosts the API is
        restarted.

        Inputs:
           username - The initial administrator account name
           password - The password for the initial administrator account
           fullname - The full name for the initial administrator account
           email - The account email address
           description - An optional description for the account
           securityQuestionIdx - The index of the secret question to retrieve a forgotten password
           securityQuestionAns - The answer to the secret question

        """
        url = self._url + "/createNewSite"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "username" : username,
            "password" : password,
            "fullname" : fullname,
            "email" : email,
            "description" : description,
            "securityQuerstionIdx" : securityQuerstionIdx,
            "securityQuestionAns" : securityQuestionAns
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def system(self):
        """
        Creates a reference to the System operations for Portal
        """
        url = self._url + "/system"
        return _System(url=url,
                       securityHandler=self._securityHandler,
                       proxy_url=self._proxy_url,
                       proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def security(self):
        """
        Creates a reference to the Security operations for Portal
        """
        url = self._url + "/security"
        return _Security(url=url,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def root(self):
        """gets/sets the root admin url"""
        return self._url
    #----------------------------------------------------------------------
    @root.setter
    def root(self, value):
        """gets/sets the root admin url"""
        if self._url != value:
            self._url = value