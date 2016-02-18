"""
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.2
    @description: Used to delete content from a feature service
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2016
"""

from __future__ import print_function

import gc
import os
import sys
import arcpy
import re

from arcresthelper import featureservicetools
from arcresthelper import common
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
def outputPrinter(message,typeOfMessage='message'):
    if typeOfMessage == "error":
        arcpy.AddError(message=message)
    elif typeOfMessage == "warning":
        arcpy.AddWarning(message=message)
    else:
        arcpy.AddMessage(message=message)

    print (message)
def main(*argv):

    proxy_port = None
    proxy_url = None

    layerNames = None
    layerName = None
    layerName = None
    sql = None
    fst = None
    fs = None
    results = None
    fl = None
    existingDef = None
    try:


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
            password == None or password== "#" or str(password).strip() == ""):
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
        layerNames = argv[4]
        sql = argv[5]
        showFullResponse = argv[6]

        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid:

            fs = fst.GetFeatureService(itemId=fsId,returnURLOnly=False)
            if not fs is None:
                for layerName in layerNames.split(','):
                    layerName = layerName.strip()
                    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                    if not fl is None:
                        outputPrinter(message="\tAttempting to delete features matching this query: %s " % sql)
                        results = fl.deleteFeatures(where=sql)

                        if str(showFullResponse).lower() =='true':
                            outputPrinter(message="\t\tResponse:  %s" % results)
                        if 'error' in results:
                            outputPrinter(message="\t\tError in response from server:  %s" % results['error'],typeOfMessage='error')
                            arcpy.SetParameterAsText(7, "false")
                        else:
                            if results['deleteResults'] is not None:
                                featSucces = 0
                                for result in results['deleteResults']:
                                    if 'success' in result:
                                        if result['success'] == False:
                                            if 'error' in result:

                                                outputPrinter (message="\t\t\tError info: %s" % (result['error']) )
                                        else:
                                            featSucces = featSucces + 1

                                outputPrinter (message="\t\t%s features delete from %s" % (featSucces,layerName) )
                            else:
                                outputPrinter (message="\t\t0 features deleted from %s /n result info %s" % (layerName,str(results)))
                    else:
                        outputPrinter(message="\t\tLayer %s was not found, please check your credentials and layer name"    % layerName,typeOfMessage='error')
                        arcpy.SetParameterAsText(7, "false")
                        break
            else:
                outputPrinter(message="\tFeature Service with id %s was not found" % fsId, typeOfMessage='error')
                arcpy.SetParameterAsText(7, "false")

        else:
            outputPrinter(message=fst.message, typeOfMessage='error')
            arcpy.SetParameterAsText(7, "false")

    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(7, "false")
    except (common.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(7, "false")
    except:
        line, filename, synerror = trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(7, "false")
    finally:
        existingDef = None
        fsId = None
        layerNames = None
        layerName = None
        sql = None
        fst = None
        fs = None
        results = None
        fl = None

        del existingDef

        del fsId
        del layerNames
        del layerName
        del sql
        del fst
        del fs
        del results
        del fl


        gc.collect()
if __name__ == "__main__":
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)

