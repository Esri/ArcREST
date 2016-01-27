'''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0
    @description: Used to append points from a layer
        to the workforce assignment layer
    @requirements: Python 2.7.x/, ArcGIS 10.2.1 or higher
    @copyright: Esri, 2016
'''
import gc
import os
import sys
import arcpy

from arcresthelper import featureservicetools
from arcresthelper import common
from arcrest.common.general import Feature
from arcrest.agol import FeatureLayer
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
    arcpy.env.overwriteOutput = True
    fsId = None
    pointLayer = None
    pointLayerProj = None
    projection = None
    scratchGDB = None
    scratchLayer = None
    scratchLayName = None
    fst = None
    rows = None
    features = None
    sr_web = None
    priority = None
    status = None
    description = None
    assignmentType = None
    workOrderId = None
    json_string = None
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


        pointLayer = arcpy.GetParameterAsText(0)
        fsId = arcpy.GetParameterAsText(1)
        priority = arcpy.GetParameterAsText(2)
        status = arcpy.GetParameterAsText(3)
        description = arcpy.GetParameterAsText(4)
        assignmentType = arcpy.GetParameterAsText(5)
        workOrderId = arcpy.GetParameterAsText(6)
        location = arcpy.GetParameterAsText(7)
        locationField = arcpy.GetParameterAsText(8)
        showFullResponse = arcpy.GetParameterAsText(9)

        sr_web = arcpy.SpatialReference(102100)
        scratchGDB = arcpy.env.scratchWorkspace
        scratchLayName = "tempAppGrpFS"
        scratchLayer = os.path.join(scratchGDB,scratchLayName)
        if arcpy.Exists(pointLayer):

            features = []
            fst = featureservicetools.featureservicetools(securityinfo)
            if fst is not None and fst.valid:

                fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)
                if not fs is None:
                    fls = fs.layers
                    if len(fls) > 0 :
                        fl = fls[0]
                        pointLayerProj = arcpy.Project_management(pointLayer,
                                              scratchLayer,
                                              sr_web,
                                              "",
                                              "",
                                              "PRESERVE_SHAPE",
                                              "")

                        field_names = ["SHAPE@X", "SHAPE@Y", workOrderId]
                        if locationField is not None and locationField != '#' and locationField != '':
                            field_names.append(locationField)
                        #Get a cursor to the point layer
                        rows = arcpy.da.SearchCursor(in_table=pointLayerProj,
                                                  field_names=field_names
                                                  )
                        for row in rows:
                            json_string={}
                            json_string['geometry'] = {}
                            json_string['geometry']['x'] = row[0]
                            json_string['geometry']['y'] = row[1]
                            json_string['attributes'] ={}
                            json_string['attributes']['description'] = description
                            json_string['attributes']['status'] = status
                            #json_string['attributes']['notes'] = ''
                            json_string['attributes']['priority'] = priority
                            json_string['attributes']['assignmentType'] = assignmentType
                            json_string['attributes']['workOrderId'] = row[2]
                            if locationField is not None and locationField != '#' and locationField != '':
                                json_string['attributes']['location'] = location + ": " + row[3]
                            else:
                                json_string['attributes']['location'] = location

                            features.append(Feature(json_string=json_string))

                        results = fl.addFeature(features=features)
                        if  str(showFullResponse).lower() =='true':
                            outputPrinter(message="\t\tResponse:  %s" % results)
                        else:
                            if 'error' in results:
                                outputPrinter(message="\t\tError in response from server:  %s" % results['error'],typeOfMessage='error')
                                arcpy.SetParameterAsText(8, "false")
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

                                    outputPrinter (message="\t\t%s features added to %s" % (featSucces,fl.name) )
                                else:
                                    outputPrinter (message="\t\t0 features added to %s /n result info %s" % (fl.name,str(results)))

                        arcpy.SetParameterAsText(8, "true")
                    else:
                        outputPrinter(message="Assignment feature service not found in item with ID: " % fsId, typeOfMessage='error')
                        arcpy.SetParameterAsText(8, "false")
                else:
                    outputPrinter(message="Feature Service with id %s was not found" % fsId, typeOfMessage='error')
                    arcpy.SetParameterAsText(8, "false")
            else:
                outputPrinter(fst.message,typeOfMessage='error')
                arcpy.SetParameterAsText(8, "false")
        else:
            outputPrinter(message="Point layer does not exist",typeOfMessage='error')
            arcpy.SetParameterAsText(8, "false")


    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(8, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(8, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(8, "false")
    finally:
        pass
        if scratchLayer is not None:
            if arcpy.Exists(scratchLayer):
                arcpy.Delete_management(scratchLayer)

        gc.collect()

if __name__ == "__main__":
    main()
