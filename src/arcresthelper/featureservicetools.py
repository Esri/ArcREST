
from securityhandlerhelper import securityhandlerhelper

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
import arcpy
#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect, sys 
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

class featureservicetools(securityhandlerhelper):
  
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
    def disableSync(self, url, definition = None):
        adminFS = AdminFeatureService(url=url, securityHandler=self._securityHandler)
        
        cap = str(adminFS.capabilities)
        existingDef = {}
    
        enableResults = 'skipped'      
        if 'Sync' in cap:
            capItems = cap.split(',')
            if 'Sync' in capItems:
                capItems.remove('Sync')

            existingDef['capabilities'] = ','.join(capItems)
            enableResults = adminFS.updateDefinition(json_dict=existingDef)
    
            if 'error' in enableResults:
                return enableResults['error']
        adminFS = None
        del adminFS


        return enableResults
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
        
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
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
        
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
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
      
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
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
    def AddFeaturesToFeatureLayer(self,url,pathToFeatureClass,chunksize=0):
        fl = None
        try:
            fl = FeatureLayer(
                   url=url,
                   securityHandler=self._securityHandler)
                        
            if chunksize > 0:
                messages = {'addResults':[]}
                total = arcpy.GetCount_management(pathToFeatureClass)
                arcpy.env.overwriteOutput = True
                inDesc = arcpy.Describe(pathToFeatureClass)
                oidName = arcpy.AddFieldDelimiters(pathToFeatureClass,inDesc.oidFieldName)
                sql = '%s = (select min(%s) from %s)' % (oidName,oidName,os.path.basename(pathToFeatureClass))
                cur = arcpy.da.SearchCursor(pathToFeatureClass,[inDesc.oidFieldName],sql)
                minOID = cur.next()[0]
                del cur, sql
                sql = '%s = (select max(%s) from %s)' % (oidName,oidName,os.path.basename(pathToFeatureClass))
                cur = arcpy.da.SearchCursor(pathToFeatureClass,[inDesc.oidFieldName],sql)
                maxOID = cur.next()[0]
                del cur, sql
                breaks = range(minOID,maxOID)[0:-1:chunksize] 
                breaks.append(maxOID+1)
                exprList = [oidName + ' >= ' + str(breaks[b]) + ' and ' + \
                            oidName + ' < ' + str(breaks[b+1]) for b in range(len(breaks)-1)]
                for expr in exprList:
                    UploadLayer = arcpy.MakeFeatureLayer_management(pathToFeatureClass, 'TEMPCOPY', expr).getOutput(0)
                    result = fl.addFeatures(fc=UploadLayer)
                    if messages is None:
                        messages = result
                    else:
                        if 'addResults' in result:
                            if 'addResults' in messages:
                                messages['addResults'] = messages['addResults'] + result['addResults']
                                print "%s/%s features added" % (len(messages['addResults']),total)
                            else:
                                messages['addResults'] = result['addResults']
                                print "%s/%s features added" % (len(messages['addResults']),total)
                        else:
                            messages['errors'] = result
                return messages
            else:
                return fl.addFeatures(fc=pathToFeatureClass)
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "create_report_layers_using_config",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
                "arcpyError": arcpy.GetMessages(2),
            }
                           )  
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
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
    def DeleteFeaturesFromFeatureLayer(self,url,sql,chunksize=0):
        fl = None
        try:
            fl = FeatureLayer(
                   url=url,
                   securityHandler=self._securityHandler)
            totalDeleted = 0
            if chunksize > 0:
                qRes = fl.query(where=sql, returnIDsOnly=True)
                if 'error' in qRes:
                    print qRes
                    return qRes
                elif 'objectIds' in qRes:
                    oids = qRes['objectIds']
                    total = len(oids)
                    if total == 0:
                        return "No features matched the query"
                        
                    minId = min(oids)
                    maxId = max(oids)
                   
                    i = 0
                    print "%s features to be deleted" % total
                    while(i <= len(oids)):
                        oidsDelete = ','.join(str(e) for e in oids[i:i+chunksize])
                        if oidsDelete == '':
                            continue
                        else:
                            results = fl.deleteFeatures(objectIds=oidsDelete)
                        if 'deleteResults' in results:
                            totalDeleted += len(results['deleteResults'])
                            print "%s%% Completed: %s/%s " % (int(totalDeleted / float(total) *100), totalDeleted, total)
                            i += chunksize                            
                        else:
                            print results
                            return "%s deleted" % totalDeleted
                    qRes = fl.query(where=sql, returnIDsOnly=True)
                    if 'objectIds' in qRes:
                        oids = qRes['objectIds']
                        if len(oids)> 0 :
                            print "%s features to be deleted" % len(oids)
                            results = fl.deleteFeatures(where=sql)
                            if 'deleteResults' in results:
                                totalDeleted += len(results['deleteResults'])
                                return "%s deleted" % totalDeleted
                            else:
                                return results
                    return "%s deleted" % totalDeleted 
                    
                else:
                    print qRes
            else:
                results = fl.deleteFeatures(where=sql)
                if 'deleteResults' in results:         
                    return totalDeleted + len(results['deleteResults'])
                else:
                    return results
       
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
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