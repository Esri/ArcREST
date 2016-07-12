"""
The ArcREST API allows you to perform administrative tasks not available in
the Portal for ArcGIS website. The API is organized into resources and
operations. Resources are entities within Portal for ArcGIS that hold some
information and have a well-defined state. Operations act on these
resources and update their information or state. Resources and operations
are hierarchical and have unique universal resource locators (URLs).
"""
from __future__ import absolute_import
from __future__ import print_function
import json
import tempfile
from datetime import datetime
from .._abstract.abstract import BaseAGOLClass
from ..security import PortalTokenSecurityHandler,ArcGISTokenSecurityHandler,OAuthSecurityHandler
########################################################################
class _Federation(BaseAGOLClass):
    """
    """
    _resources = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if url.lower().endswith("/federation") == False:
            url = url + "/federation"
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the site properties """
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
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
                print( k, " - attribute not implemented in manageportal.administration._Federation class.")
    #----------------------------------------------------------------------
    @property
    def servers(self):
        """
        This resource returns detailed information about the ArcGIS Servers
        registered with Portal for ArcGIS, such as the ID of the server,
        name of the server, ArcGIS Web Adaptor URL, administration URL, and
        if the server is set as a hosting server.
        """
        params = {"f" : "json"}
        url = self._url + "/servers"
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def unfederate(self, serverId):
        """
        This operation unfederates an ArcGIS Server from Portal for ArcGIS
        """
        url = self._url + "/servers/{serverid}/unfederate".format(
            serverid=serverId)
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_ur)
    #----------------------------------------------------------------------
    def updateServer(self, serverId, serverRole):
        """
        This operation unfederates an ArcGIS Server from Portal for ArcGIS

        Parameters:
           serverRole - Whether the server is a hosting server for the
            portal, a federated server, or a server with restricted access
            to publishing. The allowed values are FEDERATED_SERVER,
            FEDERATED_SERVER_WITH_RESTRICTED_PUBLISHING, or HOSTING_SERVER.
           serverId - unique id of the server
        """
        url = self._url + "/servers/{serverid}/update".format(
            serverid=serverId)
        params = {"f" : "json",
                  "serverRole" : serverRole}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_ur)
    #----------------------------------------------------------------------
    def validateServer(self, serverId):
        """
        This operation provides status information about a specific ArcGIS
        Server federated with Portal for ArcGIS.

        Parameters:
           serverId - unique id of the server
        """
        url = self._url + "/servers/{serverid}/validate".format(
            serverid=serverId)
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_ur)
    #----------------------------------------------------------------------
    def validateAllServers(self):
        """
        This operation provides status information about a specific ArcGIS
        Server federated with Portal for ArcGIS.

        Parameters:
           serverId - unique id of the server
        """
        url = self._url + "/servers/validate"
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_ur)
########################################################################
class _log(BaseAGOLClass):
    """handles the portal log information at 10.3.1+"""
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    _resources = None
    _operations = None

    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if url.lower().endswith("/logs") == False:
            url = url + "/logs"
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the site properties """
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
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
                print( k, " - attribute not implemented in manageportal.administration.log class.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """returns the admin sites resources"""
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    @property
    def operations(self):
        """lists operations available to user"""
        if self._operations is None:
            self.__init()
        return self._operations
    #----------------------------------------------------------------------
    @property
    def settings(self):
        """returns the log settings for portal"""
        url = self._url + "/settings"
        params = {
            "f" : "json",
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def editLogSettings(self, logLocation, logLevel="WARNING", maxLogFileAge=90):
        """
           edits the log settings for the portal site

           Inputs:
              logLocation - file path to where you want the log files saved
               on disk
              logLevel - this is the level of detail saved in the log files
                Levels are: OFF, SEVERE, WARNING, INFO, FINE, VERBOSE, and
                  DEBUG
              maxLogFileAge - the numbers of days to keep a single log file
        """
        url = self._url + "/settings/edit"
        params = {
            "f" : "json",
            "logDir" : logLocation,
            "logLevel" : logLevel,
            "maxLogFileAge" : maxLogFileAge
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def query(self, logLevel="WARNING", source="ALL",
              startTime=None, endTime=None,
              logCodes=None, users=None, messageCount=1000):
        """
           allows users to look at the log files from a the REST endpoint

           Inputs:
              logLevel - this is the level of detail saved in the log files
                Levels are: OFF, SEVERE, WARNING, INFO, FINE, VERBOSE, and
                  DEBUG
              source - the type of information to search.  Allowed values
                are: ALL, PORTAL_ADMIN, SHARING, PORTAL
              startTime - datetime object to start search at
              endTime - datetime object to end search
              logCodes - comma seperate list of codes to search
              users - comma seperated list of users to query
              messageCount - integer number of the max number of log
                entries to return to the user.
        """
        url = self._url + "/query"
        filter_value = {"codes":[], "users":[], "source": "*"}
        if source.lower() == "all":
            filter_value['source'] = "*"
        else:
            filter_value['source'] = [source]
        params = {
            "f" : "json",
            "level" : logLevel

        }
        if not startTime is None and \
           isinstance(startTime, datetime):
            params['startTime'] = startTime.strftime("%Y-%m-%dT%H:%M:%S")#2015-01-31T15:00:00
        if not endTime is None and \
           isinstance(endTime, datetime):
            params['endTime'] = startTime.strftime("%Y-%m-%dT%H:%M:%S")
        if not logCodes is None:
            filter_value['codes'] = logCodes.split(',')
        if not users is None:
            filter_value['users'] = users.split(',')
        if messageCount is None:
            params['pageSize'] = 1000
        elif isinstance(messageCount, (int, long, float)):
            params['pageSize'] = int(messageCount)
        else:
            params['pageSize'] = 1000
        params['filter'] = filter_value
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def cleanLogs(self):
        """erases all the log data"""
        url = self._url + "/clean"
        params = {
            "f":"json"
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
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
    _json = None
    _json_dict = None
    _resources = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if securityHandler is None:
            pass
        elif isinstance(securityHandler, PortalTokenSecurityHandler) or \
               isinstance(securityHandler, ArcGISTokenSecurityHandler) or \
               isinstance(securityHandler, OAuthSecurityHandler):
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the site properties """
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
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
                print( k, " - attribute not implemented in manageportal.administration.log class.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """returns the admin sites resources"""
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    def createUser(self,
                   username,
                   password,
                   firstName,
                   lastName,
                   email,
                   role="org_user",
                   provider="arcgis",
                   description="",
                   idpUsername=None):
        """
        This operation is used to create a new user account in the portal.
        Inputs:
           username - The name of the user account.
           password - The password for the account. This is a required
                      parameter only if the provider is arcgis; otherwise,
                      the password parameter is ignored.
           firstName - first name of the user account
           lastName - last name of the user account
           email - The email address for the user account.
           description - An optional description string for the user
                         account.
           role - The role for the user account. The default value is
                  org_user.
                  Values: org_user | org_publisher | org_admin
           provider - The provider for the account. The default value is
                      arcgis.
                      Values: arcgis | webadaptor | enterprise
           idpUsername - name of the user on the domain controller.
                         Ex: domain\account
        """
        url = self._url + "/users/createUser"
        params = {
            "f" : "json",
            "username" : username,
            "password" : password,
            "firstname" : firstName,
            "lastname" : lastName,
            "email" : email,
            "role" : role,
            "provider" : provider,
            "description" : description
        }
        if idpUsername is None:
            params['idpUsername'] = idpUsername
        return self._post(url=url,
                          param_dict=params,
                          securityHandler=self._securityHandler,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def deleteCertificate(self, certName):
        """
        This operation deletes an SSL certificate from the key store. Once
        a certificate is deleted, it cannot be retrieved or used to enable
        SSL.

        Inputs:
          certName - name of the cert to delete

        """

        params = {"f" : "json"}
        url = self._url + "/sslCertificates/{cert}/delete".format(
            cert=certName)
        return self._post(url=url, param_dict=params,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def exportCertificate(self, certName, outFolder=None):
        """
        This operation downloads an SSL certificate. The file returned by
        the server is an X.509 certificate. The downloaded certificate can
        be imported into a client that is making HTTP requests.

        Inputs:
          certName - name of the cert to export
          outFolder - folder on disk to save the certificate.
        """
        params = {"f" : "json"}
        url = self._url + "/sslCertificates/{cert}/export".format(
            cert=certName)
        if outFolder is None:
            outFolder = tempfile.gettempdir()
        return self._post(url=url, param_dict=params,
                          out_folder=outFolder,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def generateCertificate(self, alias,
                            commonName, organizationalUnit,
                            city, state, country,
                            keyalg="RSA", keysize=1024,
                            sigalg="SHA256withRSA",
                            validity=90
                            ):
        """
        Use this operation to create a self-signed certificate or as a
        starting point for getting a production-ready CA-signed
        certificate. The portal will generate a certificate for you and
        store it in its keystore.
        """
        params = {"f" : "json",
                  "alias" : alias,
                  "commonName" : commonName,
                  "organizationalUnit" : organizationalUnit,
                  "city" : city,
                  "state" : state,
                  "country" : country,
                  "keyalg" : keyalg,
                  "keysize" : keysize,
                  "sigalg" : sigalg,
                  "validity" : validity
                  }
        url = self._url + "/SSLCertificate/ generateCertificate"
        return self._post(url=url,
                          param_dict=params,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def generateCSR(self, certName):
        """
        """
        url = self._url + "/sslCertificates/{cert}/generateCsr".format(cert=certName)
        params = {"f" : "json"}
        return self._post(url=url, param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getAppInfo(self, appId):
        """
        Every application registered with Portal for ArcGIS has a unique
        client ID and a list of redirect URIs that are used for OAuth. This
        operation returns these OAuth-specific properties of an application.
        You can use this information to update the redirect URIs by using
        the Update App Info operation.

        Input:
           appId - unique id of the application to get the information
            about.
        """
        params = {
            "f" : "json",
            "appID" : appId
        }
        url = self._url + "/oauth/getAppInfo"
        return self._get(url=url, param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getUsersEnterpriseGroups(self, username, searchFilter, maxCount=100):
        """
        This operation lists the groups assigned to a user account in the
        configured enterprise group store. You can use the filter parameter
        to narrow down the search results.

        Inputs:
           username - name of the user to find
           searchFilter - helps narrow down results
           maxCount - maximum number of results to return
        """
        params = {
            "f" : "json",
            "username" : username,
            "filter" : searchFilter,
            "maxCount" : maxCount
        }
        url = self._url + "/Groups/getEnterpriseGroupsForUser"
        return self._get(url=url,
                         param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getEnterpriseUser(self, username):
        """"""
        url = self._url + "/users/getEnterpriseUser"
        params = {
            "f" : "json",
            "username" : username
        }
        return self._get(url=url, param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getUsersWithinEnterpriseGroup(self,
                                      groupName,
                                      searchFilter=None,
                                      maxCount=10):
        """
        This operation returns the users that are currently assigned to the
        enterprise group within the enterprise user/group store. You can
        use the filter parameter to narrow down the user search.

        Inputs:
          groupName - name of the group
          searchFilter - string used to narrow down the search
          maxCount - maximum number of users to return
        """
        params = {
            "f" : "json",
            "groupName" : groupName,
            "maxCount" : maxCount
        }
        if searchFilter:
            params['filters'] = searchFilter
        url = self._url + "/groups/getUsersWithinEnterpriseGroup"
        return self._get(url=url,
                         param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def importExistingServerCertificate(self, alias, certPassword,
                                        certFile):
        """
        This operation imports an existing server certificate, stored in
        the PKCS #12 format, into the keystore. If the certificate is a CA
        signed certificate, you must first import the CA Root or
        Intermediate certificate using the Import Root or Intermediate
        Certificate operation.

        Parameters
          alias - certificate name
          certPassword - password to unlock the certificate
          certFile - certificate file
        """
        url = self._url + "/sslCertificates/importExistingServerCertificate"
        files = {}
        files['certFile'] = certFile
        params = {
            "f" : "json",
            "alias" : alias,
            "certPassword" : certPassword
        }
        return self._post(url=url,
                          param_dict=params,
                          files=files,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def importRootOrIntermediate(self, alias, rootCSCertificate):
        """"""
        params = {
            "alias" : alias,
            "f" : "json"
        }
        files = {
            "rootCSCertificate" : rootCSCertificate
        }
        url = self._url + "/sslCertificates/importRootOrIntermediate"
        return self._post(url=url,
                          param_dict=params,
                          files=files,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def importSignedCertificate(self, alias, certFile):
        """
        This operation imports a certificate authority (CA) signed SSL
        certificate into the key store.
        """
        params = { "f" : "json" }
        files = {"file" : certFile}
        url = self._url + \
            "/sslCertificates/{cert}/importSignedCertificate".format(cert=alias)
        return self._post(url=url,
                          files=files,
                          param_dict=params,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def oauth(self):
        """
        The OAuth resource contains a set of operations that update the
        OAuth2-specific properties of registered applications in Portal for
        ArcGIS.
        """
        url = self._url + "/oauth"
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def refreshGroupMembership(self, groups):
        """
        This operation iterates over every enterprise account configured in
        the portal and determines if the user account is a part of the
        input enterprise group. If there are any change in memberships, the
        database and the indexes are updated for each group.
        While portal automatically refreshes the memberships during a user
        login and during a periodic refresh configured through the Update
        Identity Store operation, this operation allows an administrator to
        force a refresh.

        Parameters:
           groups - comma seperated list of group names
        """
        params = {
            "f" : "json",
            "groups" : groups
        }
        url = self._url + "/groups/refreshMembership"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def refreshUserMembership(self, users):
        """
        This operation iterates over every enterprise group configured in
        the portal and determines if the input user accounts belong to any
        of the configured enterprise groups. If there is any change in
        membership, the database and the indexes are updated for each user
        account. While portal automatically refreshes the memberships
        during a user login and during a periodic refresh (configured
        through the Update Identity Store operation), this operation allows
        an administrator to force a refresh.

        Parameters:
          users - comma seperated list of user names
        """
        params = {
            "f" : "json",
            "users" : users
        }
        url = self._url + "/users/refreshMembership"
        return self._post(url=url,
                          param_dict=params,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def searchEnterpriseGroups(self, searchFilter="", maxCount=100):
        """
        This operation searches groups in the configured enterprise group
        store. You can narrow down the search using the search filter
        parameter.

        Parameters:
           searchFilter - text value to narrow the search down
           maxCount - maximum number of records to return
        """
        params = {
            "f" : "json",
            "filter" : searchFilter,
            "maxCount" : maxCount
        }
        url = self._url + "/groups/searchEnterpriseGroups"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def searchEnterpriseUsers(self, searchFilter="", maxCount=100):
        """
        This operation searches users in the configured enterprise user
        store. You can narrow down the search using the search filter
        parameter.

        Parameters:
           searchFilter - text value to narrow the search down
           maxCount - maximum number of records to return
        """
        params = {
            "f" : "json",
            "filter" : searchFilter,
            "maxCount" : maxCount
        }
        url = self._url + "/users/searchEnterpriseUsers"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def SSLCertificates(self):
        """
        Lists certificates.
        """
        url = self._url + "/SSLCertificate"
        params = {"f" : "json"}
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getSSLCertificate(self, alias):
        """"""
        url = self._url + "/sslCertificates/{cert}".format(cert=alias)
        params = {"f": "json"}
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def testIdentityStore(self):
        """
        This operation can be used to test the connection to a user or
        group store.
        """
        params = {"f" : "json"}
        url = self._url + "/config/testIdentityStore"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def user_count(self):
        """
        The users resource is an umbrella for operations to manage members
        within Portal for ArcGIS. The resource returns the total number of
        members in the system.
        As an administrator, you can register enterprise accounts in your
        portal instance by using the Create User operation. When automatic
        sign-in for users is disabled in the security configuration,
        registered enterprise accounts can sign in as members of the
        portal. This gives you full control on all the accounts within a
        portal instance.
        """
        params = {"f" : "json"}
        url = self._url + "/users"
        return self._get(url=url, param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateAppInfo(self, appInfo):
        """
        This operation allows you to update the OAuth-specific properties
        associated with an application. Use the Get App Info operation to
        obtain the existing OAuth properties that can be edited.
        """
        params = {"f" : "json",
                  "appInfo" : appInfo}
        url = self._url + "/oauth/updateAppInfo"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateEnterpriseUser(self, username, idpUsername):
        """
        This operation allows an administrator to update the idpUsername
        for an enterprise user in the portal. This is used when migrating
        from accounts used with web-tier authentication to SAML
        authentication.

        Parameters:
           username - username of the enterprise account
           idpUsername - username used by the SAML identity provider
        """
        params = {
            "f" : "json",
            "username" : username,
            "idpUsername" : idpUsername
        }
        url = self._url + "/users/updateEnterpriseUser"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateWebServerCertificate(self, webServerCertificateAlias,
                                   sslProtocols,
                                   cipherSuites):
        """"""
        params = {
            "f" : "json",
            "webServerCertificateAlias": webServerCertificateAlias,
            "sslProtocols" : sslProtocols,
            "cipherSuites" : cipherSuites
        }
        url = self._url + "/sslcertificates/update"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
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
            "enableAutomaticAccountCreation": enableAutomaticAccountCreation,
            "disableServicesDirectory" : disableServicesDirectory
        }
        return self._post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
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
        r"""
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
            "userPassword" : userPassword,
            "isPasswordEncrypted" : isPasswordEncrypted,
            "user" : user,
            "userFullnameAttribute": userFullnameAttribute,
            "ldapURLForUsers" : ldapURLForUsers,
            "userEmailAttribute" : userEmailAttribute,
            "usernameAttribute" : usernameAttribute,
            "caseSensitive" : caseSensitive
        }
        return self._post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
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
            "tokenConfig" : {"sharedKey" : sharedKey}
        }
        return self._post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def users(self):
        """ returns the number of registered users on site """
        url = self._url + "/users"
        params = {
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
        if securityHandler is not None:
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            "f" : "json",
            "webAdaptorsConfig" : webAdaptorsConfig
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            "f" : "json",
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json",
            "physicalPath": physicalPath,
            "description" : description
        }
        return self._post(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def getEntitlements(self, appId):
        """
        This operation returns the currently queued entitlements for a
        product, such as ArcGIS Pro or Navigator for ArcGIS, and applies
        them when their start dates become effective. It's possible that
        all entitlements imported using the Import Entitlements operation
        are effective immediately and no entitlements are added to the
        queue. In this case, the operation returns an empty result.
        """
        params = {
            "f" : "json",
            "appId" : appId
        }
        url = self._url + "/licenses/getEntitlements"
        return self._get(url=url, param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def importEntitlements(self, entitlementFile, appId):
        """"""
        params = {
                    "f" : "json",
                    "appId" : appId
                }
        url = self._url + "/licenses/importEntitlements"
        files = {"file" : entitlementFile}
        return self._post(url=url, param_dict=params,
                          files=files,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def languages(self):
        """
        This resource lists which languages will appear in portal content
        search results.
        """
        params = {"f" : "json"}
        url = self._url + "/languages"
        return self._get(url=url,
                         param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def releaseLicense(self, username):
        """
        If a user checks out an ArcGIS Pro license for offline or
        disconnected use, this operation releases the license for the
        specified account. A license can only be used with a single device
        running ArcGIS Pro. To check in the license, a valid access token
        and refresh token is required. If the refresh token for the device
        is lost, damaged, corrupted, or formatted, the user will not be
        able to check in the license. This prevents the user from logging
        in to ArcGIS Pro from any other device. As an administrator, you
        can release the license. This frees the outstanding license and
        allows the user to check out a new license or use ArcGIS Pro in a
        connected environment.

        Parameters:
           username - username of  the account
        """
        url = self._url + "/licenses/releaseLicense"
        params = {
            "username" : username,
            "f" : "json"
        }
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeAllEntitlements(self, appId):
        """
        This operation removes all entitlements from the portal for ArcGIS
        Pro or additional products such as Navigator for ArcGIS and revokes
        all entitlements assigned to users for the specified product. The
        portal is no longer a licensing portal for that product.
        License assignments are retained on disk. Therefore, if you decide
        to configure this portal as a licensing portal for the product
        again in the future, all licensing assignments will be available in
        the website.

        Parameters:
           appId - The identifier for the application for which the
            entitlements are being removed.
        """
        params = {
            "f" : "json",
            "appId" : appId
        }
        url = self._url + "/licenses/removeAllEntitlements"
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def system_properties(self):
        """
        This resource lists system properties that have been modified to
        control the portal's environment.
        """
        params = {"f" : "json"}
        url = self._url + "/properties"
        return self._get(url=url,
                         param_dict=params,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateLanguages(self, languages):
        """
        You can use this operation to change which languages will have
        content displayed in portal search results.

        Parameters:
           languages - The JSON object containing all of the possible
             portal languages and their corresponding status (true or
             false).
        """
        url = self._url = "/languages/update"
        params = {
            "f" : "json",
            "languages" : languages
        }
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateLicenseManager(self, licenseManagerInfo):
        """
        ArcGIS License Server Administrator works with your portal and
        enforces licenses for ArcGIS Pro. This operation allows you to
        change the license server connection information for your portal.
        When you import entitlements into portal using the Import
        Entitlements operation, a license server is automatically configured
        for you. If your license server changes after the entitlements have
        been imported, you only need to change the license server
        connection information.
        You can register a backup license manager for high availability of
        your licensing portal. When configuring a backup license manager,
        you need to make sure that the backup license manager has been
        authorized with the same organizational entitlements. After
        configuring the backup license manager, Portal for ArcGIS is
        restarted automatically. When the restart completes, the portal is
        configured with the backup license server you specified.

        Parameters:
           licenseManagerInfo - The JSON representation of the license
             server connection information.
        """
        url = self._url + "/licenses/updateLicenseManager"
        params = {
            "f" : "json",
            "licenseManagerInfo" : licenseManagerInfo
        }
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json",
            "username" : username,
            "password" : password
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            "f" : "json",
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json",
            "mode" : mode,
            "includes" : includes
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json",
            "indexerHost": indexerHost,
            "indexerPort": indexerPort
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
    _siteKey = None
    _securityHandler = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    _resources = None
    _version = None
    _json = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self, admin_url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initalize=False):
        """Constructor"""
        if admin_url.endswith("/portaladmin") == False:
            admin_url = admin_url + "/portaladmin"
        if securityHandler is not None:
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = admin_url
        if initalize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the site properties """
        params = {
            "f" : "json",
        }

        json_dict = self._get(self._url, params,
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
                setattr(self, k, v)
                print( k, " - attribute not implemented in manageportal.administration class.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the raw key/values for the object"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def siteKey(self):
        """gets the portal siteKey property"""
        if self._siteKey is None:
            self.__init()
        return self._siteKey
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """returns the admin sites resources"""
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    @property
    def version(self):
        """returns the portal version"""
        if self._version is None:
            self.__init()
        return self._version
    #----------------------------------------------------------------------
    def createSite(self, username, password, fullname,
                   email, description, securityQuestionIdx,
                   secuirtyQuestionAns, contentDir
                   ):
        """
        The create site operation initializes and configures Portal for
        ArcGIS for use. It must be the first operation invoked after
        installation. Creating a new site involves:

        Creating the initial administrator account
        Creating a new database administrator account (which is same as the
         initial administrator account)
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
        email	- The account email address
        description - An optional description for the account
        securityQuestionIdx - The index of the secret question to retrieve
         a forgotten password
        securityQuestionAns - The answer to the secret question
        contentDir - The path to the location of the site's content
        """
        params = {
            "username" : username,
            "password" : password,
            "fullname" : fullname,
            "email" : email,
            "description" : description,
            "secuirtyQuestionAns" :  secuirtyQuestionAns,
            "securityQuestionIdx" : securityQuestionIdx,
            "contentDir" : contentDir
        }
        url = self._url + "/createNewSite"
        return self._get(url=url,
                          param_dict=params)
    #----------------------------------------------------------------------
    def exportSite(self, location):
        """
        This operation exports the portal site configuration to a location
        you specify.
        """
        params = {
            "location" : location,
            "f" : "json"
        }
        url = self._url + "/exportSite"
        return self._post(url=url, param_dict=params)
    #----------------------------------------------------------------------
    def importSite(self, location):
        """
        This operation imports the portal site configuration to a location
        you specify.
        """
        params = {
            "location" : location,
            "f" : "json"
        }
        url = self._url + "/importSite"
        return self._post(url=url, param_dict=params)
    #----------------------------------------------------------------------
    def joinSite(self, machineAdminUrl,
                 username, password):
        """
        The joinSite operation connects a portal machine to an existing
        site. You must provide an account with administrative privileges to
        the site for the operation to be successful.
        """
        params = {
            "machineAdminUrl" : machineAdminUrl,
            "username" : username,
            "password" : password,
            "f" : "json"
        }
        url = self._url + "/joinSite"
        return self._post(url=url, param_dict=params)
    #----------------------------------------------------------------------
    def unregisterMachine(self, machineName):
        """
        This operation unregisters a portal machine from a portal site. The
        operation can only performed when there are two machines
        participating in a portal site.
        """
        url = self._url + "/machines/unregister"
        params = {
            "f" : "json",
            "machineName" : machineName
        }
        return self._post(url=url,
                          param_dict=params,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def federation(self):
        """returns the class that controls federation"""
        url = self._url + "/federation"
        return _Federation(url=url,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
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
    def logs(self):
        """returns the portals log information"""
        url = self._url + "/logs"
        return _log(url=url,
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
