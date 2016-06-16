"""
Login class to the site or server.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .web.connection import _connection
from .security import AGOLTokenSecurityHandler, AGSTokenSecurityHandler
from .security import PortalTokenSecurityHandler, PKISecurityHandler
from .security import LDAPSecurityHandler, NTLMSecurityHandler, hasNTLM
from .security import OAuthSecurityHandler
from ..packages.six.moves.urllib_parse import urlparse
from ..packages.six.moves.urllib.error import HTTPError

from collections import OrderedDict
import logging
_log = logging.getLogger(__name__)
__version__ = "4.0.0"
class SiteConnection(object):
    """The SiteConnection object is the class that holds all the login
    information about the user, security method and holds the entry point
    to the web operations.
    """
    _verify_ssl = None
    _client_id = None
    _secret_id = None
    _logged_in = False
    _root = None
    _username = None
    _password = None
    _baseurl = None
    _key_file = None
    _cert_file = None
    _all_ssl = None
    _proxy_host = None
    _proxy_port = None
    _ensure_ascii = None
    _token = None
    _handler = None
    _security_method = None
    _ops = None
    _allowed_types = ["UNKNOWN", 'ANONYMOUS', "NONE",
                      'PKI', 'NTLM', 'OAUTH', "BUILT-IN"]
    _allowed_product_type = ["SERVER", "AGO", "AGOL",
                             "PORTAL", "SERVER", "AGS"]
    _securityHandler = None
    def __init__(self,
                 baseurl,
                 token_url=None,
                 product_type=None,
                 security_method=None,
                 username=None,
                 password=None,
                 key_file=None,
                 cert_file=None,
                 client_id=None,
                 secret_id=None,
                 expiration=60,
                 all_ssl=False,
                 referer=None,
                 proxy_host=None,
                 proxy_port=None,
                 ensure_ascii=True,
                 verify_ssl_certificates=False,
                 **kwargs):
        self._expiration = expiration
        self._ops = _connection(verify=verify_ssl_certificates)
        self._username = username
        self._password = password
        self._client_id = client_id
        self._secret_id = secret_id
        self._baseurl = baseurl
        self._key_file = key_file
        self._cert_file = cert_file
        self._all_ssl = all_ssl
        self._verify_ssl = verify_ssl_certificates
        if all_ssl:
            self._baseurl = self._baseurl.lower().replace("http://", "https://")
        self._proxy_url = proxy_host
        self._proxy_port = proxy_port
        self._ensure_ascii = ensure_ascii
        self._token = None
        self._token_url = token_url
        if product_type is None:
            product_type = self._check_product(baseurl)
        if referer:
            self._referer = referer
        else:
            self._referer = urlparse(baseurl).netloc
        self._useragent = 'ArcREST/' + __version__
        if proxy_host and proxy_port:
            purl = "%s:%s" % (proxy_host, proxy_port)
            self._ops.install_proxy(https=purl, http=purl)
        if username and password and \
           security_method is None:
            self._security_method = self._guess_security(username=username)
        elif cert_file and key_file:
            self._security_method = "PKI"
        elif client_id and secret_id:
            self._security_method = "OAUTH"
        elif username is None and \
             password is None and \
             cert_file is None and \
             key_file is None:
            security_method = "ANONYMOUS"
        elif security_method.upper() in self._allowed_types:
            self._security_method = security_method.upper()
        else:
            raise ValueError("Invalid security method: {}".format(security_method))
        if baseurl.lower().find('arcgis.com') > -1:
            product_type = "AGO"
        if product_type is None:
            self._product_type = "AGO"
        elif product_type.upper() in self._allowed_product_type:
            self._product_type = product_type.upper()
        else:
            raise ValueError("Invalid product type: {}".format(product_type))
        self.login()
    #----------------------------------------------------------------------
    def _check_product(self, baseurl):
        """
        determines if the product is portal, arcgis online or arcgis server
        """
        if baseurl.lower().find("arcgis.com") > -1:
            return "AGO"
        elif baseurl.lower().find("/sharing/rest") > -1:
            return "PORTAL"
        else:
            #Brute Force Method
            root = baseurl.lower().split("/sharing")[0]
            parts = ['/rest/info', '/sharing/rest/info']
            params = {"f" : "json"}
            for pt in parts:
                try:
                    res = self._ops.get(url=root + pt, param_dict=params)
                except HTTPError as e:

                    code = e.getcode()
                    if code == 407:
                        raise Exception("Proxy Authentication Required")
                    res = ""
                if isinstance(res, dict) and \
                   "currentVersion" in res:
                    return "SERVER"
                del pt
                del res
        return "PORTAL"
    #----------------------------------------------------------------------
    def _guess_security(self, username):
        """
        When presented with a username if there is not domain, the value
        cannot be LDAP because LDAP and NTLM both require domain values.
        Therefore a value split on '\\' with a length of 1 would mean that
        the security used is BUILT-IN.
        LDAP and NTLM require domain"""
        if len(username.split("\\")) > 1:
            return "LDAP"
        else:
            return "BUILT-IN"
    #----------------------------------------------------------------------
    @property
    def security_method(self):
        """gets/sets the current security method"""
        return self._security_method
    #----------------------------------------------------------------------
    @security_method.setter
    def security_method(self, value):
        """gets/sets the current security method"""
        if str(value).upper() in self._allowed_types and \
           str(value).upper() != self._security_method:
            self._security_method = value
            self.logout()
    #----------------------------------------------------------------------
    @property
    def product_type(self):
        """gets/sets the product type"""
        return self._product_type
    #----------------------------------------------------------------------
    @product_type.setter
    def product_type(self, value):
        """gets/sets the product type"""
        if str(value).upper() in self._allowed_product_type and \
           str(value).upper() != str(self._product_type).upper():
            self._product_type = value
            self.logout()
    #----------------------------------------------------------------------
    def login(self):
        """ Logs into the portal using username/password. """
        self._securityHandler = None

        if self._product_type in ['AGOL', 'AGO'] and \
           self._security_method in ['PKI', 'LDAP', 'NTLM']:
            raise ValueError("This method is not supported by ArcGIS Online: {}".format(self._security_method))
        if self._security_method in ["NONE", "ANONYMOUS"]:
            self._securityHandler = None
        elif self._security_method == "BUILT-IN":
            if self._product_type in ["AGO", "AGOL"]:
                self._securityHandler = AGOLTokenSecurityHandler(connection=self._ops,
                                                                 username=self._username,
                                                                 password=self._password,
                                                                 token_url=self._token_url)
            elif self._product_type == "PORTAL":
                self._securityHandler = PortalTokenSecurityHandler(connection=self._ops,
                                                                   username=self._username,
                                                                   password=self._password,
                                                                   org_url=self._baseurl,
                                                                   token_url=self._token_url)
            elif self._product_type in ["SERVER", "AGS"]:
                self._securityHandler = AGSTokenSecurityHandler(connection=self._ops,
                                                                username=self._username,
                                                               password=self._password,
                                                               org_url=self._baseurl,
                                                               token_url=self._token_url)

        elif self._security_method == "PKI":
            self._securityHandler = PKISecurityHandler(connection=self._ops,
                                                       org_url=self._baseurl,
                                                       keyfile=self._key_file,
                                                       certificatefile=self._cert_file,
                                                       referer_url=self._referer)
        elif self._security_method == "LDAP":
            self._securityHandler = LDAPSecurityHandler(connection=self._ops,
                                                        org_url=self._baseurl,
                                                        username=self._username,
                                                        password=self._password,
                                                        referer_url=self._referer)
        elif self._security_method == "OAUTH":
            self._securityHandler = OAuthSecurityHandler(connection=self._ops,
                                                        client_id=self._client_id,
                                                        secret_id=self._secret_id,
                                                        org_url=self._baseurl,
                                                        token_url=self._token_url)
        elif self._security_method == "NTLM":
            if hasNTLM == False:
                raise NotImplementedError("NTLM is currently not supported, Please install ntlm3 to run this handler")
            else:
                self._securityHandler = NTLMSecurityHandler(connection=self._ops,
                                                            org_url=self._baseurl,
                                                            username=self._username,
                                                            password=self._password,
                                                            referer_url=self._referer)
        self._logged_in = True
        return self._securityHandler
    #----------------------------------------------------------------------
    def logout(self):
        """ Logs out of the portal. """
        self._logged_in = False
        self._token = None
        self._handler = None
        self._ops = _connection(verify=self._verify_ssl)
    #----------------------------------------------------------------------
    def is_logged_in(self):
        """ Returns true if logged into the portal. """
        return self._logged_in
    #----------------------------------------------------------------------
    @property
    def token(self):
        """gets the login token"""
        if self._securityHandler and \
           self._securityHandler.method == "TOKEN":
            return self._securityHandler.token
        else:
            return None
    #----------------------------------------------------------------------
    @property
    def baseUrl(self):
        """get/set the base url"""
        return self._baseurl
    #----------------------------------------------------------------------
    @baseUrl.setter
    def baseUrl(self, value):
        """get/set the base url"""
        if self._baseurl != value:
            self._baseurl = value
            self.logout()
            self.login()
    #----------------------------------------------------------------------
    @property
    def con(self):
        """gets the connection class"""
        self._ops._securityHandler = self._securityHandler
        return self._ops
    #----------------------------------------------------------------------
    def add_proxy(self, proxy_url, proxy_port, username, password):
        """sets the proxy for all web calls"""
        self._ops.install_proxy(https="{url}:{port}".format(url=proxy_url, port=proxy_port),
                                http="{url}:{port}".format(url=proxy_url, port=proxy_port),
                                username=username,
                                password=password)
    #----------------------------------------------------------------------
    def remove_proxies(self):
        """removes all the proxies for the web calls"""
        self._ops.remove_proxy_handler()
    #----------------------------------------------------------------------
    @property
    def useragent(self):
        """gets the product's useragent"""
        return self._ops.useragent
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    def get(self, path_or_url, params=None,
            ssl=False, compress=True,
            try_json=True, is_retry=False,
            use_ordered_dict=False,
            out_folder=None, file_name=None, **kwargs):
        """
        Performs a GET web operation.
        Inputs:
         path_or_url - this can be either a full url or part of a url. If
          part of a url is given without the scheme, then the baseURL used
          on object creation will be used.
         params - parameters to be past
        """
        add_header = None
        if self.is_logged_in == False:
            self.login()
        if self._securityHandler is None:
            self.login()
        if params is None:
            if "params" in kwargs:
                params = kwargs['params']
            elif "param_dict" in kwargs:
                params = kwargs['param_dict']
            else:
                params = {}
        if try_json:
            params['f'] = 'json'
        if path_or_url.find("http://") > -1 or \
           path_or_url.find("https://") > -1:
            url = path_or_url
        elif self._baseurl[-1] == '/' and \
             len(path_or_url) > 0:
            url = "{}{}".format(self._baseurl, path_or_url)
        elif  len(path_or_url) > 0:
            url = "{}/{}".format(self._baseurl, path_or_url)
        else:
            url = self._baseurl
        if ssl:
            url = url.replace("http://", "https://")
        if "out_folder" in kwargs:
            out_folder = kwargs["out_folder"]
        if "file_name" in kwargs:
            file_name = kwargs['file_name']
        if "additional_headers" in kwargs:
            add_header = kwargs['additional_headers']
        if isinstance(self._ops, _connection): pass
        res = self._ops.get(url=url,
                            param_dict=params,
                            securityhandler=self._securityHandler,
                            compress=compress,
                            out_folder=out_folder,
                            file_name=file_name,
                            additional_headers=add_header)
        if use_ordered_dict:
            if isinstance(res, dict):
                items = []
                for k,v in res.items():
                    items.append((k,v))
                return OrderedDict(items)
            else:
                return res
        else:
            return res
    #----------------------------------------------------------------------
    def post(self, path_or_url, postdata=None,
             files=None, ssl=False, compress=True,
             is_retry=False, use_ordered_dict=False,
             out_folder=None, file_name=None,
             **kwargs):
        """
        performs a basic POST operation on a given URL

        """
        add_headers = None
        if self.is_logged_in == False:
            self.login()
        if self._securityHandler is None:
            self.login()
        if postdata is None:
            params = {}
            if "params" in kwargs:
                params = kwargs['params']
            elif "param_dict" in kwargs:
                params = kwargs['param_dict']
        else:
            params = postdata
        if files is None:
            files = {}
        if path_or_url.find("http://") > -1 or \
           path_or_url.find("https://") > -1:
            url = path_or_url
        elif self._baseurl[-1] == '/':
            url = "{}{}".format(self._baseurl, path_or_url)
        else:
            url = "{}/{}".format(self._baseurl, path_or_url)
        if ssl:
            url = url.replace("http://", "https://")
        if "out_folder" in kwargs:
            out_folder = kwargs["out_folder"]
        if "file_name" in kwargs:
            file_name = kwargs['file_name']
        if "additional_headers" in kwargs:
            add_headers = kwargs['additional_headers']
        res = self._ops.post(url=url,
                             param_dict=params,
                             files=files,
                             securityhandler=self._securityHandler,
                             compress=compress,
                             out_folder=out_folder,
                             file_name=file_name,
                             additional_headers=add_headers)
        if use_ordered_dict:
            if isinstance(res, dict):
                items = []
                for k,v in res.items():
                    items.append((k,v))
                return OrderedDict(items)
            else:
                return res
        else:
            return res