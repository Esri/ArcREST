from __future__ import print_function

from arcrest import security
import arcrest
from arcrest.manageags import AGSAdministration
from arcrest.manageorg import Administration
from ...arcrest.packages import six
import six.moves.urllib as urllib
from six.moves.urllib.error import HTTPError
import os
import common
import copy

########################################################################
class securityhandlerhelper(object):
    """
        A number of different security handlers are suppoted by ArcGIS, this
        function simplifies the creation of the handlers.  A dict with the
        type of handler and information to created it is required to generate
        the handlers
    """
    _org_url = None
    _username = None
    _password = None
    _proxy_url = None
    _proxy_port = None
    _token_url = None
    _securityHandler = None
    _security_type = None
    _featureServiceFieldCase = None
    _keyfile = None
    _certificatefile = None
    _referer_url = None
    _client_id = None
    _secret_id = None
    _is_portal = False

    #----------------------------------------------------------------------
    def __init__(self, securityinfo):

        """Constructor
            A number of different security handlers are suppoted by ArcGIS, this
            function simplifies the creation of the handlers.  A dict with the
            type of handler and information to created it is required to generate
            the handlers

           Inputs:
              securityinfo - The dict with details to create the handler.  The
                        valid parameters are:
                            - security_type: Required, valid values are Portal,
                                NTLM, PKI, OAUTH, LDAP
                            - proxy_url: Optional, url for proxy server
                            - proxy_port: Optional, port for proxy server
                            - referer_url: Optional, url for referer
                            - token_url: Optional, url for token server
                            - username: Optional, Username for log in, not
                                required for all security types
                            - password: Optional, Password for log in, not
                                required for all security types
                            - certificatefile: Only required for PKI
                            - keyfile: Only required for PKI
                            - client_id: Only required for OAuth
                            - secret_id: Only required for OAuth
        """

        if not securityinfo is None:
            if isinstance(securityinfo,securityhandlerhelper):

                self._securityHandler = securityinfo.securityhandler
                self._username = securityinfo._username
                self._password = securityinfo._password
                self._proxy_url = securityinfo._proxy_url
                self._proxy_port = securityinfo._proxy_port
                self._token_url = securityinfo._token_url
                self._security_type = securityinfo._security_type
                self._featureServiceFieldCase = securityinfo._featureServiceFieldCase
                self._keyfile = securityinfo._keyfile
                self._certificatefile = securityinfo._certificatefile
                self._referer_url = securityinfo._referer_url
                self._client_id = securityinfo._client_id
                self._secret_id = securityinfo._secret_id
                self._is_portal = securityinfo._is_portal
                self._message = securityinfo._message
                self._valid = securityinfo._valid

                #self._securityHandler = securityinfo
                return
            else:
                pass
            if isinstance(securityinfo,str) and os.path.isfile(securityinfo):
                securityinfo = common.init_config_json(config_file=securityinfo)
                if 'Credentials' in securityinfo:
                    securityinfo = securityinfo['Credentials']

            if 'security_type' in securityinfo:
                self._security_type = securityinfo['security_type']
            else:
                self._message = 'Security type not specified'
                self._valid = False
                return

            if 'proxy_url' in securityinfo:
                self._proxy_url = securityinfo['proxy_url']

            if 'proxy_port' in securityinfo:
                self._proxy_port = securityinfo['proxy_port']

            if 'referer_url' in securityinfo:
                self._referer_url = securityinfo['referer_url']

            if 'token_url' in securityinfo and securityinfo['token_url'] is not None:
                self._token_url = securityinfo['token_url']
                if not self._token_url.startswith('http://') and \
                   not self._token_url.startswith('https://'):
                    self._token_url = 'https://' + self._token_url

            if 'org_url' in securityinfo and securityinfo['org_url'] is not None:
                self._org_url = securityinfo['org_url']
                if not self._org_url.startswith('http://') and not self._org_url.startswith('https://'):
                    self._org_url = 'http://' + self._org_url

            if 'username' in securityinfo:
                self._username = securityinfo['username']
            if 'password' in securityinfo:
                self._password = securityinfo['password']

            if 'certificatefile' in securityinfo:
                self._certificatefile = securityinfo['certificatefile']
            if 'keyfile' in securityinfo:
                self._keyfile = securityinfo['keyfile']

            if 'client_id' in securityinfo:
                self._client_id = securityinfo['client_id']
            if 'secret_id' in securityinfo:
                self._secret_id = securityinfo['secret_id']

            if str(securityinfo['security_type']).upper() == 'ArcGIS'.upper():

                self._securityHandler = security.ArcGISTokenSecurityHandler(proxy_url=self._proxy_url,
                                            proxy_port=self._proxy_port)

                self._org_url = self._securityHandler.org_url
                self._username = self._securityHandler.username
                self._valid = True
                self._message = "ArcGIS security handler created"
            elif str(securityinfo['security_type']).upper() == 'Portal'.upper() or \
                 str(securityinfo['security_type']).upper() == 'AGOL'.upper():
                if self._org_url is None or self._org_url == '':
                    self._org_url = 'http://www.arcgis.com'
                if self._username is None or self._username == '' or \
                    self._password is None or self._password == '':
                    self._message = "No username or password, no security handler generated"
                    self._valid = True
                else:
                    if self._org_url is None or '.arcgis.com' in self._org_url:
                        self._securityHandler = security.AGOLTokenSecurityHandler(username=self._username,
                                                                                 password=self._password,
                                                                                 org_url=self._org_url,
                                                                                 token_url=self._token_url,
                                                                                 proxy_url=self._proxy_url,
                                                                                 proxy_port=self._proxy_port)
                        self._message = "ArcGIS Online security handler created"
                    else:
                        self._securityHandler = security.PortalTokenSecurityHandler(username=self._username,
                                                                                   password=self._password,
                                                                                   org_url=self._org_url,
                                                                                   proxy_url=self._proxy_url,
                                                                                   proxy_port=self._proxy_port)
                        self._message = "Portal security handler created"

            elif str(securityinfo['security_type']).upper() == 'NTLM'.upper():
                if self._username is None or self._username == '' or \
                    self._password is None or self._password == '':
                    self._message = "Username and password required for NTLM"
                    self._valid = False
                else:
                    self._securityHandler = security.NTLMSecurityHandler(username=self._username,
                                                                        password=self._password,
                                                                        org_url=self._org_url,
                                                                        proxy_url=self._proxy_url,
                                                                        proxy_port=self._proxy_port,
                                                                        referer_url=self._referer_url)
                    self._message = "NTLM security handler created"
            elif str(securityinfo['security_type']).upper() == 'LDAP'.upper():
                if self._username is None or self._username == '' or \
                    self._password is None or self._password == '':
                    self._message = "Username and password required for LDAP"
                    self._valid = False
                else:
                    self._securityHandler = security.LDAPSecurityHandler(username=self._username,
                                                                        password=self._password,
                                                                        org_url=self._org_url,
                                                                        proxy_url=self._proxy_url,
                                                                        proxy_port=self._proxy_port,
                                                                        referer_url=self._referer_url)
                    self._message = "LDAP security handler created"
            elif str(securityinfo['security_type']).upper() == 'PKI'.upper():
                if self._keyfile is None or self._keyfile == '' or \
                    self._certificatefile is None or self._certificatefile == '':
                    self._message = "Key file and certification file required for PKI"
                    self._valid = False
                else:
                    self._securityHandler = security.PKISecurityHandler(keyfile = self._keyfile,
                                                                        certificatefile = self._certificatefile,
                                                                        org_url=self._org_url,
                                                                        proxy_url=self._proxy_url,
                                                                        proxy_port=self._proxy_port,
                                                                        referer_url=self._referer_url)
                    self._message = "PKI security handler created"
            elif str(securityinfo['security_type']).upper() == 'OAUTH'.upper():
                if self._secret_id is None or self._secret_id == '' or \
                    self._client_id is None or self._client_id == '':
                    self._message = "client_id and secret_id required for OAUTH"
                    self._valid = False
                else:
                    self._securityHandler = security.OAuthSecurityHandler(client_id=self._client_id,
                                                                         secret_id = self._secret_id,
                                                                         org_url=self._org_url,
                                                                         proxy_url=self._proxy_url,
                                                                         proxy_port=self._proxy_port)

                    self._message = "OAuth security handler created"
            else:
                print ("No valid security type set")
                self._message = "No valid security type set"
            if self._securityHandler is not None:

                admin = Administration(url=self._org_url,
                                       securityHandler=self._securityHandler)

                try:
                    portal = admin.portals.portalSelf
                    for hostingServer in portal.featureServers:
                        if isinstance(hostingServer, AGSAdministration):
                            try:
                                serData = hostingServer.data

                                dataItems = serData.rootDataItems
                                if 'rootItems' in dataItems:
                                    for rootItem in dataItems['rootItems']:
                                        if rootItem == '/enterpriseDatabases':
                                            rootItems = serData.findDataItems(ancestorPath=rootItem,type='fgdb,egdb')
                                            if not rootItems is None and 'items' in rootItems:
                                                for item in rootItems['items']:
                                                    if 'info' in item:
                                                        if 'isManaged' in item['info'] and item['info']['isManaged'] == True:
                                                            conStrDic = {}
                                                            conStr = item['info']['connectionString'].split(";")
                                                            for conStrValue in conStr:
                                                                spltval = conStrValue.split("=")
                                                                conStrDic[spltval[0]] = spltval[1]
                                                            if 'DBCLIENT' in conStrDic:
                                                                if str(conStrDic['DBCLIENT']).upper() == 'postgresql'.upper():
                                                                    self._featureServiceFieldCase = 'lower'
                            except HTTPError as err:
                                if err.code == 403:
                                    print ("Admistrative access denied, unable to check if hosting servers")
                                else:
                                    print (err)
                            except Exception as e:
                                print (e)

                except HTTPError as err:
                    if err.code == 403:
                        print ("Admistrative access denied, unable to check if hosting servers")
                    else:
                        print (err)
                except Exception as e:
                    print (e)

                if 'error' in self._securityHandler.message:
                    self._message = self._securityHandler.message
                    self._valid = False

                else:
                    if self._securityHandler.message is not None:
                        self._message = self._securityHandler.message
                    self._valid = True
        else:
            self._message = 'Security info not set'
            self._valid = True
    #----------------------------------------------------------------------
    def dispose(self):
        self._username = None
        self._password = None
        self._org_url = None
        self._proxy_url = None
        self._proxy_port = None
        self._token_url = None
        self._securityHandler = None
        self._valid = None
        self._message = None

        del self._username
        del self._password
        del self._org_url
        del self._proxy_url
        del self._proxy_port
        del self._token_url
        del self._securityHandler
        del self._valid
        del self._message
    #----------------------------------------------------------------------
    @property
    def message(self):
        """ returns any messages """
        return self._message
    #----------------------------------------------------------------------
    @message.setter
    def message(self,message):
        """ returns any messages """
        self._message = message
    #----------------------------------------------------------------------
    @property
    def valid(self):
        """ returns boolean wether handler is valid """
        return self._valid
    #----------------------------------------------------------------------
    @valid.setter
    def valid(self,valid):
        """ returns boolean wether handler is valid """
        self._valid = valid
    #----------------------------------------------------------------------
    @property
    def securityhandler(self):
        """ returns the security hanlder """
        return self._securityHandler
    #@property
    #def is_portal(self):
        #return self._is_portal
