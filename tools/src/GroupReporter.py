import sys, io, os, datetime
import csv
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common

import csv,json

log_file='..//logs/GroupReporter.log'

configFiles=  ['..//configs/UtilitiesTryItLive.json','..//configs/UtilitiesTryItLive.json','..//configs/UtilitiesTryItLive.json','..//configs/UtilitiesTryItLive.json','..//configs/UtilitiesTryItLive.json','..//configs/UtilitiesTryItLive.json']
globalLoginInfo = '..//configs/___GlobalLoginInfo.json'

dateTimeFormat = '%Y-%m-%d %H:%M'
def noneToString(value):
    if( value is None):
        return ""
    else:
        return value
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
 
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror
if __name__ == "__main__":
    log = Common.init_log(log_file=log_file)
 
    try:

        if log is None:
            print "Log file could not be created"

        print "********************Script Started********************"
        print datetime.datetime.now().strftime(dateTimeFormat)
        webmaps = []
        cred_info = None
        if os.path.isfile(globalLoginInfo):
            loginInfo = Common.init_config_json(config_file=globalLoginInfo)
            if 'Credentials' in loginInfo:
                cred_info = loginInfo['Credentials']
        if cred_info is None:
            print "Login info not found"
        else: 
            arh = ArcRestHelper.orgTools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                               token_url=None, 
                                               proxy_url=None, 
                                               proxy_port=None)
            
            if arh is None:
                print "Error: Security handler not created"
            else:
                print "Security handler created"
              
            
                groups=[]
             
                for configFile in configFiles:
                 
                    config = Common.init_config_json(config_file=configFile)
                    if config is not None:
                          
                        print " "
                        print "    ---------"
                        print "        Processing config %s" % configFile
                                  
                        if 'Groups' in config:
                            fileName = os.path.join(config['OutputPath'],config['OutputFileName'])
                            iconPath = os.path.join(config['OutputPath'],"icons")
                            if not os.path.exists(iconPath):
                                os.makedirs(iconPath)                            
                            file = io.open(fileName, "w", encoding='utf-8')                                               
                            for groupName in config['Groups']:
                                results = arh.getGroupContent(groupName=groupName)  
                               
                                if 'results' in results:
                                  
                                    for result in results['results']:
                                        thumbLocal = arh.getThumbnailForItem(itemId=result['id'],fileName=result['title'],filePath=iconPath)
                                        result['thumbnail']=thumbLocal
                                        groups.append(result)
                                       
                            if len(groups) > 0:
                                file.write(unicode(json.dumps(groups, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))))                                              
                            file.close()                                                                                    
                        else:
                            print "        ERROR: Config %s is missing the Groups parameter" % configFile
                      
                        print "        Config %s completed" % configFile
                        print "    ---------"                                            
                    else:
                        print "Config %s not found" % configFile
                                           
                         
    except(TypeError,ValueError,AttributeError),e:
        print e
    except(ArcRestHelper.ArcRestHelperError),e:
        print e
    except:
        line, filename, synerror = trace()
        arcpy.AddError("error on line: %s" % line)
        arcpy.AddError("error in file name: %s" % filename)
        arcpy.AddError("with error message: %s" % synerror)                  
    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()
            
            
            
            
            
            
            
            
            
            
            
            