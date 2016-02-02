"""
   This sample shows to query completed workforce work

   Python 2.x/3.x
   ArcREST 3.5
"""
from __future__ import print_function
import arcrest
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

def main():
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
    sql = "status = 3" #Completed work
    saveLocation = r"c:\temp\completedWork.gdb" #GDB or folder to save result
    outName = "completedWork" #Name of result

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
                    res =  fst.QueryAllFeatures(url=fl.url,
                                    sql=sql,
                                    chunksize=300,
                                    saveLocation=saveLocation,
                                    outName=outName)
                    print (res)

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