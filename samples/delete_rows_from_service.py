"""
   This sample shows how to delete rows from a layer
"""
import arcrest
from arcresthelper import featureservicetools
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

def main():
    proxy_port = None
    proxy_url = None    

    securityInfo = {}
    securityInfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityInfo['username'] = "<UserName>"
    securityInfo['password'] = "<Password>"
    securityInfo['org_url'] = "http://www.arcgis.com"
    securityInfo['proxy_url'] = proxy_url
    securityInfo['proxy_port'] = proxy_port
    securityInfo['referer_url'] = None
    securityInfo['token_url'] = None
    securityInfo['certificatefile'] = None
    securityInfo['keyfile'] = None
    securityInfo['client_id'] = None
    securityInfo['secret_id'] = None   


    itemId = "<ID of Item>"    
    sql = "1=1"
    layerNames = "Layer1,Layer2"
    try:      

        fst = featureservicetools.featureservicetools(securityInfo)
        if fst.valid == False:
            print fst.message
        else:         

            fs = fst.GetFeatureService(itemId=itemId,returnURLOnly=False)
            if not fs is None:
               
                for layerName in layerNames.split(','):
                    fl = fst.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                    if not fl is None:
                        qRes = fl.query(where=sql, returnIDsOnly=True)
                        oids = qRes['objectids']
                        minId = min(oids)
                        maxId = max(oids)
                        chunksize = 500
                        i = 0
                        while(i <= len(oids)):
                            oidsDelete = ','.join(str(e) for e in oids[i:i+chunksize])
                            if oids == '':
                                continue
                            else:
                                results = fl.deleteFeatures(objectIds=oids)
                            i += chunksize
                            print i
                            print "Completed: {0:.0f}%".format(i / float(len(oids)) *100)
                        print results
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)

if __name__ == "__main__":
    main()