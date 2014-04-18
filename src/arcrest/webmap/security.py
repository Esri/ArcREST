import base
import json
import urllib
import datetime
########################################################################
class OAuthSecurityHandler(base.BaseSecurityHandler):
    """Handles AGOL OAuth Security
       Inputs:
          client_id - OAuth client key
          secret_id - OAuth secret key
          token_url - optional - url to where the token is obtained
       Output:
          OAuthSecurityHandler Class Object
    """
    _token = None
    _default_token_url = "https://www.arcgis.com/sharing/oauth2/token"
    _token_url = "https://www.arcgis.com/sharing/oauth2/token"
    _client_id = None
    _secret_id = None
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    #----------------------------------------------------------------------
    def __init__(self, client_id, secret_id, token_url=None):
        """Constructor"""
        self._client_id = client_id
        self._secret_id = secret_id
        self._token_url = token_url
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
            token_url = "https://www.arcgis.com/sharing/oauth2/token"
        params = {
            "client_id" : client_id,
            "client_secret" : secret_id,
            "grant_type":grant_type,
            "f" : "json"
        }
        token = self._do_get(url=token_url, param_dict=params)

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
########################################################################
class AGOLTokenSecurityHandler(base.BaseSecurityHandler):
    """"""
    _token = None
    _username = None
    _password = None
    _token_url = None
    _default_token_url = 'https://arcgis.com/sharing/rest/generateToken'
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    #----------------------------------------------------------------------
    def __init__(self, username, password, token_url=None):
        """Constructor"""
        self._username = username
        self._password = password
        self._token_url = token_url
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
    def token(self):
        """ returns the token for the site """
        if self._token is None or \
           datetime.datetime.now() >= self._token_expires_on:
            self._generateForTokenSecurity(username=self._username,
                                           password=self._password,
                                           referer=None,
                                           tokenURL=self._token_url)
        return self._token
    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self, username, password,
                                 referer=None, tokenURL=None,
                                 expiration=None):
        """ generates a token for a feature service """
        if referer is None:
            referer='https://www.arcgis.com'
        if tokenURL is None:
            tokenURL  = 'https://arcgis.com/sharing/rest/generateToken'
        query_dict = {'username': username,
                      'password': password,
                      'expiration': str(60),
                      'referer': referer,
                      'f': 'json'}
        if expiration is not None:
            query_dict['expiration'] = expiration
        token = self._do_post(url=tokenURL, param_dict=query_dict)
        if "token" not in token:
            self._token = None
            self._token_created_on = None
            self._token_expires_on = None
            self._expires_in = None
            return None, None
        else:
            httpPrefix = "http://www.arcgis.com/sharing/rest"
            if token['ssl'] == True:
                httpPrefix = "https://www.arcgis.com/sharing/rest"
            self._token = token['token']
            self._token_created_on = datetime.datetime.now()
            if token['expires'] > 86400:
                seconds = 86400
            else:
                seconds = int(token['expires'])
            self._token_expires_on = self._token_created_on + datetime.timedelta(seconds=seconds)
            self._expires_in = token['expires']
            return token['token'], httpPrefix
########################################################################
class AGSTokenSecurityHandler(base.BaseSecurityHandler):
    """"""
    _token = None
    _username = None
    _password = None
    _token_url = None
    _token_created_on = None
    _token_expires_on = None
    _expires_in = None
    #----------------------------------------------------------------------
    def __init__(self, username, password, token_url):
        """Constructor"""
        self._username = username
        self._password = password
        self._token_url = token_url
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
                                           tokenURL=self._token_url)
        return self._token
    #----------------------------------------------------------------------
    def _generateForTokenSecurity(self,
                                  username, password,
                                  tokenURL, expiration=None):
        """ generates a token for a feature service """
        query_dict = {'username': username,
                      'password': password,
                      'client': 'requestip',
                      'f': 'json'}
        if expiration is not None:
            query_dict['expiration'] = expiration
        token = self._do_post(url=tokenURL, param_dict=query_dict)
        if "token" not in token:
            self._token = None
            self._token_created_on = None
            self._token_expires_on = None
            self._expires_in = None
            return None
        else:
            self._token = token['token']
            self._token_created_on = datetime.datetime.now()
            if token['expires'] > 86400:
                seconds = 86400
            else:
                seconds = int(token['expires'])
            self._token_expires_on = self._token_created_on + datetime.timedelta(seconds=seconds)
            self._expires_in = token['expires']
            return token['token']