"""
   This sample shows to update an assignment
   Python 2.x/3.x
   ArcREST 3.5
"""

from __future__ import print_function
import arcrest
from arcrest.common.general import Feature
from arcresthelper import featureservicetools
from arcresthelper import common
from arcrest.packages import six
import csv
from datetime import datetime

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

def main():
    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = "" #User Name
    securityinfo['password'] = "" #Password
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    itemId = ""#<Item ID>
    sql = "workOrderId = 'jCYverjadj'" #sql to return records to update
    fieldToChange = 'status' #field to change
    valueToSet = '3' #value to set

    fl = None
    fls = None
    fs = None
    try:
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid == False:
            print (fst.message)
        else:
            fs = fst.GetFeatureService(itemId=itemId,returnURLOnly=False)
            if not fs is None:
                fls = fs.layers
                if len(fls) > 0 :
                    fl = fls[0]
            if fl is None:
                print ("Layer Not Found")
                return

            features = fl.query(where=sql,out_fields='OBJECTID' + "," + fieldToChange,returnGeometry=False)
            if len(features) == 0:
                print ("No Matching features")
                return
            for feature in features:
                feature.set_value(fieldToChange,valueToSet)

            results = fl.updateFeature(features=features)

            if 'error' in results:
                print ("Error in response from server:  %s" % results['error'])

            else:
                if results['updateResults'] is not None:
                    featSucces = 0
                    for result in results['updateResults']:
                        if 'success' in result:
                            if result['success'] == False:
                                if 'error' in result:
                                    print ("Error info: %s" % (result['error']))
                            else:
                                featSucces = featSucces + 1

                    print ("%s features updated in %s" % (featSucces,fl.name))
                else:
                    print ("0 features updated in %s /n result info %s" % (fl.name,str(results)))

    except (common.ArcRestHelperError),e:
        print ("error in function: %s" % e[0]['function'])
        print ("error on line: %s" % e[0]['line'])
        print ("error in file name: %s" % e[0]['filename'])
        print ("with error message: %s" % e[0]['synerror'])
        if 'arcpyError' in e[0]:
            print ("with arcpy message: %s" % e[0]['arcpyError'])

    except:
        line, filename, synerror = trace()
        print ("error on line: %s" % line)
        print ("error in file name: %s" % filename)
        print ("with error message: %s" % synerror)

if __name__ == "__main__":
    main()
