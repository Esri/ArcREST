"""
   This sample shows how to append a featureclass 
   to a feature service using ArcRest and ArcRestHelper

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

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    url = "<portal or AGOL url>"
    itemId = "<Id of feature service item>"    
    layerName='<Name of layer in Feature Service>'
    fc=r'<Path to Feature Class to append>'
    atTable=r'<Attachment table of Feature Class - Optional>'    
    try:   
        fst = featureservicetools.featureservicetools(username = username, password=password,org_url=url,
                                           token_url=None, 
                                           proxy_url=None, 
                                           proxy_port=None)
        if fst.valid:
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