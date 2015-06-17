

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
from .. import common 
import gc


########################################################################
class baseToolsClass(object):
    _org_url = None
    _username = None
    _password = None
    _proxy_url = None
    _proxy_port = None
    _token_url = None
    _securityHandler = None
    _featureServiceFieldCase = None
    #----------------------------------------------------------------------
    def __init__(self,
                 username=None,
                 password=None,
                 org_url=None,
                 token_url = None,
                 proxy_url=None,
                 proxy_port=None,
                 use_arcgis_creds=None):

        """Constructor"""
       
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if use_arcgis_creds == True:
            self._securityHandler = arcrest.ArcGISTokenSecurityHandler(proxy_url=self._proxy_url,
                                                                     proxy_port=self._proxy_port)
            token = self._securityHandler.token     
            self._org_url = self._securityHandler.org_url
            self._username = self._securityHandler.username
            self._valid = True
        else:
            self._token_url = token_url
            self._org_url = org_url
            self._username = username
            self._password = password
            if self._org_url is None or self._org_url =='':
                self._org_url = 'http://www.arcgis.com'
            if self._username == "" or self._password == "":
                self._message = "No username or password, no security handler generated"
                self._valid = True
            else:        
                if self._org_url is None or '.arcgis.com' in self._org_url:
                    self._securityHandler = arcrest.AGOLTokenSecurityHandler(username=self._username,
                                                                      password=self._password,
                                                                      org_url=self._org_url,
                                                                      token_url=self._token_url,
                                                                      proxy_url=self._proxy_url,
                                                                      proxy_port=self._proxy_port)
                    token = self._securityHandler.token
              
    
                        #if self._securityHandler.message['error']['code'] == 400:
        
                            #self._securityHandler = arcrest.OAuthSecurityHandler(client_id='',
                                                                                 #secret_id='',
                                                                                 #org_url=self._org_url,
                                                                                 #proxy_url=self._proxy_url,
                                                                                 #proxy_port=self._proxy_port)
                            #token = self._securityHandler.token
                else:
        
                    self._securityHandler = arcrest.PortalTokenSecurityHandler(username=self._username,
                                                                      password=self._password,
                                                                      org_url=self._org_url,
                                                                      proxy_url=self._proxy_url,
                                                                      proxy_port=self._proxy_port)
                    token = self._securityHandler.token
               
            admin = arcrest.manageorg.Administration(url=self._org_url,
                                                     securityHandler=self._securityHandler)
          
            hostingServers = admin.hostingServers()    
            for hostingServer in hostingServers:
                serData = hostingServer.data
                serData
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
                                             
                #if 'error' in self._securityHandler.message and token is None:
                    #if self._securityHandler.message['error']== 401:
    
                        #self._securityHandler = arcrest.OAuthSecurityHandler(client_id='s5CKlHcJoNSm07TP',
                                                                               #secret_id='6015feb0f44c4a5fa00e1e9486de8c48',
                                                                               #org_url=self._org_url,
                                                                               #proxy_url=self._proxy_url,
                                                                               #proxy_port=self._proxy_port)
                        #token = self._securityHandler.token
            if 'error' in self._securityHandler.message and token is None:
                self._message = self._securityHandler.message
                self._valid = False
        
            else:
                self._message = self._securityHandler.message
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