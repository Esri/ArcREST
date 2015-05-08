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

    print(message)
def main(*argv):
    userName = None
    password = None
    org_url = None
    fsId = None
    layerName = None
    dataToAppend = None
    fst = None
    fs = None
    results = None
    fl = None
    existingDef= None
    try:

        userName = argv[0]
        password = argv[1]
        org_url = argv[2]
        fsId = argv[3]
        layerName = argv[4]
        dataToAppend = argv[5]
        toggleEditCapabilities = argv[6]
       
        if arcpy.Exists(dataset=dataToAppend) == False:
            outputPrinter(message="Data layer not found: %" % dataToAppend)
        else:
            fst = featureservicetools.featureservicetools(username = userName, password=password,org_url=org_url,
                                                       token_url=None,
                                                       proxy_url=None,
                                                       proxy_port=None)
            if fst.valid:
                outputPrinter(message="Security handler created")

                fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)

                if not fs is None:
                    if str(toggleEditCapabilities).upper() == 'TRUE':
                        existingDef = fst.EnableEditingOnService(url=fs.url)
                    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                    if not fl is None:
                        results = fl.addFeatures(fc=dataToAppend)

                        if 'error' in results:
                            outputPrinter(message="Error in response from server:  %s" % results['error'],typeOfMessage='error')
                            arcpy.SetParameterAsText(6, "false")

                        else:
                            outputPrinter (message="%s features added" % len(results['addResults']) )
                            if toggleEditCapabilities == 'True':
                                existingDef = fst.EnableEditingOnService(url=fs.url,definition = existingDef)
                            arcpy.SetParameterAsText(6, "true")

                    else:
                        outputPrinter(message="Layer %s was not found, please check your credentials and layer name" % layerName,typeOfMessage='error')
                        arcpy.SetParameterAsText(6, "false")
                else:
                    outputPrinter(message="Feature Service with id %s was not found" % fsId,typeOfMessage='error')
                    arcpy.SetParameterAsText(6, "false")
            else:
                outputPrinter(fst.message,typeOfMessage='error')
                arcpy.SetParameterAsText(6, "false")



    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    finally:
        existingDef = None
        userName = None
        password = None
        org_url = None
        fsId = None
        layerName = None
        dataToAppend = None
        fst = None
        fs = None
        results = None
        fl = None

        del existingDef
        del userName
        del password
        del org_url
        del fsId
        del layerName
        del dataToAppend
        del fst
        del fs
        del results
        del fl

        gc.collect()
if __name__ == "__main__":
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)



























