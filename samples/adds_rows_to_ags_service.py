"""
   This sample shows how to add rows to an AGS based service
   version 3.5.4
   Python 2
"""
from __future__ import print_function
from __future__ import absolute_import
import arcrest
from arcresthelper import featureservicetools
from arcresthelper import common

def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect,sys
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
    securityinfo['security_type'] = 'AGS'
    securityinfo['username'] = ""#<UserName>
    securityinfo['password'] = ""#<Password>
    securityinfo['org_url'] = ""#<ArcGIS Server URL, ex: https://myserver/arcgis
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None
    
    pathToFeatureClass = r""#local path to feature class to load
    fs_url = ''#url to layer, not service, make sure it ends with a \Number
    
    try:

        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid == False:
            print (fst.message)
        else:
            results =  fst.AddFeaturesToFeatureLayer(url=fs_url, pathToFeatureClass=pathToFeatureClass,
                                                      chunksize=2000)
            if 'addResults' in results:
                print ("%s features processed" % len(results['addResults']))
    except (common.ArcRestHelperError) as e:
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