'''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.1
    @description: Used to append content from a feature service
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
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
    try:

        proxy_port = None
        proxy_url = None

        securityinfo = {}
        securityinfo['security_type'] = 'ArcGIS'#LDAP, NTLM, OAuth, Portal, PKI

        securityinfo['proxy_url'] = proxy_url
        securityinfo['proxy_port'] = proxy_port
        securityinfo['referer_url'] = None
        securityinfo['token_url'] = None
        securityinfo['certificatefile'] = None
        securityinfo['keyfile'] = None
        securityinfo['client_id'] = None
        securityinfo['secret_id'] = None

        fsId = arcpy.GetParameterAsText(1)
        groupLayer = arcpy.GetParameterAsText(0)
        layerMap = arcpy.GetParameterAsText(2)
        matchEntireName = arcpy.GetParameterAsText(3)
        projection = arcpy.GetParameterAsText(4)
        if projection is not None and projection != '#' and projection != '':
            #outputPrinter(message="Projecting %s" % str(projection))
            pass
        else:
            projection = None
            #outputPrinter(message="No Projection defined")
        arcpy.SetParameterAsText(5, "true")

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
                        for key, value in layerToServiceLayer.iteritems():
                            if matchEntireName =='true' and key == lyr.name:
                                matches = True
                            elif matchEntireName =='false' and key in lyr.name:
                                matches = True
                            else:
                                matches = False
                            if matches:
                                if arcpy.Exists(lyr.name) == True:
                                    result =  arcpy.GetCount_management(lyr.name)
                                    count = int(result.getOutput(0))
                                    if count > 0:
                                        layerNameFull = groupLayer.name + '\\' + lyr.name

                                        if projection is not None:
                                            outputPrinter(message="Projecting %s" % lyr.name)
                                            arcpy.Project_management(layerNameFull,
                                                                    scratchLayer,
                                                                    projection,
                                                                    "",
                                                                    "",
                                                                    "NO_PRESERVE_SHAPE",
                                                                    "")

                                        else:
                                            outputPrinter(message="Copying %s" % lyr.name)
                                            arcpy.FeatureClassToFeatureClass_conversion(layerNameFull,scratchGDB,scratchLayName)

                                        desc = arcpy.Describe(scratchLayer)
                                        if desc.shapeType == 'Polygon':
                                            outputPrinter(message="Densifying %s" % lyr.name)
                                            arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                                        syncLayer(fst, fs, scratchLayer, value, lyr.name)

                                    else:
                                        outputPrinter (message="%s does not contain any features, skipping" % lyr.name)
                                else:
                                    outputPrinter (message="%s does not exist, skipping" % lyr.name)
                                break

                else:
                    outputPrinter (message="Group layer is not a group layer", typeOfMessage='error')
            else:
                outputPrinter(message="Feature Service with id %s was not found" % fsId, typeOfMessage='error')
                arcpy.SetParameterAsText(5, "false")
        else:
            outputPrinter(fst.message,typeOfMessage='error')
            arcpy.SetParameterAsText(5, "false")



    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(5, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(5, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(5, "false")
    finally:
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
def syncLayer(fst, fs, layer, layerName, displayName):

    outputPrinter (message="Attemping to sync %s to %s" % (displayName,layerName))
    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
    if not fl is None:
        results = fl.addFeatures(fc=layer)

        if 'error' in results:
            outputPrinter(message="Error in response from server:  %s" % results['error'],typeOfMessage='error')
            arcpy.SetParameterAsText(5, "false")
        else:
            if results['addResults'] is not None:
                outputPrinter (message="%s features added to %s" % (len(results['addResults']),layerName) )
            else:
                outputPrinter (message="0 features added to %s" % layerName)
    else:
        outputPrinter(message="Layer %s was not found, please check your credentials and layer name" % layerName,typeOfMessage='error')
        arcpy.SetParameterAsText(5, "false")

if __name__ == "__main__":
    main()
