"""
   This sample shows how to disable
   sync on a feature service
   CSV requires the following fields
    - itemid - ID of AGOL item



"""
from __future__ import print_function
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.security import PortalTokenSecurityHandler

import os, datetime
import csv
import arcresthelper
from arcresthelper import featureservicetools
from arcresthelper import common as Common

dateTimeFormat = '%Y-%m-%d %H:%M'

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
    securityinfo = {}
    securityinfo['security_type'] = 'Portal'
    securityinfo['username'] = ""
    securityinfo['password'] = ""
    securityinfo['org_url'] = "http://www.arcgis.com"
    try:
        fst = featureservicetools.featureservicetools(securityinfo=securityinfo)
        fs = fst.GetFeatureService(itemId='',returnURLOnly=False)
        result = fst.disableSync(url=fs.url)
        print (result)


    except:
        line, filename, synerror = trace()
        print ("error on line: %s" % line)
        print ("error in file name: %s" % filename)
        print ("with error message: %s" % synerror)

    finally:
        print (datetime.datetime.now().strftime(dateTimeFormat))
        print ("###############Script Completed#################")

if __name__ == "__main__":
    main()