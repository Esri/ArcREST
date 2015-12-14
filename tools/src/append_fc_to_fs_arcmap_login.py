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
def main(*argv):

    fsId = None
    layerName = None
    dataToAppend = None
    fst = None
    fs = None
    results = None
    fl = None
    existingDef= None
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

        fsId = argv[0]
        layerName = argv[1]
        dataToAppend = argv[2]
        lowerCaseFieldNames = argv[3]

        if str(lowerCaseFieldNames).upper() == 'TRUE':
            lowerCaseFieldNames = True
        else:
            lowerCaseFieldNames = False
        if arcpy.Exists(dataset=dataToAppend) == False:
            outputPrinter(message="Data layer not found: " + dataToAppend)
        else:
            fst = featureservicetools.featureservicetools(securityinfo)
            if fst.valid:
                outputPrinter(message="Security handler created")

                fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)

                if not fs is None:
                   
                    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                    if not fl is None:
                        results = fl.addFeatures(fc=dataToAppend,lowerCaseFieldNames=lowerCaseFieldNames)

                        if 'error' in results:
                            outputPrinter(message="Error in response from server:  %s" % results['error'],typeOfMessage='error')
                            arcpy.SetParameterAsText(4, "false")

                        else:
                            if results['addResults'] is not None:
                                outputPrinter (message="%s features added" % len(results['addResults']) )
                            else:
                                outputPrinter (message="0 features added" )
                            
                            arcpy.SetParameterAsText(4, "true")

                    else:
                        outputPrinter(message="Layer %s was not found, please check your credentials and layer name" % layerName,typeOfMessage='error')
                        arcpy.SetParameterAsText(4, "false")
                else:
                    outputPrinter(message="Feature Service with id %s was not found" % fsId,typeOfMessage='error')
                    arcpy.SetParameterAsText(4, "false")
            else:
                outputPrinter(fst.message,typeOfMessage='error')
                arcpy.SetParameterAsText(4, "false")



    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(4, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(4, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(4, "false")
    finally:
        existingDef = None
        fsId = None
        layerName = None
        dataToAppend = None
        fst = None
        fs = None
        results = None
        fl = None

        del existingDef

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



























