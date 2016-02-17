'''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.1
    @description: Used to append content from a group to a feature service
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2016
'''
import gc
import os
import sys
import arcpy

from arcresthelper import featureservicetools
from arcresthelper import common
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

def outputPrinter(message,typeOfMessage='message'):
    if typeOfMessage == "error":
        arcpy.AddError(message=message)
    elif typeOfMessage == "warning":
        arcpy.AddWarning(message=message)
    else:
        arcpy.AddMessage(message=message)

    print message
def main():

    fsId = None
    groupLayer = None
    layerMap = None
    matchEntireName = None
    projection = None
    scratchGDB = None
    scratchLayer = None
    fst = None
    rows = None
    fieldList = None
    layerToServiceLayer = None
    matches = False
    showfullResponse = False

    try:

        proxy_port = None
        proxy_url = None

        securityinfo = {}
        securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI

        securityinfo['proxy_url'] = proxy_url
        securityinfo['proxy_port'] = proxy_port
        securityinfo['referer_url'] = None
        securityinfo['token_url'] = None
        securityinfo['certificatefile'] = None
        securityinfo['keyfile'] = None
        securityinfo['client_id'] = None
        securityinfo['secret_id'] = None

        username = arcpy.GetParameterAsText(0)
        password = arcpy.GetParameterAsText(1)
        siteURL = arcpy.GetParameterAsText(2)
        securityinfo['username'] = username
        securityinfo['password'] = password
        securityinfo['org_url'] = siteURL

        groupLayer = arcpy.GetParameterAsText(3)
        fsId = arcpy.GetParameterAsText(4)
        layerMap = arcpy.GetParameterAsText(5)
        matchEntireName = arcpy.GetParameterAsText(6)
        projection = arcpy.GetParameterAsText(7)
        lowerCaseFieldNames =arcpy.GetParameterAsText(8)
        showfullResponse =arcpy.GetParameterAsText(9)

        if str(lowerCaseFieldNames).upper() == 'TRUE':
            lowerCaseFieldNames = True
        else:
            lowerCaseFieldNames = False
        if projection is not None and projection != '#' and projection != '':
            #outputPrinter(message="Projecting %s" % str(projection))
            pass
        else:
            projection = None
            #outputPrinter(message="No Projection defined")
        arcpy.SetParameterAsText(10, "true")

        scratchGDB = arcpy.env.scratchWorkspace
        scratchLayName = "tempAppGrpFS"
        scratchLayer = os.path.join(scratchGDB,scratchLayName)

        groupLayer = arcpy.mapping.Layer(groupLayer)
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid:
            #outputPrinter(message="Security handler created")

            fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)

            if not fs is None:
                #Get a cursor to the layer map recordset
                rows = arcpy.SearchCursor(layerMap)

                #Get the fields
                fieldList = arcpy.ListFields(layerMap)

                #initialize the Translation Dictionary
                layerToServiceLayer = {}

                #Loop through each input row and add it to the conversion dict
                for row in rows:
                    layerToServiceLayer[row.getValue(fieldList[1].name)] = row.getValue(fieldList[2].name)
                    del row
                if groupLayer.isGroupLayer:
                    for lyr in groupLayer:
                        for key, value in layerToServiceLayer.items():
                            if str(matchEntireName).lower() =='true' and key == lyr.name:
                                matches = True
                            elif str(matchEntireName).lower() =='false' and str(lyr.name).startswith(key):
                                matches = True
                            else:
                                matches = False
                            if matches:
                                #arcpy.env.workspace = lyr.workspacePath
                                if arcpy.Exists(dataset=lyr) == True:
                                    outputPrinter(message="\tProcessing %s" % (lyr.name))
                                    result =  arcpy.GetCount_management(lyr.name)
                                    count = int(result.getOutput(0))
                                    outputPrinter(message="\t\t%s features" % (count))
                                    if count > 0:
                                        layerNameFull = groupLayer.name + '\\' + lyr.name

                                        if projection is not None:
                                            outputPrinter(message="\t\tProjecting %s" % (lyr.name))
                                            result = arcpy.Project_management(layerNameFull,
                                                                    scratchLayer,
                                                                    projection,
                                                                    "",
                                                                    "",
                                                                    "PRESERVE_SHAPE",
                                                                    "")


                                        else:
                                            outputPrinter(message="\t\tCopying %s" % (lyr.name))
                                            outputPrinter(message="Copying %s feature from %s" % (count,lyr.name))
                                            arcpy.FeatureClassToFeatureClass_conversion(layerNameFull,scratchGDB,scratchLayName)

                                        desc = arcpy.Describe(scratchLayer)
                                        if desc.shapeType == 'Polygon':
                                            outputPrinter(message="\t\tDensifying %s" % lyr.name)
                                            arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                                        if desc.shapeType == 'Polyline':
                                            outputPrinter(message="\t\tDensifying %s" % lyr.name)
                                            arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                                        syncLayer(fst, fs, scratchLayer, value, lyr.name,lowerCaseFieldNames,showfullResponse)
                                        outputPrinter (message="\tComplete")
                                        outputPrinter (message="\t")

                                    else:
                                        outputPrinter (message="\t\t%s does not contain any features, skipping" % lyr.name)
                                        outputPrinter (message="\tComplete")
                                        outputPrinter (message="\t")
                                else:
                                    outputPrinter (message="\t%s does not exist, skipping" % lyr.name)
                                    outputPrinter (message="\tComplete")
                                    outputPrinter (message="\t")
                                break

                else:
                    outputPrinter (message="Group layer is not a group layer", typeOfMessage='error')
            else:
                outputPrinter(message="Feature Service with id %s was not found" % fsId, typeOfMessage='error')
                arcpy.SetParameterAsText(10, "false")
        else:
            outputPrinter(fst.message,typeOfMessage='error')
            arcpy.SetParameterAsText(10, "false")



    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(10, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(10, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(10, "false")
    finally:
        pass
        if scratchLayer is not None:
            if arcpy.Exists(scratchLayer):
                arcpy.Delete_management(scratchLayer)

        fsId = None
        groupLayer = None
        layerMap = None
        matchEntireName = None
        projection = None
        scratchGDB = None
        scratchLayer = None

        fst = None
        rows = None
        fieldList = None
        layerToServiceLayer = None

        del fsId
        del groupLayer
        del layerMap
        del matchEntireName
        del projection
        del scratchGDB
        del scratchLayer
        del fst
        del rows
        del fieldList
        del layerToServiceLayer

        gc.collect()
def syncLayer(fst, fs, layer, layerName, displayName, lowerCaseFieldNames, showFullResponse):

    outputPrinter (message="\t\tAttemping to sync %s to %s" % (displayName,layerName))
    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
    if not fl is None:
        results = fl.addFeatures(fc=layer,lowerCaseFieldNames=lowerCaseFieldNames)
        if  str(showFullResponse).lower() =='true':
            outputPrinter(message="\t\tResponse:  %s" % results)
        if 'error' in results:
            outputPrinter(message="\t\tError in response from server:  %s" % results['error'],typeOfMessage='error')
            arcpy.SetParameterAsText(5, "false")
        else:
            if results['addResults'] is not None:
                featSucces = 0
                for result in results['addResults']:
                    if 'success' in result:
                        if result['success'] == False:
                            if 'error' in result:

                                outputPrinter (message="\t\t\tError info: %s" % (result['error']) )
                        else:
                            featSucces = featSucces + 1

                outputPrinter (message="\t\t%s features added to %s" % (featSucces,layerName) )
            else:
                outputPrinter (message="\t\t0 features added to %s /n result info %s" % (layerName,str(results)))
    else:
        outputPrinter(message="\t\tLayer %s was not found, please check your credentials and layer name" % layerName,typeOfMessage='error')
        arcpy.SetParameterAsText(5, "false")

if __name__ == "__main__":
    main()
