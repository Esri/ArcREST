
from __future__ import print_function
from __future__ import absolute_import

from .securityhandlerhelper import securityhandlerhelper

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
from . import common
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
    """Determines information about where an error was thrown.

    Returns:
        tuple: line number, filename, error message
    Examples:
        >>> try:
        ...     1/0
        ... except:
        ...     print("Error on '{}'\\nin file '{}'\\nwith error '{}'".format(*trace()))
        ...
        Error on 'line 1234'
        in file 'C:\\foo\\baz.py'
        with error 'ZeroDivisionError: integer division or modulo by zero'

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
    def RemoveAndAddFeatures(self, url, pathToFeatureClass, id_field, chunksize=1000):
        """Deletes all features in a feature service and uploads features from a feature class on disk.

        Args:
            url (str): The URL of the feature service.
            pathToFeatureClass (str): The path of the feature class on disk.
            id_field (str): The name of the field in the feature class to use for chunking.
            chunksize (int): The maximum amount of features to upload at a time. Defaults to 1000.
        Raises:
            ArcRestHelperError: if ``arcpy`` can't be found.

        """
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
                    idstring = ' in (' + ','.join(map(str,idlist)) + ')'
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
        """Enables editing capabilities on a feature service.

        Args:
            url (str): The URL of the feature service.
            definition (dict): A dictionary containing valid definition values. Defaults to ``None``.
        Returns:
            dict: The existing feature service definition capabilities.

        When ``definition`` is not provided (``None``), the following values are used by default:

        +------------------------------+------------------------------------------+
        |              Key             |                   Value                  |
        +------------------------------+------------------------------------------+
        | hasStaticData                | ``False``                                |
        +------------------------------+------------------------------------------+
        | allowGeometryUpdates         | ``True``                                 |
        +------------------------------+------------------------------------------+
        | enableEditorTracking         | ``False``                                |
        +------------------------------+------------------------------------------+
        | enableOwnershipAccessControl | ``False``                                |
        +------------------------------+------------------------------------------+
        | allowOthersToUpdate          | ``True``                                 |
        +------------------------------+------------------------------------------+
        | allowOthersToDelete          | ``True``                                 |
        +------------------------------+------------------------------------------+
        | capabilities                 | ``"Query,Editing,Create,Update,Delete"`` |
        +------------------------------+------------------------------------------+

        """
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
    def enableSync(self, url, definition = None):
        """Enables Sync capability for an AGOL feature service.

        Args:
            url (str): The URL of the feature service.
            definition (dict): A dictionary containing valid definition values. Defaults to ``None``.
        Returns:
            dict: The result from :py:func:`arcrest.hostedservice.service.AdminFeatureService.updateDefinition`.

        """
        adminFS = AdminFeatureService(url=url, securityHandler=self._securityHandler)

        cap = str(adminFS.capabilities)
        existingDef = {}
        enableResults = 'skipped'
        if 'Sync' in cap:
            return "Sync is already enabled"
        else:
            capItems = cap.split(',')
            capItems.append('Sync')
            existingDef['capabilities'] = ','.join(capItems)
            enableResults = adminFS.updateDefinition(json_dict=existingDef)

            if 'error' in enableResults:
                return enableResults['error']
        adminFS = None
        del adminFS
        return enableResults
    #----------------------------------------------------------------------
    def disableSync(self, url, definition = None):
        """Disables Sync capabilities for an AGOL feature service.

        Args:
            url (str): The URL of the feature service.
            definition (dict): A dictionary containing valid definition values. Defaults to ``None``.
        Returns:
            dict: The result from :py:func:`arcrest.hostedservice.service.AdminFeatureService.updateDefinition`.

        """
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
    #----------------------------------------------------------------------
    def GetFeatureService(self, itemId, returnURLOnly=False):
        """Obtains a feature service by item ID.

        Args:
            itemId (int): The feature service's item ID.
            returnURLOnly (bool): A boolean value to return the URL of the feature service. Defaults to ``False``.
        Returns:
            When ``returnURLOnly`` is ``True``, the URL of the feature service is returned.

            When ``False``, the result from :py:func:`arcrest.agol.services.FeatureService` or :py:func:`arcrest.ags.services.FeatureService`.

        """
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
    def GetLayerFromFeatureServiceByURL(self, url, layerName="", returnURLOnly=False):
        """Obtains a layer from a feature service by URL reference.

        Args:
            url (str): The URL of the feature service.
            layerName (str): The name of the layer. Defaults to ``""``.
            returnURLOnly (bool): A boolean value to return the URL of the layer. Defaults to ``False``.
        Returns:
            When ``returnURLOnly`` is ``True``, the URL of the layer is returned.

            When ``False``, the result from :py:func:`arcrest.agol.services.FeatureService` or :py:func:`arcrest.ags.services.FeatureService`.

        """
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
    def GetLayerFromFeatureService(self, fs, layerName="", returnURLOnly=False):
        """Obtains a layer from a feature service by feature service reference.

        Args:
            fs (FeatureService): The feature service from which to obtain the layer.
            layerName (str): The name of the layer. Defaults to ``""``.
            returnURLOnly (bool): A boolean value to return the URL of the layer. Defaults to ``False``.
        Returns:
            When ``returnURLOnly`` is ``True``, the URL of the layer is returned.

            When ``False``, the result from :py:func:`arcrest.agol.services.FeatureService` or :py:func:`arcrest.ags.services.FeatureService`.

        """
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
    def AddFeaturesToFeatureLayer(self, url, pathToFeatureClass, chunksize=0, lowerCaseFieldNames=False):
        """Appends local features to a hosted feature service layer.

        Args:
            url (str): The URL of the feature service layer.
            pathToFeatureClass (str): The path of the feature class on disk.
            chunksize (int): The maximum amount of features to upload at a time. Defaults to 0.
            lowerCaseFieldNames (bool): A boolean value indicating if field names should be converted
                to lowercase before uploading. Defaults to ``False``.
        Returns:
            The result from :py:func:`arcrest.agol.services.FeatureLayer.addFeatures`.
        Raises:
            ArcRestHelperError: if ``arcpy`` can't be found.
        Notes:
            If publishing to a PostgreSQL database, it is suggested to to set ``lowerCaseFieldNames`` to ``True``.

        """
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
                oidName = inDesc.oidFieldName

                arr = arcpy.da.FeatureClassToNumPyArray(pathToFeatureClass, (oidName))
                syncSoFar = 0
                messages = {'addResults':[],'errors':[]}
                total = len(arr)
                errorCount = 0
                if total == '0':
                    print ("0 features in %s" % pathToFeatureClass)
                    return "0 features in %s" % pathToFeatureClass
                print ("%s features in layer" % (total))

                arcpy.env.overwriteOutput = True
                if int(total) < int(chunksize):
                    return fl.addFeatures(fc=pathToFeatureClass,lowerCaseFieldNames=lowerCaseFieldNames)
                else:
                    newArr = chunklist(arr,chunksize)
                    exprList = ["{0} >= {1} AND {0} <= {2}".format(oidName, nArr[0][0], nArr[len(nArr)-1][0])
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
                                                errorCount  = errorCount + 1
                                                print ("\tError info: %s" % (result))
                                        else:
                                            featSucces = featSucces + 1
                                syncSoFar = syncSoFar + featSucces
                                print ("%s features added in this chunk" % (featSucces))
                                print ("%s/%s features added, %s errors" % (syncSoFar,total,errorCount ))
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
    def DeleteFeaturesFromFeatureLayer(self, url, sql, chunksize=0):
        """Removes features from a hosted feature service layer by SQL query.

        Args:
            url (str): The URL of the feature service layer.
            sql (str): The SQL query to apply against the feature service.
                Those features that satisfy the query will be deleted.
            chunksize (int): The maximum amount of features to remove at a time. Defaults to 0.
        Returns:
            The result from :py:func:`arcrest.agol.services.FeatureLayer.deleteFeatures`.
        Notes:
            If you want to delete all features, it is suggested to use the SQL query ``"1=1"``.

        """
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
    def QueryAllFeatures(self, url=None,
                         where="1=1",
                        out_fields="*",
                        timeFilter=None,
                        geometryFilter=None,
                        returnFeatureClass=False,
                        out_fc=None,
                        outSR=None,
                        chunksize=1000,
                        printIndent=""):

        """Performs an SQL query against a hosted feature service layer
        and returns all features regardless of service limit.

        Args:
            url (str): The URL of the feature service layer.
            where - the selection sql statement
            out_fields - the attribute fields to return
            timeFilter - a TimeFilter object where either the start time
                         or start and end time are defined to limit the
                         search results for a given time.  The values in
                         the timeFilter should be as UTC timestampes in
                         milliseconds.  No checking occurs to see if they
                         are in the right format.
            geometryFilter - a GeometryFilter object to parse down a given
                            query by another spatial dataset.
            returnFeatureClass - Default False. If true, query will be
                                 returned as feature class
            chunksize (int): The maximum amount of features to query at a time. Defaults to 1000.
            out_fc - only valid if returnFeatureClass is set to True.
                        Output location of query.

            Output:
               A list of Feature Objects (default) or a path to the output featureclass if
               returnFeatureClass is set to True.

        """
        if (url is None):
            return
        fl = None
        try:
            fl = FeatureLayer(url=url, securityHandler=self._securityHandler)
            qRes = fl.query(where=where,
                            returnIDsOnly=True,
                            timeFilter=timeFilter,
                            geometryFilter=geometryFilter)

            if 'error' in qRes:
                print (printIndent + qRes)
                return []
            elif 'objectIds' in qRes:
                oids = qRes['objectIds']
                total = len(oids)
                if total == 0:
                    return fl.query(where=where,
                                    returnGeometry=True,
                                    out_fields=out_fields,
                                    timeFilter=timeFilter,
                                    geometryFilter=geometryFilter,
                                    outSR=outSR)

                print (printIndent + "%s features to be downloaded" % total)
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
                                           out_fields=out_fields,
                                           timeFilter=timeFilter,
                                            geometryFilter=geometryFilter,
                                            outSR=outSR)
                        if isinstance(results,FeatureSet):
                            if combinedResults is None:
                                combinedResults = results
                            else:
                                for feature in results.features:
                                    combinedResults.features.append(feature)

                            totalQueried += len(results.features)
                            print(printIndent + "{:.0%} Completed: {}/{}".format(totalQueried / float(total), totalQueried, total))

                        else:
                            print (printIndent + results)
                if returnFeatureClass == True:
                    return combinedResults.save(*os.path.split(out_fc))
                else:
                    return combinedResults
            else:
                print (printIndent + qRes)
        except:
            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "QueryAllFeatures",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fl = None
            del fl
            gc.collect()
