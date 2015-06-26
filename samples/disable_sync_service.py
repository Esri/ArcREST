"""
   This sample shows how to disable
   sync on a feature service
   CSV requires the following fields
    - itemid - ID of AGOL item
   
   
    
"""
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.security import PortalTokenSecurityHandler

import sys, os, datetime
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
    username = "<User Name>"
    password = "<Password>"
    url = "<Org or Portal>"
   
    itemCSVFile =  r'Path to CSV File'
    
    sciptPath = os.getcwd()
    try:
        print "###############Script Started#################"
        print datetime.datetime.now().strftime(dateTimeFormat)
        if os.path.exists(itemCSVFile) == False:
            itemCSVFile = os.path.join(sciptPath,itemCSVFile)
        elif os.path.isabs(itemCSVFile) == False:
            itemCSVFile = os.path.join(sciptPath,itemCSVFile)
        if os.path.exists(itemCSVFile) == False:            
            print "CSV %s could not be located" % itemCSVFile
            return
        if os.path.isfile(itemCSVFile) == False:
            print "csv file %s could not be located" % itemCSVFile
            return
                       
        fst = featureservicetools.featureservicetools(username = username, password=password,org_url=url,
                                                  token_url=None, 
                                                  proxy_url=None, 
                                                  proxy_port=None)
        if fst.valid:
            with open(itemCSVFile, 'rb') as csvfile:
                
                for row in csv.DictReader(csvfile,dialect='excel'):
                    
                    if not 'itemid' in row:
                        print "itemID could not be found if table"
                        return
                    itemid = row['itemid']
                    fs = fst.GetFeatureService(itemId=itemid,returnURLOnly=False)
                    print fst.disableSync(url=fs.url)                
                                          
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)

    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        
if __name__ == "__main__":
    main()   