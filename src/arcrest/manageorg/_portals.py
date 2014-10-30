from ..security.security import OAuthSecurityHandler, AGOLTokenSecurityHandler
from .._abstract.abstract import BaseAGOLClass
import os
import urlparse
import parameters
########################################################################
class Portals(BaseAGOLClass):
    """
    provides access to the portals' child resources.
    """
    _baseURL = None
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _portalId = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 portalId,
                 securityHandler,
                 proxy_url,
                 proxy_port):
        """Constructor"""
        if url.lower().find("/portals") < 0:
            
            self._url = url + "/portals/%s" % portalId
            self._baseURL = url + "/portals"
        else:
            self._url = url + "/%s" % portalId
            self._baseURL = url
        self._portalId = portalId
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    @property
    def portalRoot(self):
        """ returns the base url without the portal id """
        return self._baseURL
    #----------------------------------------------------------------------
    def addResource(self, key, filePath, text):
        """
        The add resource operation allows the administrator to add a file
        resource, for example, the organization's logo or custom banner.
        The resource can be used by any member of the organization. File
        resources use storage space from your quota and are scanned for
        viruses.

        Inputs:
           key - The name the resource should be stored under.
           filePath - path of file to upload
           text - Some text to be written (for example, JSON or JavaScript)
                  directly to the resource from a web client.
        """
        url = self._url + "/addresource"
        params = {
        "f": "json",
        "token" : self._securityHandler.token,
        "key" : key,
        "text" : text
        }
        parsed = urlparse.urlparse(url)
        files = []
        files.append(('file', filePath, os.path.basename(filePath)))
        res = self._post_multipart(host=parsed.hostname,
                                           selector=parsed.path,
                                           files = files,
                                           fields=params,
                                           port=parsed.port,
                                           ssl=parsed.scheme.lower() == 'https',
                                           proxy_port=self._proxy_port,
                                           proxy_url=self._proxy_url)
        return res
    #----------------------------------------------------------------------
    def checkServiceName(self,
                         name,
                         serviceType):
        """
        Checks to see if a given service name and type are available for
        publishing a new service. true indicates that the name and type is
        not found in the organization's services and is available for
        publishing. false means the requested name and type are not available.

        Inputs:
           name - requested name of service
           serviceType - type of service allowed values: Feature Service or
                         Map Service
        """
        _allowedTypes = ['Feature Service', "Map Service"]
        url = self._url + "/isServiceNameAvailable"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "name" : name,
            "type" : serviceType
        }
        return self._do_get(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def languages(self):
        """ list of available languages """
        url = self._url + "/languages"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,

        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def portalProperties(self):
        """
        Portal returns information on your organization and is accessible
        to administrators. Publishers and information workers can view
        users and resources of the organization.
        """
        url = self._url
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def portalSelf(self, culture=None, region=None):
        """
        The Portal Self resource is used to return the view of the portal
        as seen by the current user, anonymous or logged in. It includes
        information such as the name, logo, featured items, and supported
        protocols (HTTP vs. HTTPS) for this portal. If the user is not
        logged in, this call will return the default view of the portal. If
        the user is logged in, the view of the returned portal will be
        specific to the organization to which the user belongs. The default
        view of the portal is dependent on the culture of the user, which
        is obtained from the user's profile. A parameter to pass in the
        locale/culture is available for anonymous users.

        Inputs:
           culture - the culture code of the calling client output is
                     customized for this culture if settings are available
           region - the region code of the calling client.
        """
        url = self._url + "/self"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,

        }
        if culture is not None:
            params['culture'] = culture
        if region is not None:
            params['region'] = region

        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def regions(self):
        """
        Lists the available regions
        """
        url = self._url + "/regions"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def registerServer(self,
                       name,
                       url,
                       adminUrl,
                       isHosted,
                       serverType):
        """
        You can optionally register (or "federate") an ArcGIS Server site
        with your Portal for ArcGIS deployment. This provides the
        following benefits:
             The server and the portal share the same user store (that of
             the portal). This results in a convenient single sign-on
             experience.

             Any items you publish to the server are automatically shared
             on the portal.

             You can optionally allow the server to host tiled map services
             and feature services published by portal users.

        After you register a server with your portal, you must invoke the
        Update Security Configuration operation on the ArcGIS Server site
        and configure the site's security store to take advantage of users
        and roles from the portal.

        This operation is only applicable to Portal for ArcGIS; it is not
        supported with ArcGIS Online.

        Inputs:
           name - The fully qualified name of the machine hosting the
                  ArcGIS Server site, followed by the port.
           url - The externally visible URL of the ArcGIS Server site,
                 using the fully qualified name of the machine.
           adminUrl - The administrative URL of your ArcGIS Server site,
                      using the fully qualified name of the machine.
           isHosted - A Boolean property denoting whether the ArcGIS Server
                      site will be allowed to host services for the portal
                      (true) or not be allowed to host services (false).
           serverType - The type of server being registered with the portal
                        For example: ArcGIS.
        """
        url = self._url + "/register"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "url" : url,
            "adminUrl" : adminUrl,
            "isHosted" : isHosted,
            "name" : name,
            "serverType" : serverType
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeResource(self, key):
        """
        The Remove Resource operation allows the administrator to remove a
        file resource.

        Input:
           key - name of resource to delete
        """
        url = self._url + "/removeresource"
        params = {
            "key" : key,
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUser(self, users):
        """
        The Remove Users operation allows the administrator to remove users
        from a portal. Before the administrator can remove the user, all of
        the user's content and groups must be reassigned or deleted.

        Inputs:
           users - Comma-separated list of usernames to remove.
        """
        url = self._url + "/removeusers"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "users" : users
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def resources(self,
                  start=1,
                  num=10):
        """
        Resources lists all file resources for the organization. The start
        and num paging parameters are supported.

        Inputs:
           start - the number of the first entry in the result set response
                   The index number is 1-based and the default is 1
           num - the maximum number of results to be returned as a whole #
        """
        url = self._url + "/resources"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "start" : start,
            "num" : num
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def server(self, serverId):
        """
        This resource represents an ArcGIS Server site that has been
        federated with the portal.
        This resource is not applicable to ArcGIS Online; it is only
        applicable to Portal for ArcGIS.
        """
        url = self._url + "/servers/%s" % serverId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def servers(self):
        """
        This resource lists the ArcGIS Server sites that have been
        federated with the portal. This resource is not applicable to
        ArcGIS Online; it is only applicable to Portal for ArcGIS.
        """
        url = self._url + "/servers"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def unregisterServer(self, serverId):
        """
        This operation unregisters an ArcGIS Server site from the portal.
        The server is no longer federated with the portal after this
        operation completes.
        After this operation completes, you must invoke the Update Security
        Configuration operation on your ArcGIS Server site to specify how
        you want the server to work with users and roles.

        Inputs:
           serverId - unique identifier of the server
        """
        url = self._url + "/servers/%s/unregister" % serverId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def update(self,
               updatePortalParameters,
               clearEmptyFields=False):
        """
        The Update operation allows administrators only to update the
        organization information such as name, description, thumbnail, and
        featured groups.

        Inputs:
           updatePortalParamters - parameter.PortalParameters object that holds information to update
           clearEmptyFields - boolean that clears all whitespace from fields
        """
        url = self._url + "/update"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "clearEmptyFields" : clearEmptyFields
        }
        if isinstance(updatePortalParameters, parameters.PortalParameters):
            params.update(updatePortalParameters.value)
        else:
            raise AttributeError("updatePortalParameters must be of type parameter.PortalParameters")
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateServer(self,
                     serverId,
                     name,
                     url,
                     adminUrl,
                     isHosted,
                     serverType):
        """
        This operation updates the properties of an ArcGIS Server site that
        has been registered, or federated, with the portal. For example,
        you can use this operation to change the federated site that acts
        as the portal's hosting server.

        Inputs:
           serverId - identifier of server to update.
           name - The fully qualified name of the machine hosting the
                  ArcGIS Server site, followed by the port.
           url - The externally visible URL of the ArcGIS Server site,
                 using the fully qualified name of the machine.
           adminUrl - The administrative URL of the ArcGIS Server site,
                      using the fully qualified name of the machine.
           isHosted - A Boolean property denoting whether the ArcGIS Server
                      site will be allowed to host services for the portal
                      (true) or will not be allowed to host services
                      (false).
           serverType - The type of server being registered with the portal
                        For example: ArcGIS.
        """
        url = self._url + "/%s/update" % serverId
        params = {
            "name" : name,
            "url" : url,
            "adminUrl" : adminUrl,
            "isHosted" : isHosted,
            "serverType" : serverType
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateUserRole(self,
                       user,
                       role):
        """
        The Update User Role operation allows the administrator of an org
        anization to update the role of a user within a portal.

        Inputs:
           role - Sets the user's role.
                  Roles are the following:
                      org_user - Ability to add items, create groups, and
                        share in the organization.
                      org_publisher - Same privileges as org_user plus the
                        ability to publish hosted services from ArcGIS for
                        Desktop and ArcGIS Online.
                      org_admin - In addition to add, create, share, and publish
                        capabilities, an org_admin administers and customizes
                        the organization.
                  Example: role=org_publisher
           user - The username whose role you want to change.

        """
        url = self._url + "/updateuserrole"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "user" : user,
            "role" : role
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
        #----------------------------------------------------------------------
    def users(self, start=1, num=10):
        """
        Lists all the members of the organization. The start and num paging
        parameters are supported.

        Inputs:
           start - The number of the first entry in the result set response.
                   The index number is 1-based.
                   The default value of start is 1 (that is, the first
                   search result).
                   The start parameter, along with the num parameter, can
                   be used to paginate the search results.
           num - The maximum number of results to be included in the result
                 set response.
                 The default value is 10, and the maximum allowed value is
                 100.The start parameter, along with the num parameter, can
                 be used to paginate the search results.
        """
        url = self._url + "/users"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "start" : start,
            "num" : num
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)




















