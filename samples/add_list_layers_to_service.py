  '''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0
    @description: Used to append content from list of layers to
    a feature service
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
    showFullResponse = False

    try:
        arcpy.env.overwriteOutput = True

        proxy_port = None
        proxy_url = None

        securityinfo = {}
        securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
        securityinfo['username'] = ""#<UserName>
        securityinfo['password'] = ""#<Password>
        securityinfo['org_url'] = "http://www.arcgis.com"
        securityinfo['proxy_url'] = proxy_url
        securityinfo['proxy_port'] = proxy_port
        securityinfo['referer_url'] = None
        securityinfo['token_url'] = None
        securityinfo['certificatefile'] = None
        securityinfo['keyfile'] = None
        securityinfo['client_id'] = None
        securityinfo['secret_id'] = None

        itemId = "660c9dde3a24428e9143473f6ee7f77d"#Item ID of the feature service

        path = r'C:\sampleData\ElectricNetwork.gdb'#Path to GDB with layers to post
        #List of layers in the gdb and name of layer in the service
        featureClasses = [
            {
              "FeatureClass":"SafetyViolation",
              "Layer":"Violations"
              },
            {
              "FeatureClass":"VoltageRegulator",
              "Layer":"Voltage Regulator"
              },
            {
              "FeatureClass":"Capacitor",
              "Layer":"Power Factor Correcting Equipment"
              },
            {
              "FeatureClass":"Elbow",
              "Layer":"Elbow"
              },
            {
              "FeatureClass":"Fuse",
              "Layer":"Fuse"
              },
            {
              "FeatureClass":"CircuitBreaker",
              "Layer":"Protective Device"
              },
            {
              "FeatureClass":"Switch",
              "Layer":"Switch"
              },
            {
              "FeatureClass":"ServicePoint",
              "Layer":"Service Point"
              },
            {
              "FeatureClass":"Transformer",
              "Layer":"Transformer"
              },
            {
              "FeatureClass":"UndergroundStructures",
              "Layer":"Underground Structure"
              },
            {
              "FeatureClass":"Streetlights",
              "Layer":"Streetlight"
              },
            {
              "FeatureClass":"Poles",
              "Layer":"Poles"
              },
            {
              "FeatureClass":"SurfaceStructures",
              "Layer":"Surface Structure"
              },
            {
              "FeatureClass":"Substation",
              "Layer":"Electric Station"
              },
            {
              "FeatureClass":"BoundarySubstation",
              "Layer":"Substation Boundary"
              },
            {
              "FeatureClass":"SwitchingFacility",
              "Layer":"Switching Facility"
              },
            {
              "FeatureClass":"OHMediumVoltage",
              "Layer":"Primary Overhead Conductor"
              },
            {
              "FeatureClass":"UGMediumVoltage",
              "Layer":"Primary Underground Conductor"
              },     {
                "FeatureClass":"UGLowVoltage",
                "Layer":"Secondary Underground Conductor"
                },
            {
              "FeatureClass":"OHLowVoltage",
              "Layer":"Secondary Overhead Conductor"
              },
            {
              "FeatureClass":"MediumVoltageBusBar",
              "Layer":"Bus Bar"
            }
          ]

        sr = arcpy.SpatialReference(3587) #to project the data, set to None to skip projection
        lowerCaseFieldNames = False #option to convert all fields to lowercase for portal data store services
        showFullResponse = True #option to return the entire response string

        if str(lowerCaseFieldNames).upper() == 'TRUE' or lowerCaseFieldNames == True:
            lowerCaseFieldNames = True
        else:
            lowerCaseFieldNames = False
        if projection is not None and projection != '#' and projection != '':
            #outputPrinter(message="Projecting %s" % str(projection))
            pass
        else:
            projection = None
            #outputPrinter(message="No Projection defined")

        scratchGDB = arcpy.env.scratchWorkspace
        scratchLayName = random_string_generator()
        scratchLayer = os.path.join(scratchGDB,scratchLayName)

        groupLayer = arcpy.mapping.Layer(groupLayer)
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid:
            #outputPrinter(message="Security handler created")

            fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)

            if not fs is None:

                #Loop through each input row and add it to the conversion dict
                for featureClass in featureClasses:
                    localLayer = os.path.join(path,featureClass["FeatureClass"])
                    layerName = featureClass["FeatureClass"]
                    if (arcpy.Exists(localLayer)):

                        outputPrinter(message="\tProcessing %s" % (layerName))
                        result =  arcpy.GetCount_management(localLayer)
                        count = int(result.getOutput(0))
                        outputPrinter(message="\t\t%s features" % (count))
                        if count > 0:

                            if projection is not None and projection != "#" and \
                                    projection.strip() !='' :
                                outputPrinter(message="\t\tProjecting %s" % (layerName))
                                result = arcpy.Project_management(localLayer,
                                                        scratchLayer,
                                                        projection)

                            else:
                                outputPrinter(message="\t\tCopying %s feature from %s" % (count,layerName))
                                arcpy.FeatureClassToFeatureClass_conversion(localLayer,scratchGDB,scratchLayName)

                            desc = arcpy.Describe(scratchLayer)
                            if desc.shapeType == 'Polygon':
                                outputPrinter(message="\t\tDensifying %s" % layerName)
                                arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                            if desc.shapeType == 'Polyline':
                                outputPrinter(message="\t\tDensifying %s" % layerName)
                                arcpy.Densify_edit(scratchLayer, "ANGLE", "33 Unknown", "0.33 Unknown", "4")
                            syncLayer(fst, fs, scratchLayer, layerName, layerName,lowerCaseFieldNames,showFullResponse)
                            outputPrinter (message="\tComplete")
                            outputPrinter (message="\t")

                        else:
                            outputPrinter (message="\t\t%s does not contain any features, skipping" % layerName)
                            outputPrinter (message="\tComplete")
                            outputPrinter (message="\t")

            else:
                outputPrinter(message="Feature Service with id %s was not found" % fsId, typeOfMessage='error')

        else:
            outputPrinter(fst.message,typeOfMessage='error')

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
        if scratchLayer is not None:
            if arcpy.Exists(scratchLayer):
                arcpy.Delete_management(scratchLayer)


        gc.collect()
def syncLayer(fst, fs, layer, layerName, displayName, lowerCaseFieldNames, showFullResponse):
    layerName = layerName.strip()

    outputPrinter (message="\t\tAttemping to sync %s to %s" % (displayName,layerName))
    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
    if not fl is None:
        results = fl.addFeatures(fc=layer,lowerCaseFieldNames=lowerCaseFieldNames)
        if str(showFullResponse).lower() =='true':
            outputPrinter(message="\t\tResponse:  %s" % results)
        if 'error' in results:
            outputPrinter(message="\t\tError in response from server:  %s" % results['error'],typeOfMessage='error')
            arcpy.SetParameterAsText(10, "false")
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
        arcpy.SetParameterAsText(10, "false")

if __name__ == "__main__":
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)

