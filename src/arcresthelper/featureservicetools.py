

dateTimeFormat = '%Y-%m-%d %H:%M'

import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime
import json
import os
import common as Common

import time
import gc
import arcpy

class ArcRestHelperError(Exception):
    """ raised when error occurs in utility module functions """
    pass

class featureservicetools():
    _username = None
    _password = None
    _org_url = None
    _proxy_url = None
    _proxy_port = None
    _token_url = None
    _securityHandler = None
    _valid = True
    _message = ""
    #----------------------------------------------------------------------
    def __init__(self,
                 username=None,
                 password=None,
                 org_url=None,
                 token_url = None,
                 proxy_url=None,
                 proxy_port=None,
                 securityHandler=None):

        """Constructor"""
        if securityHandler is None:
            self._org_url = org_url
            self._username = username
            self._password = password
            self._proxy_url = proxy_url
            self._proxy_port = proxy_port
            self._token_url = token_url
            if self._org_url is None or self._org_url =='':
                self._org_url = 'http://www.arcgis.com'
            if self._org_url is None or '.arcgis.com' in  self._org_url:
                self._securityHandler = arcrest.AGOLTokenSecurityHandler(username=self._username,
                                                                  password=self._password,
                                                                  org_url=self._org_url,
                                                                  token_url=self._token_url,
                                                                  proxy_url=self._proxy_url,
                                                                  proxy_port=self._proxy_port)
            else:

                self._securityHandler = arcrest.PortalTokenSecurityHandler(username=self._username,
                                                                  password=self._password,
                                                                  org_url=self._org_url,
                                                                  proxy_url=self._proxy_url,
                                                                  proxy_port=self._proxy_port)
        else:
            self._org_url = securityHandler.org_url
            self._username = securityHandler.username
            self._password = securityHandler.password
            self._proxy_url = securityHandler.proxy_url
            self._proxy_port = securityHandler.proxy_port
            self._token_url = securityHandler.token_url
            self._securityHandler = securityHandler
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
    @property
    def valid(self):
        """ returns boolean wether handler is valid """
        return self._valid
    #----------------------------------------------------------------------
    def EnableEditingOnService(self, url, definition = None):
        adminFS = AdminFeatureService(url=url, securityHandler=self._securityHandler)

        if definition is None:
            definition = {}

            definition['capabilities'] = "Create,Delete,Query,Update,Editing"
            definition['allowGeometryUpdates'] = True

        existingDef = {}

        existingDef['capabilities']  = adminFS.capabilities
        existingDef['allowGeometryUpdates'] = adminFS.allowGeometryUpdates

        enableResults = adminFS.updateDefinition(json_dict=definition)

        if 'error' in enableResults:
            return enableResults['error']
        adminFS = None
        del adminFS


        return existingDef
    #----------------------------------------------------------------------

    def GetFeatureService(self,itemId,returnURLOnly=False):
        admin = None
        item = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            if self._securityHandler.valid == False:
                self._valid = self._securityHandler.valid
                self._message = self._securityHandler.message
                return None


            item = admin.content.item(itemId=itemId)
            if item.itemType == "Feature Service":
                if returnURLOnly:
                    return item.url
                else:
                    return FeatureService(
                       url=item.url,
                       securityHandler=self._securityHandler)
            return None
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            admin = None
            item = None
            del item
            del admin

            gc.collect()
    #----------------------------------------------------------------------
    def GetLayerFromFeatureServiceByURL(self,url,layerName="",returnURLOnly=False):
        fs = None
        try:
            fs = FeatureService(
                    url=url,
                    securityHandler=self._securityHandler)

            return self.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=returnURLOnly)
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureServiceByURL",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureServiceByURL",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fs = None

            del fs

            gc.collect()
    #----------------------------------------------------------------------
    def GetLayerFromFeatureService(self,fs,layerName="",returnURLOnly=False):
        layers = None
        table = None
        layer = None
        sublayer = None
        try:
            layers = fs.layers
            for layer in layers:
                if layer.name == layerName:
                    if returnURLOnly:
                        return fs.url + '/' + str(layer.id)
                    else:
                        return layer

                elif not layer.subLayers is None:
                    for sublayer in layer.subLayers:
                        if sublayer == layerName:
                            return sublayer
            for table in fs.tables:
                if table.name == layerName:
                    if returnURLOnly:
                        return fs.url + '/' + str(layer.id)
                    else:
                        return table
            return None
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            layers = None
            table = None
            layer = None
            sublayer = None

            del layers
            del table
            del layer
            del sublayer

            gc.collect()
    #----------------------------------------------------------------------
    def AddFeaturesToFeatureLayer(self,url,pathToFeatureClass):
        fl = None
        try:
            fl = FeatureLayer(
                   url=url,
                   securityHandler=self._securityHandler)
            return fl.addFeatures(fc=pathToFeatureClass)
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "AddFeaturesToFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "AddFeaturesToFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fl = None

            del fl

            gc.collect()
    #----------------------------------------------------------------------
    def DeleteFeaturesFromFeatureLayer(self,url,sql):
        fl = None
        try:
            fl = FeatureLayer(
                   url=url,
                   securityHandler=self._securityHandler,)
            return fl.deleteFeatures(where=sql)
        except arcpy.ExecuteError:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = Common.trace()
            raise ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fl = None

            del fl

            gc.collect()