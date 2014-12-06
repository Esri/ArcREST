from ..security.security import OAuthSecurityHandler, AGOLTokenSecurityHandler
from .._abstract.abstract import BaseAGOLClass
import os
import urlparse
import parameters

########################################################################
class oauth2(BaseAGOLClass):
    """
    The root of all OAuth2 resources and operations.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None

    #----------------------------------------------------------------------
    def __init__(self, oauth_url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = oauth_url
        self._proxy_port = proxy_port
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url  
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    def root(self):
        """ returns the root url for OAuth2 resources """
        return self._url
    #----------------------------------------------------------------------
    def registerApp(self,
                    itemId,
                    appType,
                    redirect_uris=None):
        """
        The register app operation registers an app item with the portal.
        App registration results in an APPID and APPSECRET (also known as
        client_id and client_secret (in OAuth speak respectively) being
        generated for that application. Upon successful registration, a
        Registered App type keyword gets appended to the app item.

        Inputs:
           itemId - The ID of item being registered. Note that the item
                    must be owned by the user invoking this operation
                    otherwise the call will be rejected.

           appType - The type of app that was registered indicating whether
                     it's a browser app, native app, server app or a
                     multiple interface app.
                     Values: browser | native | server| multiple

           redirect_uris - The URIs where the access_token or authorization
                           code will be delivered to upon successful
                           authorization. The redirect_uri specified during
                           authorization must be match one of the
                           registered URIs otherwise authorization will be
                           rejected.
                           A special value of urn:ietf:wg:oauth:2.0:oob can
                           also be specified for authorization grants. This
                           will result in the authorization code being
                           delivered to a portal URL (/oauth2/approval).
                           This value is typically used by applications
                           that don't have a web server or a custom URI
                           scheme to deliver the code to.
                           The value is a JSON string array.
        """
        url = self._url + "/registerApp"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "itemId" : itemId,
            "appType" : appType
        }
        if redirect_uris is None:
            params['redirect_uris'] = redirect_uris
        return self._do_post(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def registeredApp(self, clientId):
        """
        An app registered with the portal. An app item can be registered by
        invoking the register app operation. Every registered app gets an
        App ID and App Secret which in OAuth speak are known as client_id
        and client_secret respectively.
        Only the app owner has access to the registered app resource.
        """
        url = self._url + "/app/%s" % clientId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)









