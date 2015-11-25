"""
   This sample shows how to append a featureclass
   to a feature service using ArcRest and ArcRestHelper
   version 3.0.1
   Python 2
"""
import arcrest, json
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

if __name__ == "__main__":

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


    itemId = ""#<Item ID>
    layerName=''#Name of layer in the service
    fc=r''#Path to Feature Class
    atTable=None
    try:
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid == False:
            print fst.message
        else:

            fs = fst.GetFeatureService(itemId=itemId,returnURLOnly=False)
            if not fs is None:

                fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                if not fl is None:
                    results = fl.addFeatures(fc=fc,attachmentTable=atTable)
                    print json.dumps(results)
                else:
                    print "Layer %s was not found, please check your credentials and layer name" % layerName
            else:
                print "Feature Service with id %s was not found" % fsId

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror