"""
Handles all the security oeprations for the product logins.

"""
from __future__ import print_function
from __future__ import absolute_import
import datetime
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
try:
    from ..packages.ntlm3 import HTTPNtlmAuthHandler
    hasNTLM = True
except:
    hasNTLM = False
from .._abstract import abstract
from ..packages.six.moves.urllib import request
from ..packages.six.moves.urllib_parse import urlencode, urlparse, urlunparse
from ..packages.six.moves.http_cookiejar import CookieJar
from ..constants import DEFAULT_TOKEN_EXPIRATION

_defaultTokenExpiration = DEFAULT_TOKEN_EXPIRATION #Minutes
########################################################################
class CommunityMapsSecurityHandler(abstract.BaseSecurityHandler):
    """
    Handler that allows access to the community maps program
    """
    _referer_url = "esri"
    _method = "TOKEN"
    _username = None
    _password = None
    _agolSecurityHandler = None
    _securityHandler = None
    _token = None
    _expire = _defaultTokenExpiration
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 username,
                 password,
                 proxy_url=None,
                 proxy_port=None):
        """ initialize"""
        self._url = url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._agolSecurityHandler = AGOLTokenSecurityHandler(username=username,
                                                            password=password)
        self._referer_url = urlparse(url).netloc
    @property
    def securityhandler(self):
        """ges/set the AGOLTokenSecurityHandler"""
        return self._agolSecurityHandler
    @securityhandler.setter
    def securityhandler(self, value):
        """get/set the AGOLTokenSecurityHandler"""
        if isinstance(value, AGOLTokenSecurityHandler):
            self._agolSecurityHandler = value
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ generates a token """
        return self._generateForTokenSecurity()
    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self):
        """ generates a token for a feature service """
        agolToken = self._agolSecurityHandler.token
        url = self._url + "/getProxyUserToken"
        params = {"token" : self._agolSecurityHandler.token,
                  "contributorUid" : self._contributionUID}
        res = self._post(url=url, param_dict=params,
                         additional_headers={ "Referer": self._agolSecurityHandler._referer_url},
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
        return res['token']
    #----------------------------------------------------------------------
    @property
    def _contributionUID(self):
        """"""
        url = self._url + "/users/" + self._username
        params = {'f': 'json'}
        res = self._get(url=url, param_dict=params)
        return res["ContributorUID"]
########################################################################
class LDAPSecurityHandler(abstract.BaseSecurityHandler):
    """
       This Security Handler handles LDAP based security.
    """

    _jar = None
    _handler = None
    _certificatefile = None
    _keyfile = None
    _token = ""
    _proxy_url = None
    _proxy_port = None
    _org_url = None
    _url = None
    _surl = None
    _referer_url = None
    _parsed_org_url = None
    _portal_username = None
    _method = "HANDLER"
    _login_username = None
    _username = None
    _password = None
    #----------------------------------------------------------------------
    def __init__(self, org_url, username, password,
                 proxy_url=None, proxy_port=None, referer_url=None):
        """Constructor"""
        self._login_username = username
        self._password = password

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port

        self._initURL(org_url=org_url,
                      referer_url=referer_url)

        self.loadusername()
    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal
    #----------------------------------------------------------------------
    @property
    def method(self):
        """get the security handler type"""
        return self._method
    #----------------------------------------------------------------------
    def _initURL(self,
                 org_url,
                 referer_url):
        """ sets proper URLs for AGOL """


        if org_url is not None and org_url != '':
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'https://' + org_url
            self._org_url = org_url

        if self._org_url.lower().find('/sharing/rest') > -1:
            self._url = self._org_url
        else:
            self._url = self._org_url + "/sharing/rest"

        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
            self._surl = self._url

        parsed_url = urlparse(self._org_url)
        self._parsed_org_url = urlunparse((parsed_url[0],parsed_url[1],"","","",""))#added 7/15/2015

        if referer_url is None:
            self._referer_url = parsed_url.netloc

    #----------------------------------------------------------------------
    @property
    def org_url(self):
        """gets the org_url"""
        return self._org_url
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """gets the referer url"""
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def token(self):
        """gets the token"""
        return self._token
    #----------------------------------------------------------------------
    @property
    def username(self):
        """gets/sets the username"""
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, value):
        """gets/sets the username"""
        if isinstance(value, str):
            self._username = value
            self._handler = None
    #----------------------------------------------------------------------
    @property
    def password(self):
        """gets/sets the current password"""
        return self._password
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """gets/sets the current password"""
        if isinstance(value, str):
            self._password = value
            self._handler = None
    #----------------------------------------------------------------------
    @property
    def handler(self):
        """returns the handler"""
        if self._handler is None:
            passman = request.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None,
                                 self._parsed_org_url,
                                 self._login_username,
                                 self.password)
            self._handler = request.HTTPBasicAuthHandler(passman)
        return self._handler
    #----------------------------------------------------------------------
    @property
    def cookiejar(self):
        """gets the cookiejar"""
        if self._jar is None:
            self._jar = CookieJar()
        return self._jar

    def loadusername(self):
        if self._username is None:
            from ..manageorg import Administration
            admin = Administration(url=self._org_url,
                                   securityHandler=self,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)
            portal = admin.portals.portalSelf

            if 'username' in portal.user:
                self._username = portal.user['username']
            else:
                self._username = self._login_username

            del portal, admin

    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    def portalServerHandler(self, serverUrl, username=None):
        """
        returns a handler to access a federated server

        serverUrl - url to the server. Example:
                    https://server.site.com/arcgis
        username - the portal site username. if None is passed, it obtains
         it from the portal properties
        Outout:
          returns a PortalServerSecurityHandler object

        Usage:
        >>> # access the administration site
        >>> serverUrl="https://mysite.site.com/arcgis"
        >>> newSH = sh.portalServerHandler(serverUrl=serverUrl,
                                           username=None)
        >>> agsAdmin = AGSAdministration(url=serverUrl, securityHandler=newSH)
        >>> print agsAdmin.info
        >>> # access a secure service from portal handler
        >>> msUrl = "https://mysite.site.com:6443/arcgis/rest/services/SampleWorldCities/MapServer"
        >>> ms = arcrest.ags.MapService(url=msUrl, securityHandler=newSH)
        >>> print ms.mapName
        """


        from ..manageorg import Administration
        admin = Administration(url=self._org_url,
                               securityHandler=self,
                               proxy_url=self._proxy_url,
                               proxy_port=self._proxy_port)

        token_url = admin.tokenURL

        if username is None:
            username = self._login_username

        ptsh = PortalTokenSecurityHandler(username=username,
                                          password=self._password,
                                          org_url=self._org_url,
                                          token_url=token_url,
                                          proxy_url=self._proxy_url,
                                          proxy_port=self._proxy_port,
                                          jar=self.cookiejar,
                                          handler=self.handler)

        pssh = PortalServerSecurityHandler(tokenHandler=ptsh,
                                           serverUrl=serverUrl,
                                           referer=self._referer_url,
                                           jar=self.cookiejar,
                                           handler=self.handler)


        return pssh

########################################################################
class NTLMSecurityHandler(LDAPSecurityHandler):
    """performs NTLM/Kerberos security handling"""

    def __init__(self, org_url, username, password, proxy_url=None,
                 proxy_port=None, referer_url=None):
        self._login_username = username
        self._password = password

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port

        self._initURL(org_url=org_url,
                      referer_url=referer_url)
        self.loadusername()
    #----------------------------------------------------------------------
    @property
    def handler(self):
        """gets the security handler for the class"""
        if hasNTLM:
            if self._handler is None:
                passman = request.HTTPPasswordMgrWithDefaultRealm()
                passman.add_password(None, self._parsed_org_url, self._login_username, self._password)
                self._handler = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
            return self._handler
        else:
            raise Exception("Missing Ntlm python package.")
    #----------------------------------------------------------------------
    @property
    def cookiejar(self):
        """gets the cookiejar"""
        if self._jar is None:
            self._jar = CookieJar()
        return self._jar
########################################################################
class PKISecurityHandler(abstract.BaseSecurityHandler):
    """
       This Security Handler handles PKI based security
    """

    _jar = None
    _handler = None
    _certificatefile = None
    _keyfile = None
    _token = ""
    _proxy_url = None
    _proxy_port = None
    _org_url = None
    _parsed_org_url = None
    _url = None
    _surl = None
    _referer_url = None
    _method = "HANDLER"
    _username = None
    #----------------------------------------------------------------------
    def __init__(self, org_url, keyfile, certificatefile,
                 proxy_url=None, proxy_port=None, referer_url=None):
        """Constructor"""
        self._keyfile = keyfile
        self._certificatefile = certificatefile

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port

        self._initURL(org_url=org_url,
                      referer_url=referer_url)
    #----------------------------------------------------------------------
    @property
    def method(self):
        """get the security handler type"""
        return self._method
    #----------------------------------------------------------------------
    def _initURL(self,
                 org_url,
                 referer_url):
        """ sets proper URLs for AGOL """
        if org_url is not None and org_url != '':
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'https://' + org_url
            self._org_url = org_url

            if self._org_url.lower().find('/sharing/rest') > -1:
                self._url = self._org_url
            else:
                self._url = self._org_url + "/sharing/rest"

            if self._url.startswith('http://'):
                self._surl = self._url.replace('http://', 'https://')
            else:
                self._surl = self._url

            parsed_url = urlparse(self._org_url)
            self._parsed_org_url = urlunparse((parsed_url[0],parsed_url[1],"","","",""))

        if referer_url is None:
            parsed_org = urlparse(self._org_url)
            self._referer_url = parsed_org.netloc

            url = '{}/portals/self'.format( self._url)

        parameters = {
            'f': 'json'
        }
        portal_info = self._post(url=url,
                                 param_dict=parameters,
                                 securityHandler=self,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        if 'user' in portal_info:
            if 'username' in portal_info['user']:
                self._username = portal_info['user']['username']
    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username """
        return self._username
    #----------------------------------------------------------------------

    @property
    def org_url(self):
        """gets the org_url"""
        return self._org_url
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """gets the referer url"""
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def token(self):
        """gets the token"""
        return self._token
    #----------------------------------------------------------------------
    @property
    def handler(self):
        """returns the handler"""
        if self._handler is None:
            self._handler = self.HTTPSClientAuthHandler(key=self._keyfile,
                                                        cert=self._certificatefile)
        return self._handler
    #----------------------------------------------------------------------
    @property
    def certificate(self):
        """gets/sets the certificate file"""
        return self._certificatefile
    #----------------------------------------------------------------------
    @certificate.setter
    def certificate(self, value):
        """gets/sets the certificate file"""
        import os
        if os.path.isfile(value):
            self._certificatefile = value
    #----------------------------------------------------------------------
    @property
    def key_file(self):
        """returns the key file"""
        return self._keyfile
    #----------------------------------------------------------------------
    @key_file.setter
    def key_file(self, value):
        """gets/sets the certificate file"""
        import os
        if os.path.isfile(value):
            self._keyfile = value
    #----------------------------------------------------------------------
    @property
    def cookiejar(self):
        """gets the cookiejar"""
        if self._jar is None:
            self._jar = CookieJar()
        return self._jar
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    class HTTPSClientAuthHandler(request.HTTPSHandler):
        from ..packages.six.moves import http_client as httplib#import httplib
        def __init__(self, key, cert):
            request.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert
        def https_open(self, req):
            #Rather than pass in a reference to a connection class, we pass in
            # a reference to a function which, for all intents and purposes,
            # will behave as a constructor
            return self.do_open(self.getConnection, req)
        def getConnection(self, host, timeout=300):
            return  self.httplib.HTTPSConnection(host,
                                                 key_file=self.key,
                                                 cert_file=self.cert,
                                                 timeout=timeout)
########################################################################
class PortalServerSecurityHandler(abstract.BaseSecurityHandler):
    """
    This service is designed to allow users manage a server from a Portal
    site credentials.  This means a user can get an ArcGIS Server Token
    from a Portal login to manage and use secure services.  It is not
    designed for users to create this object through code, but rather it is
    generated by the system.
    """
    _method = "TOKEN"
    _tokenHandler = None
    _serverUrl = None
    _referer = None
    _parsed_org_url = None
    _token = None
    _handler = None
    _jar = None
    #
    def __init__(self,
                 tokenHandler,
                 serverUrl,
                 referer,
                 handler=None,
                 jar = None):

        """Constructor"""
        if isinstance(tokenHandler, PortalTokenSecurityHandler):
            self._portalTokenHandler = tokenHandler
        elif isinstance(tokenHandler, ArcGISTokenSecurityHandler):
            self._tokenHandler = tokenHandler
        else:
            raise AttributeError("Invalid token handler")

        self._handler = handler
        self._jar = jar
        self._initURL(serverUrl=serverUrl)

        #----------------------------------------------------------------------
    def _initURL(self, serverUrl=None):
        """ sets proper URLs for AGOL """
        self._serverUrl = serverUrl

        parsed_url = urlparse(self._serverUrl)
        self._parsed_org_url = urlunparse((parsed_url[0],parsed_url[1],"","","",""))
        self._referer = parsed_url.netloc

    #----------------------------------------------------------------------
    @property
    def token(self):
        """gets the AGS server token"""
        return self._portalTokenHandler.servertoken(serverURL=self._serverUrl,
                                                    referer=self._referer)
    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method
    #
    @property
    def serverUrl(self):
        """gets/sets the server url"""
        return self._serverUrl
    #
    @serverUrl.setter
    def serverUrl(self, value):
        """gets/sets the server url"""
        if value.lower() != self._serverUrl.lower():
            self._serverUrl = value
    #
    @property
    def referer(self):
        """gets/sets the referer object"""
        return self._referer

    #----------------------------------------------------------------------
    @property
    def cookiejar(self):
        """gets the cookiejar"""

        return self._jar

    @cookiejar.setter
    def cookiejar(self, value):
        """gets/sets a cookiejar"""
        if value is not None:
            self._jar = value
    @property
    def handler(self):
        """gets/sets a handler"""

        return self._handler
    @handler.setter
    def handler(self, value):
        """gets/sets a handler"""
        if value is not None:
            self._handler = value

    @referer.setter
    def referer(self, value):
        """gets/sets the referer object"""
        if value is not None and \
           self._referer is not None and \
           self._referer.lower() != value.lower():
            self._referer = value
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        return False
########################################################################
class OAuthSecurityHandler(abstract.BaseSecurityHandler):
    """Handles AGOL OAuth Security
       Inputs:
          client_id - OAuth client key
          secret_id - OAuth secret key
          org_url - The url of that ArcGIS Organization.  This url is
           composed on the machine name and the instance name of the portal.
           For example:  http://myportal.mycompany.com/portal for a Portal
            for ArcGIS Server instance.
             - http://www.arcgis.com for ArcGIS Online
             - http://myOnlineOrg.maps.arcgis.com for ArcGIS Online, but the
               unique url for your org
          token_url - optional - url to where the token is obtained
          proxy_url - optional - proxy url as a string
          proxy_port - optional - proxy port as integer
       Output:
          OAuthSecurityHandler Class Object
    """
    _token = None
    _default_token_url = "https://www.arcgis.com/sharing/rest/oauth2/token/"
    _token_url = "https://www.arcgis.com/sharing/rest/oauth2/token/"
    _client_id = None
    _secret_id = None
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    _proxy_url = None
    _proxy_port = None
    _method = "OAUTH"
    #----------------------------------------------------------------------
    def __init__(self, client_id, secret_id, org_url,token_url=None,
                 proxy_url=None, proxy_port=None):
        """Constructor"""
        self._client_id = client_id
        self._secret_id = secret_id
        self._token_url = token_url
        self._org_url = org_url

        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._token_expires_on = datetime.datetime.now() + datetime.timedelta(seconds=_defaultTokenExpiration)
        self._initURL(token_url=token_url)

    #----------------------------------------------------------------------
    def _initURL(self, org_url=None,
                 token_url=None,
                 referer_url=None):
        """ sets proper URLs for AGOL """
        if org_url is not None and org_url != '':
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'http://' + org_url
            self._org_url = org_url
        if not self._org_url.startswith('http://') and not self._org_url.startswith('https://'):
            self._org_url = 'http://' + self._org_url

        if self._org_url.lower().find('/sharing/rest') > -1:
            self._url = self._org_url
        else:
            self._url = self._org_url + "/sharing/rest"

        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
            self._surl = self._url

        if token_url is None:
            self._token_url = self._surl + "/oauth2/token"
        else:
            self._token_url = token_url

        if referer_url is None:
            if not self._org_url.startswith('http://'):
                self._referer_url = self._org_url.replace('http://', 'https://')
            else:
                self._referer_url = self._org_url
        else:
            self._referer_url = referer_url
    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal
    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    @property
    def org_url(self):
        """ gets/sets the organization URL """
        return self._org_url
    #----------------------------------------------------------------------

    @property
    def referer_url(self):
        """ returns when the token was generated """
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ obtains a token from the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            self._generateForOAuthSecurity(self._client_id,
                                           self._secret_id,
                                           self._token_url)
        return self._token
    #----------------------------------------------------------------------
    @property
    def client_id(self):
        """ returns the client id """
        return self._client_id
    #----------------------------------------------------------------------
    @client_id.setter
    def client_id(self, value):
        """ sets the client id for oauth """
        self._token = None
        self._client_id = value
    #----------------------------------------------------------------------
    @property
    def secret_id(self):
        """ returns ***** for secret id """
        return "*****"
    #----------------------------------------------------------------------
    @secret_id.setter
    def secret_id(self, value):
        """ sets the secret id """
        self._token = None
        self._secret_id = value
    #----------------------------------------------------------------------
    @property
    def token_url(self):
        """ returns the token url """
        return self._token_url
    #----------------------------------------------------------------------
    @token_url.setter
    def token_url(self, value):
        """ sets the token url """
        self._token = None
        self._token_url = value
    #----------------------------------------------------------------------
    def resetTokenURLToDefault(self):
        """ resets the token url to the default url """
        self._token = None
        self._token_url = self._default_token_url
    #----------------------------------------------------------------------
    @property
    def tokenExperationDate(self):
        """ returns when the token is not valid """
        return self._token_expires_on
    #----------------------------------------------------------------------
    @property
    def tokenObtainedDate(self):
        """ returns when the token was generated """
        return self._token_created_on
    #----------------------------------------------------------------------
    def _generateForOAuthSecurity(self, client_id,
                                  secret_id, token_url=None):
        """ generates a token based on the OAuth security model """
        grant_type="client_credentials"
        if token_url is None:
            token_url = "https://www.arcgis.com/sharing/rest/oauth2/token"
        params = {
            "client_id" : client_id,
            "client_secret" : secret_id,
            "grant_type":grant_type,
            "f" : "json"
        }
        token = self._post(url=token_url,
                              param_dict=params,
                              securityHandler=None,
                              proxy_port=self._proxy_port,
                              proxy_url=self._proxy_url)

        if 'access_token' in token:
            self._token = token['access_token']
            self._expires_in = token['expires_in']
            self._token_created_on = datetime.datetime.now()
            self._token_expires_on = self._token_created_on + datetime.timedelta(seconds=int(token['expires_in']))
        else:
            self._token = None
            self._expires_in = None
            self._token_created_on = None
            self._token_expires_on = None
            #self._token_expires_on = None
########################################################################
class ArcGISTokenSecurityHandler(abstract.BaseSecurityHandler):
    """ handles ArcGIS Maps Token Base Security

    """
    _method = "TOKEN"
    _token = None
    _surl = None
    _org_url =None
    _url = None
    _referer_url = None
    _username = None
    _token_expires_on = None
    _expires_in = None
    _proxy_url = None
    _proxy_port = None
    _server_token = None
    _server_token_expires_on = None
    _server_token_created_on = None
    _server_expires_in = None
    _server_url = None
    _token_url = None
    #----------------------------------------------------------------------
    def __init__(self,proxy_url=None, proxy_port=None):
        """Constructor"""
        if arcpyFound == False:
            self._message = "ArcPy not available"
            self._valid = False
        else:
            self._proxy_port = proxy_port
            self._proxy_url = proxy_url
            self._token_expires_on = None
            self._initURL()
    #----------------------------------------------------------------------
    def _initURL(self):
        """ sets proper URLs for AGOL """

        token = self._getTokenArcMap()
        if 'error' in token:
            self._valid = False
            self._message = token['error']
        else:
            self._valid = True
            self._message = "Token Generated"
        self._org_url = arcpy.GetActivePortalURL()
        if self._org_url.lower().find('/sharing/rest') > -1:
            self._url = self._org_url
        else:
            self._url = self._org_url + "/sharing/rest"

        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
            self._surl  =  self._url

        url = '{}/portals/self'.format( self._url)

        parameters = {
            'f': 'json'
        }
        portal_info = self._post(url=url,
                                 param_dict=parameters,
                                 securityHandler=self,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)

        if 'user' in portal_info:
            if 'username' in portal_info['user']:
                self._username = portal_info['user']['username']


        results = self._get(url= self._surl + '/portals/info',
                               param_dict={'f':'json'},
                               proxy_port=self._proxy_port,
                               proxy_url=self._proxy_url)
        if 'authInfo' in results and 'tokenServicesUrl' in results['authInfo']:

            self._token_url = results['authInfo']['tokenServicesUrl']
        else:
            self._token_url = self._surl  + '/generateToken'


    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal
    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method
    #----------------------------------------------------------------------
    @property
    def org_url(self):
        """ gets/sets the organization URL """
        return self._org_url

    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username """
        return self._username

    #----------------------------------------------------------------------
    @property
    def tokenExperationDate(self):
        """ returns when the token is not valid """
        return self._token_expires_on

    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """ returns when the token was generated """
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ returns the token for the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            result = self._getTokenArcMap()
            if 'error' in result:
                self._valid = False
                self._message = result
            else:
                self._valid = True
                self._message = "Token Generated"
        return self._token
    #----------------------------------------------------------------------
    def _getTokenArcMap(self):
        token_response = arcpy.GetSigninToken()
        if token_response and 'token' in token_response:
            self._token = token_response['token']
            self._expires_in = token_response['expires']
            self._token_expires_on = datetime.datetime.fromtimestamp(token_response['expires'] /1000) - \
                datetime.timedelta(seconds=1)
            self._referer_url = token_response['referer']
            return self._token
        else:
            return {"error": "No valid token, please log in ArcMap"}

    #----------------------------------------------------------------------
    def servertoken(self,serverURL,referer):
        """ returns the server token for the server """
        if self._server_token is None or self._server_token_expires_on is None or \
           datetime.datetime.now() >= self._server_token_expires_on or \
           self._server_url != serverURL:
            self._server_url = serverURL
            result = self._generateForServerTokenSecurity(serverURL=serverURL,
                                                          token=self.token)
            if 'error' in result:
                self._valid = False
                self._message = result
            else:
                self._valid = True
                self._message = "Server Token Generated"
        return self._server_token
    #----------------------------------------------------------------------
    def _generateForServerTokenSecurity(self,
                                        serverURL,
                                        token,
                                        expiration=None):
        """ generates a token for a feature service """

        query_dict = {'serverURL':serverURL,
                      'token': token,
                      'expiration':str(_defaultTokenExpiration),
                      'f': 'json',
                      'request':'getToken'}
        if expiration is not None:
            query_dict['expiration'] = expiration

        server_token = self._post(url=self._token_url,
                                     param_dict=query_dict,
                                     securityHandler=None,
                                     proxy_port=self._proxy_port,
                                     proxy_url=self._proxy_url)
        if 'error' in server_token:
            self._server_token = None
            self._server_token_created_on = None
            self._server_token_expires_on = None
            self._server_expires_in = None

            return server_token

        else:
            self._server_token = server_token['token']
            self._server_token_created_on = datetime.datetime.now()

            self._server_token_expires_on = datetime.datetime.fromtimestamp(server_token['expires'] /1000) - \
                datetime.timedelta(seconds=1)
            self._server_expires_in = (self._server_token_expires_on - self._server_token_created_on).total_seconds()
            return server_token['token']

########################################################################
class AGOLTokenSecurityHandler(abstract.BaseSecurityHandler):
    """ handles ArcGIS Online Token Base Security
        username - required - username to access AGOL services
        password - required - password for username above
        org_url - The url of that ArcGIS Organization.  This url is
         composed on the machine name and the instance name of the portal.
         For example:  http://myportal.mycompany.com/portal for a Portal
         for ArcGIS Server instance.
          - http://www.arcgis.com for ArcGIS Online
          - http://myOnlineOrg.maps.arcgis.com for ArcGIS Online, but the
            unique url for your org
        token_url - optional - if URL is different than default AGOL token
                    url, then enter it here for AGOL token service.
        proxy_url - optional - if proxy is required to access internet, the
                    IP goes here.
        proxy_post - optional - if proxy is used and it's not port 90 enter
                     it here.
    """
    _token = None

    _surl = None
    _org_url ="http://www.arcgis.com"
    _url = "https://www.arcgis.com/sharing/rest"
    _parsed_org_url = "http://www.arcgis.com"
    _referer_url = None
    _method = "TOKEN"
    _username = None
    _password = None
    _token_url = None
    _default_token_url = 'https://arcgis.com/sharing/rest/generateToken'
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self,
                 username,
                 password,
                 org_url ="https://www.arcgis.com",
                 token_url=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._username = username
        self._password = password
        self._token_url = token_url
        self._org_url = org_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._token_expires_on = datetime.datetime.now() + datetime.timedelta(seconds=_defaultTokenExpiration)

        urlInfo = urlparse(org_url)

        if str(urlInfo.netloc).lower() == "www.arcgis.com"> -1:
            self._initURL(org_url=org_url,token_url=token_url)

            from ..manageorg import Administration
            admin = Administration(securityHandler=self)
            portalSelf = admin.portals.portalSelf
            urlInfo=urlInfo._replace(netloc= "%s.%s" % (portalSelf.urlKey, portalSelf.customBaseUrl))
            org_url = urlunparse(urlInfo)
            del portalSelf
            del admin
        self._initURL(org_url=org_url,token_url=token_url)
    #----------------------------------------------------------------------
    def _initURL(self, org_url=None,
                 token_url=None,
                 referer_url=None):
        """ sets proper URLs for AGOL """
        if org_url is not None and org_url != '':
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'http://' + org_url
            self._org_url = org_url
        if not self._org_url.startswith('http://') and not self._org_url.startswith('https://'):
            self._org_url = 'http://' + self._org_url

        if self._org_url.lower().find('/sharing/rest') > -1:
            self._url = self._org_url
        else:
            self._url = self._org_url + "/sharing/rest"

        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
            self._surl  =  self._url

        if token_url is None:

            results = self._get(url= self._surl + '/info',
                                   param_dict={'f':'json'},
                                   proxy_port=self._proxy_port,
                                   proxy_url=self._proxy_url)
            if 'authInfo' in results and 'tokenServicesUrl' in results['authInfo']:

                self._token_url = results['authInfo']['tokenServicesUrl']
            else:
                self._token_url = self._surl  + '/generateToken'

        else:
            self._token_url = token_url
        parsed_url = urlparse(self._org_url)
        self._parsed_org_url = urlunparse((parsed_url[0],parsed_url[1],"","","",""))

        if referer_url is None:
            self._referer_url = parsed_url.netloc

                #if referer_url is None or \
            #referer_url.lower().find('www.arcgis.com') > -1:
            #self._referer_url = "arcgis.com"
        #else:
            #self._referer_url = referer_url
    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal

#----------------------------------------------------------------------
    def __getRefererUrl(self, url=None):
        """
        gets the referer url for the token handler
        """
        if url is None:
            url = "http://www.arcgis.com/sharing/rest/portals/self"
        params = {
            "f" : "json",
            "token" : self.token
        }
        val = self._get(url=url, param_dict=params,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        self._referer_url = "arcgis.com"#"http://%s.%s" % (val['urlKey'], val['customBaseUrl'])
        self._token = None
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method

    #----------------------------------------------------------------------
    @property
    def org_url(self):
        """ gets/sets the organization URL """
        return self._org_url
    #----------------------------------------------------------------------
    @org_url.setter
    def org_url(self, value):
        """ gets/sets the organization URL """
        if value is not None:
            self._org_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username """
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, username):
        """ sets the username """
        self._token = None
        self._username = username
    #----------------------------------------------------------------------
    @property
    def password(self):
        """ returns **** for the password """
        return "****"
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """ sets the password """
        self._token = None
        self._password = value
    #----------------------------------------------------------------------
    @property
    def token_url(self):
        """ returns the token url """
        if self._token_url is None:
            return self._default_token_url
        return self._token_url
    #----------------------------------------------------------------------
    @token_url.setter
    def token_url(self, value):
        """ sets the token url """
        self._token = None
        self._token_url = value
    #----------------------------------------------------------------------
    def resetTokenURLToDefault(self):
        """ resets the token url to the default url """
        self._token = None
        self._token_url = self._default_token_url
    #----------------------------------------------------------------------
    @property
    def tokenExperationDate(self):
        """ returns when the token is not valid """
        return self._token_expires_on
    #----------------------------------------------------------------------
    @property
    def tokenObtainedDate(self):
        """ returns when the token was generated """
        return self._token_created_on
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """ returns when the token was generated """
        return self._referer_url
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ returns the token for the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            result = self._generateForTokenSecurity(username=self._username,
                                                    password=self._password,
                                                    referer=self._referer_url,
                                                    tokenUrl=self._token_url)
            if 'error' in result:
                self._valid = False
                self._message = result
            else:
                self._valid = True
                self._message = "Token Generated"
        return self._token
    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self,
                                  username,
                                  password,
                                  referer=None,
                                  tokenUrl=None,
                                  expiration=None,
                                  proxy_url=None,
                                  proxy_port=None):
        """ generates a token for a feature service """
        if referer is None:
            referer = self._referer_url
        if tokenUrl is None:
            tokenUrl  = self._token_url

        query_dict = {'username': self._username,
                      'password': self._password,
                      'expiration': str(_defaultTokenExpiration),
                      'referer': referer,
                      'f': 'json'}
        if expiration is not None:
            query_dict['expiration'] = str(expiration)
        self._token_created_on = datetime.datetime.now()
        token = self._post(url=tokenUrl,
                              param_dict=query_dict,
                              securityHandler=None,
                              proxy_port=self._proxy_port,
                              proxy_url=self._proxy_url)
        if 'error' in token:
            self._token = None
            return token


        self._token_expires_on = datetime.datetime.fromtimestamp(token['expires'] / 1000) - \
            datetime.timedelta(seconds=10)

        #if token['expires'] > 86400:
            #seconds = 86400
        #else:
            #seconds = int(token['expires'])
        #self._token_expires_on = self._token_created_on + \
            #datetime.timedelta(seconds=seconds)
        if "token" not in token:
            self._token = None
            return None
        else:
            httpPrefix = self._url
            if token['ssl'] == True:
                httpPrefix = self._surl
            self._token = token['token']
            return token['token'], httpPrefix
#########################################################################
class AGSTokenSecurityHandler(abstract.BaseSecurityHandler):
    """ handles ArcGIS Server Security
        username - required - person accessing server
        password - required - login credential
        token_url - required - URL to generate a token on server
        proxy_url - optional - IP of proxy
        proxy_port - optional - port of the proxy server
    """
    _method = "TOKEN"
    _token = None
    _username = None
    _password = None
    _token_url = None
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    _proxy_url = None
    _proxy_port = None
    _default_token_url = None
    _referer_url = None
    _org_url = None

    #----------------------------------------------------------------------
    def __init__(self, username, password,
                 org_url=None,
                 token_url=None,
                 proxy_url=None, proxy_port=None):
        """Constructor"""
        self._username = username
        self._password = password
        self._token_url = token_url
        self._org_url = org_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._token_expires_on = datetime.datetime.now() + datetime.timedelta(seconds=_defaultTokenExpiration)
        if token_url is None and \
           not org_url is None:

            params = {"f":"json"}
            parts = urlparse(org_url)
            p = parts.path[1:].strip().split('/')[0]
            url = "%s://%s/%s/rest/info" % (parts.scheme, parts.netloc, p)
            result = self._get(url=url, param_dict=params,
                                  securityHandler=None,
                                  proxy_url=proxy_url,
                                  proxy_port=proxy_port)
            if 'authInfo' in result and \
               'tokenServicesUrl' in result['authInfo']:
                self._token_url = result['authInfo']['tokenServicesUrl']
            else:
                raise Exception("Cannot determine the token url, please pass that parameter.")

    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username """
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, username):
        """ sets the username """
        self._token = None
        self._username = username
    #----------------------------------------------------------------------
    @property
    def password(self):
        """ returns **** for the password """
        return "****"
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """ sets the password """
        self._token = None
        self._password = value
    #----------------------------------------------------------------------
    @property
    def token_url(self):
        """ returns the token url """
        return self._token_url
    #----------------------------------------------------------------------
    @token_url.setter
    def token_url(self, value):
        """ sets the token url """
        self._token = None
        self._token_url = value
    #----------------------------------------------------------------------
    @property
    def tokenExperationDate(self):
        """ returns when the token is not valid """
        return self._token_expires_on
    #----------------------------------------------------------------------
    @property
    def tokenObtainedDate(self):
        """ returns when the token was generated """
        return self._token_created_on
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ returns the token for the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            self._generateForTokenSecurity(username=self._username,
                                           password=self._password,
                                           tokenUrl=self._token_url)
        return self._token
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """ returns when the token was generated """
        return self._referer_url
    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self,
                                  username, password,
                                  tokenUrl, expiration=None):
        """ generates a token for a feature service """
        query_dict = {'username': username,
                      'password': password,
                      'expiration': str(_defaultTokenExpiration),
                      'client': 'requestip',
                      'f': 'json'}
        if expiration is not None:
            query_dict['expiration'] = expiration
        token = self._post(url=tokenUrl,
                              param_dict=query_dict,
                              securityHandler=None,
                              proxy_port=self._proxy_port,
                              proxy_url=self._proxy_url)
        if "token" not in token:
            self._token = None
            self._token_created_on = None
            self._token_expires_on = None
            self._expires_in = None
            return None
        else:
            self._token = token['token']
            self._token_created_on = datetime.datetime.now()
            #if token['expires'] > 86400:
                #seconds = 86400
            #else:
                #seconds = int(token['expires'])
            #self._token_expires_on = self._token_created_on + datetime.timedelta(seconds=seconds)
            self._token_expires_on = datetime.datetime.fromtimestamp(int(token['expires']) /1000) - datetime.timedelta(seconds=1)
            self._expires_in = (self._token_expires_on - self._token_created_on).total_seconds()
            return token['token']
########################################################################
class PortalTokenSecurityHandler(abstract.BaseSecurityHandler):
    """
    Handles connection to a Portal Site

    Inputs:
       username - name of the user
       password - password for user
       org_url - The url of that ArcGIS Organization.  This url is
         composed on the machine name and the instance name of the portal.
         For example:  http://myportal.mycompany.com/portal for a Portal
         for ArcGIS Server instance.
          - http://www.arcgis.com for ArcGIS Online
          - http://myOnlineOrg.maps.arcgis.com for ArcGIS Online, but the
            unique url for your org
       proxy_url - URL of the proxy
       proxy_port - proxy port
    """
    _token = None
    _server_token = None
    _server_token_expires_on = None
    _server_token_created_on = None
    _server_expires_in = None
    _server_url = None
    _org_url = None
    _url = None
    _surl = None
    _parsed_org_url = None
    _username = None
    _password = None
    _proxy_port = None
    _proxy_url = None
    _token_url = None
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    _method = "TOKEN"
    #Added for testing
    _handler = None
    _jar = None

    def __init__(self,
                 username,
                 password,
                 org_url,
                 token_url=None,
                 proxy_url=None,
                 proxy_port=None,
                 handler=None,
                 jar=None):
        """Constructor"""
        self._org_url = org_url
        self._username = username
        self._password = password

        self._token_url = token_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._token_expires_on = datetime.datetime.now() + datetime.timedelta(seconds=_defaultTokenExpiration)

        self._jar = jar
        self._handler = handler

        self._initURL(org_url=org_url, token_url=token_url,
                      referer_url=None)
    #----------------------------------------------------------------------

    def _initURL(self, org_url=None,
                 token_url=None,
                 referer_url=None):
        """ sets proper URLs for AGOL """
        if org_url is not None and org_url != '':
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'http://' + org_url
            self._org_url = org_url
        if not self._org_url.startswith('http://') and not self._org_url.startswith('https://'):
            self._org_url = 'http://' + self._org_url

        if self._org_url.lower().find('/sharing/rest') > -1:
            self._url = self._org_url
            self._org_url = str(self._org_url).replace('/sharing/rest','')
        else:
            self._url = self._org_url + "/sharing/rest"


        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
            self._surl  =  self._url

        if token_url is None:
            results = self._get(url= self._surl + '/portals/info',
                                param_dict={'f':'json'},
                                securityHandler=None,
                                proxy_port=self._proxy_port,
                                proxy_url=self._proxy_url)
            if 'authInfo' in results and 'tokenServicesUrl' in results['authInfo']:

                self._token_url = results['authInfo']['tokenServicesUrl']
            else:
                self._token_url = self._surl  + '/generateToken'

        else:
            self._token_url = token_url

        parsed_url = urlparse(self._org_url)
        self._parsed_org_url = urlunparse((parsed_url[0],parsed_url[1],"","","",""))

        if referer_url is None:

            self._referer_url = parsed_url.netloc

    _is_portal = None
    #----------------------------------------------------------------------
    @property
    def is_portal(self):
        if self._is_portal is None:
            self.check_portal()
        return self._is_portal
    #----------------------------------------------------------------------
    def check_portal(self):
        from ..manageorg import Administration

        admin = Administration(url=self._org_url,
                               securityHandler=self)
        portal = admin.portals.portalSelf

        self._is_portal = portal.isPortal
    #----------------------------------------------------------------------
    @property
    def method(self):
        """returns the handler method"""
        return self._method

    #----------------------------------------------------------------------
    @property
    def org_url(self):
        """ gets/sets the organization URL """
        return self._org_url
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """gets the proxy url"""
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy_url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """ gets the proxy port """
        return self._proxy_port
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username """
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, username):
        """ sets the username """
        self._token = None
        self._username = username
    #----------------------------------------------------------------------
    @property
    def password(self):
        """ returns **** for the password """
        return "****"
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """ sets the password """
        self._token = None
        self._password = value
    #----------------------------------------------------------------------
    @property
    def token_url(self):
        """ returns the token url """
        return self._token_url
    #----------------------------------------------------------------------
    @token_url.setter
    def token_url(self, value):
        """ sets the token url """
        self._token = None
        self._token_url = value
    #----------------------------------------------------------------------
    @property
    def tokenExperationDate(self):
        """ returns when the token is not valid """
        return self._token_expires_on
    #----------------------------------------------------------------------
    @property
    def tokenObtainedDate(self):
        """ returns when the token was generated """
        return self._token_created_on
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """ returns when the token was generated """
        return self._referer_url
    #----------------------------------------------------------------------

    @property
    def token(self):
        """ returns the token for the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            result = self._generateForTokenSecurity(username=self._username,
                                                    password=self._password,
                                                    tokenUrl=self._token_url)
            if 'error' in result:
                self._valid = False
                self._message = result
            else:
                self._valid = True
                self._message = "Token Generated"
        return self._token

    #----------------------------------------------------------------------
    @property
    def cookiejar(self):
        """gets the cookiejar"""

        return self._jar
    #----------------------------------------------------------------------
    @cookiejar.setter
    def cookiejar(self, value):
        """gets/sets a cookiejar"""
        if value is not None:
            self._jar = value

    #----------------------------------------------------------------------
    @property
    def handler(self):
        """gets/sets a handler"""
        return self._handler
    #----------------------------------------------------------------------
    @handler.setter
    def handler(self, value):
        """gets/sets a handler"""
        if value is not None:
            self._handler = value
    #----------------------------------------------------------------------
    def servertoken(self,serverURL,referer):
        """ returns the server token for the server """
        if self._server_token is None or self._server_token_expires_on is None or \
           datetime.datetime.now() >= self._server_token_expires_on or \
           self._server_url != serverURL:
            self._server_url = serverURL
            result = self._generateForServerTokenSecurity(serverURL=serverURL,
                                                          token=self.token,
                                                          tokenUrl=self._token_url,
                                                          referer=referer)
            if 'error' in result:
                self._valid = False
                self._message = result
            else:
                self._valid = True
                self._message = "Server Token Generated"
        return self._server_token

    #----------------------------------------------------------------------
    def _generateForServerTokenSecurity(self,
                                        serverURL,
                                        token,
                                        tokenUrl,
                                        referer,
                                        expiration=None
                                        ):
        """ generates a token for a feature service """

        query_dict = {'serverURL':serverURL,
                      'token': token,
                      'expiration':str(_defaultTokenExpiration),
                      'f': 'json',
                      'request':'getToken',
                      'referer':referer}
        if expiration is not None:
            query_dict['expiration'] = expiration
        secHandler = None

        if self.cookiejar is not None:
            secHandler = self
            if secHandler is not None:
                secHandler._method = "HANDLER"

        server_token = self._post(url=tokenUrl,
                                  param_dict=query_dict,
                                  securityHandler=secHandler,
                                  proxy_port=self._proxy_port,
                                  proxy_url=self._proxy_url)
        if self.cookiejar is not None:
            if secHandler is not None:
                secHandler._method = "TOKEN"

        if 'error' in server_token:
            self._server_token = None
            self._server_token_created_on = None
            self._server_token_expires_on = None
            self._server_expires_in = None

            return server_token

        else:
            self._server_token = server_token['token']
            self._server_token_created_on = datetime.datetime.now()

            self._server_token_expires_on = datetime.datetime.fromtimestamp(server_token['expires'] /1000) - \
                datetime.timedelta(seconds=1)
            self._server_expires_in = (self._server_token_expires_on - self._server_token_created_on).total_seconds()
            return server_token['token']

    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self,
                                  username, password,
                                  tokenUrl,
                                  expiration=None):
        """ generates a token for a feature service """
        query_dict = {'username': username,
                      'password': password,
                      'expiration':str(_defaultTokenExpiration),
                      'client': 'requestip',
                      'f': 'json'}
        if expiration is not None:
            query_dict['expiration'] = expiration

        secHandler = None
        if self.cookiejar is not None:
            secHandler = self
            if secHandler is not None:
                secHandler._method = "HANDLER"
        token = self._post(url=tokenUrl,
                           param_dict=query_dict,
                           securityHandler=secHandler,
                           proxy_port=self._proxy_port,
                           proxy_url=self._proxy_url)
        if self.cookiejar is not None:
            if secHandler is not None:
                secHandler._method = "TOKEN"
        if 'error' in token:
            self._token = None
            self._token_created_on = None
            self._token_expires_on = None
            self._expires_in = None

            return token
        elif 'status' in token:
            self._token = None
            self._token_created_on = None
            self._token_expires_on = None
            self._expires_in = None
            #print token['message']
            return token

        else:
            self._token = token['token']
            self._token_created_on = datetime.datetime.now()
            self._token_expires_on = datetime.datetime.fromtimestamp(token['expires'] /1000) - \
                datetime.timedelta(seconds=1)
            self._expires_in = (self._token_expires_on - self._token_created_on).total_seconds()
            return token['token']

    #----------------------------------------------------------------------
    def portalServerHandler(self, serverUrl, username=None):
        """
        returns a handler to access a federated server

        serverUrl - url to the server. Example:
                    https://server.site.com/arcgis
        username - the portal site username. if None is passed, it obtains
         it from the portal properties
        Outout:
          returns a PortalServerSecurityHandler object

        Usage:
        >>> # access the administration site
        >>> serverUrl="https://mysite.site.com/arcgis"
        >>> newSH = sh.portalServerHandler(serverUrl=serverUrl,
                                           username=None)
        >>> agsAdmin = AGSAdministration(url=serverUrl, securityHandler=newSH)
        >>> print agsAdmin.info
        >>> # access a secure service from portal handler
        >>> msUrl = "https://mysite.site.com:6443/arcgis/rest/services/SampleWorldCities/MapServer"
        >>> ms = arcrest.ags.MapService(url=msUrl, securityHandler=newSH)
        >>> print ms.mapName
        """

        pssh = PortalServerSecurityHandler(tokenHandler=self,
                                           serverUrl=serverUrl,
                                           referer=self._referer_url)


        return pssh
