
from __future__ import print_function

from securityhandlerhelper import securityhandlerhelper

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.ags import FeatureService

from arcrest.hostedservice import AdminFeatureService
from arcrest.common.spatial import scratchFolder, scratchGDB, json_to_featureclass
from arcrest.common.general import FeatureSet
from arcresthelper.common import chunklist

import datetime, time
import json
import os
import common
import gc

try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
import traceback, inspect, sys
import collections
#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """

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
    def RemoveAndAddFeatures(self, url, pathToFeatureClass,id_field,chunksize=1000):
        fl = None

        try:
            if arcpyFound == False:
                raise common.ArcRestHelperError({
                    "function": "RemoveAndAddFeatures",
                    "line": inspect.currentframe().f_back.f_lineno,
                    "filename":  'featureservicetools',
                    "synerror": "ArcPy required for this function"
                })
            arcpy.env.overwriteOutput = True
            tempaddlayer= 'ewtdwedfew'
            if not arcpy.Exists(pathToFeatureClass):
                raise common.ArcRestHelperError({
                    "function": "RemoveAndAddFeatures",
                    "line": inspect.currentframe().f_back.f_lineno,
                    "filename":  'featureservicetools',
                    "synerror": "%s does not exist" % pathToFeatureClass
                     }
                    )

            fields = arcpy.ListFields(pathToFeatureClass,wild_card=id_field)
            if len(fields) == 0:
                raise common.ArcRestHelperError({
                    "function": "RemoveAndAddFeatures",
                    "line": inspect.currentframe().f_back.f_lineno,
                    "filename":  'featureservicetools',
                    "synerror": "%s field does not exist" % id_field
                })
            strFld = True
            if fields[0].type != 'String':
                strFld = False

            fl = FeatureLayer(
                    url=url,
                    securityHandler=self._securityHandler)

            id_field_local = arcpy.AddFieldDelimiters(pathToFeatureClass, id_field)
            idlist = []
            print( arcpy.GetCount_management(in_rows=pathToFeatureClass).getOutput(0) + " features in the layer")
            with arcpy.da.SearchCursor(pathToFeatureClass, (id_field)) as cursor:
                allidlist = []

                for row in cursor:

                    if (strFld):
                        idlist.append("'" + row[0] +"'")
                    else:
                        idlist.append(row[0])
                    if len(idlist) >= chunksize:
                        allidlist.append(idlist)
                        idlist = []

                if len(idlist) > 0:
                    allidlist.append(idlist)
                for idlist in allidlist:
                    idstring = ' in (' + ','.join(idlist) + ')'
                    sql = id_field + idstring
                    sqlLocalFC = id_field_local + idstring
                    results = fl.deleteFeatures(where=sql,
                                                rollbackOnFailure=True)

                    if 'error' in results:
                        raise common.ArcRestHelperError({
                            "function": "RemoveAndAddFeatures",
                            "line": inspect.currentframe().f_back.f_lineno,
                            "filename":  'featureservicetools',
                            "synerror":results['error']
                        })
                    elif 'deleteResults' in results:
                        print ("%s features deleted" % len(results['deleteResults']))
                        for itm in results['deleteResults']:
                            if itm['success'] != True:
                                print (itm)
                    else:
                        print (results)

                    arcpy.MakeFeatureLayer_management(pathToFeatureClass,tempaddlayer,sqlLocalFC)
                    results = fl.addFeatures(fc=tempaddlayer)

                    if 'error' in results:
                        raise common.ArcRestHelperError({
                            "function": "RemoveAndAddFeatures",
                            "line": inspect.currentframe().f_back.f_lineno,
                            "filename":  'featureservicetools',
                            "synerror":results['error']
                        })
                    elif 'addResults' in results:
                        print ("%s features added" % len(results['addResults']))
                        for itm in results['addResults']:
                            if itm['success'] != True:
                                print (itm)
                    else:
                        print (results)
                    idlist = []
            if 'error' in results:
                raise common.ArcRestHelperError({
                    "function": "RemoveAndAddFeatures",
                    "line": inspect.currentframe().f_back.f_lineno,
                    "filename":  'featureservicetools',
                    "synerror":results['error']
                })
            else:
                print (results)
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

            gc.collect()

    #----------------------------------------------------------------------
    def EnableEditingOnService(self, url, definition = None):
        adminFS = AdminFeatureService(url=url, securityHandler=self._securityHandler)

        if definition is None:
            definition = collections.OrderedDict()
            definition['hasStaticData'] = False


            definition['allowGeometryUpdates'] = True

            definition['editorTrackingInfo'] = {}
            definition['editorTrackingInfo']['enableEditorTracking'] = False
            definition['editorTrackingInfo']['enableOwnershipAccessControl'] = False
            definition['editorTrackingInfo']['allowOthersToUpdate'] = True
            definition['editorTrackingInfo']['allowOthersToDelete'] = True
            definition['capabilities'] = "Query,Editing,Create,Update,Delete"


        existingDef = {}

        existingDef['capabilities']  = adminFS.capabilities
        existingDef['allowGeometryUpdates'] = adminFS.allowGeometryUpdates
        enableResults = adminFS.updateDefinition(json_dict=definition)

        if 'error' in enableResults:
            return enableResults['error']
        adminFS = None
        del adminFS

        print (enableResults)
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


            item = admin.content.getItem(itemId=itemId)
            if item.type == "Feature Service":
                if returnURLOnly:
                    return item.url
                else:
                    fs = arcrest.agol.FeatureService(
                       url=item.url,
                       securityHandler=self._securityHandler)
                    if fs.layers is None or len(fs.layers) == 0 :
                        fs = arcrest.ags.FeatureService(
                           url=item.url)
                    return fs

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
            fs = arcrest.agol.FeatureService(
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
            if (layers is None or len(layers) == 0) and fs.url is not None:
                fs = arcrest.ags.FeatureService(
                                    url=fs.url)
                layers = fs.layers
            if layers is not None:
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
            if fs.tables is not None:
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
    def AddFeaturesToFeatureLayer(self,url,pathToFeatureClass,chunksize=0,lowerCaseFieldNames=False):
        if arcpyFound == False:
            raise common.ArcRestHelperError({
                "function": "AddFeaturesToFeatureLayer",
                "line": inspect.currentframe().f_back.f_lineno,
                "filename":  'featureservicetools',
                "synerror": "ArcPy required for this function"
            })
        fl = None
        try:
            fl = FeatureLayer(
                   url=url,
                   securityHandler=self._securityHandler)

            if chunksize > 0:
                fc = os.path.basename(pathToFeatureClass)
                inDesc = arcpy.Describe(pathToFeatureClass)
                oidName = arcpy.AddFieldDelimiters(pathToFeatureClass,inDesc.oidFieldName)

                arr = arcpy.da.FeatureClassToNumPyArray(pathToFeatureClass, (oidName))
                syncSoFar = 0
                messages = {'addResults':[],'errors':[]}
                total = len(arr)#arcpy.GetCount_management(pathToFeatureClass).getOutput(0)
                if total == '0':
                    print ("0 features in %s" % pathToFeatureClass)
                    return "0 features in %s" % pathToFeatureClass
                print ("%s features in layer" % (total))

                arcpy.env.overwriteOutput = True
                if int(total) < int(chunksize):
                    return fl.addFeatures(fc=pathToFeatureClass,lowerCaseFieldNames=lowerCaseFieldNames)
                else:
                    newArr = chunklist(arr,chunksize+1)
                    exprList = ["{0} >= {1} AND {0} < {2}".format(oidName, nArr[0][0], nArr[len(nArr)-1][0])
                        for nArr in newArr]
                    for expr in exprList:

                        UploadLayer = arcpy.MakeFeatureLayer_management(pathToFeatureClass, 'TEMPCOPY', expr).getOutput(0)
                        #print(arcpy.GetCount_management(in_rows=UploadLayer).getOutput(0) + " features in the chunk")
                        results = fl.addFeatures(fc=UploadLayer,lowerCaseFieldNames=lowerCaseFieldNames)
                        chunkCount = arcpy.GetCount_management(in_rows=UploadLayer).getOutput(0)
                        print(chunkCount + " features in the chunk")
                        if chunkCount > 0:

                            if results is not None and 'addResults' in results and results['addResults'] is not None:
                                featSucces = 0
                                for result in results['addResults']:
                                    if 'success' in result:
                                        if result['success'] == False:
                                            if 'error' in result:
                                                print ("\tError info: %s" % (result))

                                        else:
                                            featSucces = featSucces + 1
                                syncSoFar = syncSoFar + featSucces
                                print ("%s features added in this chunk" % (featSucces))
                                print ("%s/%s features added" % (syncSoFar,total))
                                if 'addResults' in messages:
                                    messages['addResults'] = messages['addResults'] + results['addResults']

                                else:
                                    messages['addResults'] = results['addResults']

                            else:
                                messages['errors'] = result
                return messages
            else:
                return fl.addFeatures(fc=pathToFeatureClass,lowerCaseFieldNames=lowerCaseFieldNames)
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "AddFeaturesToFeatureLayer",
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
                    print (qRes)
                    return qRes
                elif 'objectIds' in qRes:
                    oids = qRes['objectIds']
                    total = len(oids)
                    if total == 0:
                        return  {'success':True,'message': "No features matched the query"}

                    i = 0
                    print ("%s features to be deleted" % total)
                    while(i <= len(oids)):
                        oidsDelete = ','.join(str(e) for e in oids[i:i+chunksize])
                        if oidsDelete == '':
                            continue
                        else:
                            results = fl.deleteFeatures(objectIds=oidsDelete)
                        if 'deleteResults' in results:
                            totalDeleted += len(results['deleteResults'])
                            print ("%s%% Completed: %s/%s " % (int(totalDeleted / float(total) *100), totalDeleted, total))
                            i += chunksize
                        else:
                            print (results)
                            return {'success':True,'message': "%s deleted" % totalDeleted}
                    qRes = fl.query(where=sql, returnIDsOnly=True)
                    if 'objectIds' in qRes:
                        oids = qRes['objectIds']
                        if len(oids)> 0 :
                            print ("%s features to be deleted" % len(oids))
                            results = fl.deleteFeatures(where=sql)
                            if 'deleteResults' in results:
                                totalDeleted += len(results['deleteResults'])
                                return  {'success':True,'message': "%s deleted" % totalDeleted}
                            else:
                                return results
                    return  {'success':True,'message': "%s deleted" % totalDeleted}

                else:
                    print (qRes)
            else:
                results = fl.deleteFeatures(where=sql)
                if results is not None:
                    if 'deleteResults' in results:
                        return  {'success':True,'message': totalDeleted + len(results['deleteResults'])}
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

    #----------------------------------------------------------------------
    def QueryAllFeatures(self,url,sql,out_fields="*",chunksize=1000,saveLocation="",outName=""):
        fl = None
        try:
            fl = FeatureLayer(url=url, securityHandler=self._securityHandler)
            qRes = fl.query(where=sql, returnIDsOnly=True)

            if 'error' in qRes:
                print (qRes)
                return qRes
            elif 'objectIds' in qRes:
                oids = qRes['objectIds']
                total = len(oids)
                if total == 0:
                    return  {'success':True, 'message':"No features matched the query"}

                print ("%s features to be downloaded" % total)
                chunksize = min(chunksize, fl.maxRecordCount)
                combinedResults = None
                totalQueried = 0
                for chunk in chunklist(l=oids, n=chunksize):
                    oidsQuery = ",".join(map(str, chunk))
                    if not oidsQuery:
                        continue
                    else:
                        results = fl.query(objectIds=oidsQuery,
                                           returnGeometry=True,
                                           out_fields=out_fields)
                        if isinstance(results,FeatureSet):
                            if combinedResults is None:
                                combinedResults = results
                            else:
                                for feature in results.features:
                                    combinedResults.features.append(feature)

                            totalQueried += len(results.features)
                            print("{:.0%} Completed: {}/{}".format(totalQueried / float(total), totalQueried, total))

                        else:
                            print (results)

                if saveLocation == "" or outName == "":
                    return combinedResults
                else:
                    return combinedResults.save(saveLocation=saveLocation, outName=outName)

            else:
                print (qRes)

        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "QueryFeatureLayer",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fl = None

            del fl

            gc.collect()