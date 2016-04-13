'''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.2
    @description: Used to append content from a feature service
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2016
'''
from __future__ import print_function
import gc
import os
import sys
import arcpy
import re
import random
import string

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

    print (message)
#----------------------------------------------------------------------
def random_string_generator(size=6, chars=string.ascii_uppercase):
    try:
        return ''.join(random.choice(chars) for _ in range(size))
    except:
        return 'noRandVal'
    finally:
        pass
def main(*argv):

    fsId = None
    layerName = None
    dataToAppend = None
    fst = None
    fs = None
    results = None
    fl = None
    existingDef= None
    scratchGDB = None
    scratchLayName = None
    scratchLayer = None
    try:
        arcpy.env.overwriteOutput = True

        proxy_port = None
        proxy_url = None

        securityinfo = {}

        securityinfo['proxy_url'] = proxy_url
        securityinfo['proxy_port'] = proxy_port
        securityinfo['referer_url'] = None
        securityinfo['token_url'] = None
        securityinfo['certificatefile'] = None
        securityinfo['keyfile'] = None
        securityinfo['client_id'] = None
        securityinfo['secret_id'] = None

        username = argv[0]
        password = argv[1]
        siteURL = argv[2]

        version = arcpy.GetInstallInfo()['Version']
        if re.search("^10\.[0-2]", version) is not None:
            bReqUserName = True
        else:
            bReqUserName = False

        if bReqUserName and \
           (username == None or username == "#" or str(username).strip() == "" or \
            password == None or password== "#" or password== "*" or str(password).strip() == ""):
            outputPrinter ("{0} Requires a username and password".format(version), typeOfMessage='error')
            return

        if bReqUserName:
            securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
            securityinfo['username'] = username
            securityinfo['password'] = password
            securityinfo['org_url'] = siteURL

        else:
            securityinfo['security_type'] = 'ArcGIS'#LDAP, NTLM, OAuth, Portal, PKI

        fsId = argv[3]
        layerName = argv[4]
        dataToAppend = argv[5]
        projection = argv[6]
        lowerCaseFieldNames =argv[7]
        showFullResponse =argv[8]

        scratchGDB = arcpy.env.scratchWorkspace
        scratchLayName = random_string_generator()
        scratchLayer = os.path.join(scratchGDB,scratchLayName)

        if str(lowerCaseFieldNames).upper() == 'TRUE':
            lowerCaseFieldNames = True
        else:
            lowerCaseFieldNames = False

        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid:
            fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)

            if not fs is None:

                if arcpy.Exists(dataset=dataToAppend) == True:

                    lyr = arcpy.Describe(dataToAppend)
                    result =  arcpy.GetCount_management(dataToAppend)
                    count = int(result.getOutput(0))
                    outputPrinter(message="\t\t%s features" % (count))
                    if count > 0:
                        if projection is not None and projection != "#" and \
                                projection.strip() !='' :

                            outputPrinter(message="\t\tProjecting %s" % (lyr.name))
                            result = arcpy.Project_management(dataToAppend,
                                                              scratchLayer,
                                                              projection)
                        else:
                            outputPrinter(message="\t\tCopying %s feature from %s" % (count,lyr.name))
                            arcpy.FeatureClassToFeatureClass_conversion(dataToAppend,scratchGDB,scratchLayName)
                        desc = arcpy.Describe(scratchLayer)
                        if desc.shapeType == 'Polygon':
                            outputPrinter(message="\t\tDensifying %s" % lyr.name)
                            arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                        if desc.shapeType == 'Polyline':
                            outputPrinter(message="\t\tDensifying %s" % lyr.name)
                            arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")

                        syncLayer(fst, fs, scratchLayer, layerName, lyr.name,lowerCaseFieldNames,showFullResponse)
                        outputPrinter (message="\tComplete")
                        outputPrinter (message="\t")

                    else:
                        outputPrinter (message="\t\t%s does not contain any features, skipping" % lyr.name)
                        outputPrinter (message="\tComplete")
                        outputPrinter (message="\t")
                else:
                    outputPrinter (message="\t%s does not exist" % dataToAppend)
                    outputPrinter (message="\tComplete")
                    outputPrinter (message="\t")


            else:
                outputPrinter(message="\tFeature Service with id %s was not found" % fsId,typeOfMessage='error')
                arcpy.SetParameterAsText(9, "false")
        else:
            outputPrinter(message=fst.message, typeOfMessage="error")
            arcpy.SetParameterAsText(9, "false")
    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(9, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(9, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(9, "false")
    finally:
        if scratchLayer is not None:
            if arcpy.Exists(scratchLayer):
                arcpy.Delete_management(scratchLayer)
        existingDef = None
        fsId = None
        layerName = None
        dataToAppend = None
        fst = None
        fs = None
        results = None
        fl = None
        scratchGDB = None
        scratchLayName = None
        scratchLayer = None

        del existingDef

        del fsId
        del layerName
        del dataToAppend
        del fst
        del fs
        del results
        del fl
        del scratchGDB
        del scratchLayName
        del scratchLayer
        gc.collect()
def syncLayer(fst, fs, layer, layerName, displayName, lowerCaseFieldNames, showFullResponse):
    layerName = layerName.strip()
    outputPrinter (message="\t\tAttemping to sync %s to %s" % (displayName,layerName))
    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
    if not fl is None:
        results = fl.addFeatures(fc=layer,lowerCaseFieldNames=lowerCaseFieldNames)
        if  str(showFullResponse).lower() =='true':
            outputPrinter(message="\t\tResponse:  %s" % results)
        if 'error' in results:
            outputPrinter(message="\t\tError in response from server:  %s" % results['error'],typeOfMessage='error')
            arcpy.SetParameterAsText(9, "false")
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
        arcpy.SetParameterAsText(9, "false")

if __name__ == "__main__":
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)



























