
from _abstract import abstract

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
import common 
import gc
#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

class featureservicetools(abstract.baseToolsClass):
  
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
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "GetFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
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
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureServiceByURL",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
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
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "GetLayerFromFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
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
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "AddFeaturesToFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
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
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "DeleteFeaturesFromFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
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