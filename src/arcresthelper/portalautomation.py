"""
    @author: ArcGIS for Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.2
    @description: Used to create reports, maps and apps
    @requirements: Python 2.7.x, ArcGIS 10.2
    @copyright: Esri, 2015
   
"""
import gc
import sys, os, datetime
import json
from arcpy import env

import publishingtools
import common
try:
    import solutionreporttools 
    from solutionreporttools import reporttools as ReportTools
    from solutionreporttools import dataprep as DataPrep
    reportToolsInstalled = True
except:
    reportToolsInstalled = False


#----------------------------------------------------------------------
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

def publishfromconfig(configFiles,globalLoginInfo,combinedApp=None,log_file=None,dateTimeFormat=None):
    publishTools = None
    log = None
    webmaps = None
    cred_info = None
    loginInfo = None
    config = None
    resultFS = None
    resultMaps = None
    resultApps = None
    combinedResults = None    

    if log_file is None:
        log_file = "log.txt"
    if dateTimeFormat is None:
        dateTimeFormat = '%Y-%m-%d %H:%M'
    env.overwriteOutput = True

    log = common.init_log(log_file=log_file)

    try:
        webmaps = []
        if log is None:
            print "Log file could not be created"

        print "********************Script Started********************"
        scriptStartTime = datetime.datetime.now()       
        print "Script started at %s" % scriptStartTime.strftime(dateTimeFormat)
        print "-----Portal Credentials-----" 
        
        cred_info = None
        if not globalLoginInfo is None and os.path.isfile(globalLoginInfo):
            loginInfo = common.init_config_json(config_file=globalLoginInfo)
            if 'Credentials' in loginInfo:
                cred_info = loginInfo['Credentials']
                print "Credentials loaded"        
        if cred_info is None:
            print "Credentials not found"  
            cred_info = {}
            cred_info['Username'] = ''
            cred_info['Password'] = ''
            cred_info['Orgurl'] = 'http://www.arcgis.com'
        print "-----Portal Credentials complete-----" 
            
        
        
        # start report processing (moved out from under ArcREST logic. no AGO crednetials needed to run reports)
        for configFile in configFiles:                                                                      
            config = common.init_config_json(config_file=configFile)
            if config is not None:
                if 'ReportDetails' in config:
                    if reportToolsInstalled == False:
                        print "Report section is included in the config file but the solutionreporttools cannot be located"
                    else:
                        reportConfig = config['ReportDetails']
                        # This code checks to see if you want to export the data from SDE to a local GDB. The parameter is set in config file.
                        # Could be performance gain to run locally. If you choose this option, both the report and the data prep in memory config
                        # are modified so they can point to the local temp location.
                     
                        if 'RunReport' in reportConfig and (str(reportConfig['RunReport']).upper() =="TRUE" or str(reportConfig['RunReport']).upper() =="YES"):
                            reportConfig = ReportTools.reportDataPrep(reportConfig)
                            
                            print "-----Report Section Starting-----"  
                            startTime = datetime.datetime.now()
                            print "Processing reports in config %s, starting at: %s" % (configFile,startTime.strftime(dateTimeFormat))                                                               
                            ReportTools.create_report_layers_using_config(config=reportConfig)                   
                            print "Reports in config %s completed, time to complete: %s" % (configFile, str(datetime.datetime.now() - startTime))
                                
                            print "-----Report Section Complete-----" 
                if 'PublishingDetails' in config:
                    publishingConfig = config['PublishingDetails']                        
            
                    if 'PublishData' in publishingConfig:
                        publishData = publishingConfig['PublishData']
                    else:
                        print "PublishingDetails is missing the PublishData parameter:  type string, values, True or False"                    
                        publishData = 'TRUE'
                    if (str(publishData).upper() =="TRUE" or str(publishData).upper() =="YES"):       
            
                        print " "
                        print "-----Publishing Section Starting-----"                                   
                        startTime = datetime.datetime.now()
                        print "Processing publishing in config %s, starting at: %s" % (configFile,startTime.strftime(dateTimeFormat))  
            
                       
                        publishTools = publishingtools.publishingtools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                                              token_url=None,
                                                              proxy_url=None,
                                                              proxy_port=None)
                        if publishTools.valid == False :
                            print "Error creating publishing tools: %s" % publishTools.message
                        else:
                            print "Publishing tools created: %s" % publishTools.message
            
                            if 'FeatureServices' in publishingConfig:
                                startSectTime = datetime.datetime.now()
                                print " "                                                   
                                print "Creating Feature Services: %s" % str(startSectTime.strftime(dateTimeFormat))
                                resultFS = publishTools.publishFsFromMXD(fs_config=publishingConfig['FeatureServices'])
                                print "Feature Services published, time to complete: %s" % str(datetime.datetime.now() - startSectTime)
                            if 'ExistingServices' in publishingConfig:
            
                                startSectTime = datetime.datetime.now()
                                print " "                                                       
                                print "Updating Existing Feature Services: %s" % str(startSectTime.strftime(dateTimeFormat))                                
                                resultES = publishTools.updateFeatureService(efs_config=publishingConfig['ExistingServices'])
                                print "Updating Existing Feature Services completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)
                            if 'MapDetails' in publishingConfig:
                                startSectTime = datetime.datetime.now()
                                print " "                                                       
                                print "Creating maps: %s" % str(startSectTime.strftime(dateTimeFormat))                                          
                                resultMaps = publishTools.publishMap(maps_info=publishingConfig['MapDetails'],fsInfo=resultFS)
                                for maps in resultMaps:
                                    if 'MapInfo' in maps:
                                        if 'Results' in maps['MapInfo']:
                                            if 'id' in maps['MapInfo']['Results']:
                                                webmaps.append(maps['MapInfo']['Results']['id'])
                                print "Creating maps completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)                
                            if 'AppDetails' in publishingConfig:  
                                startSectTime = datetime.datetime.now()
                                print " "                                                       
                                print "Creating apps: %s" % str(startSectTime.strftime(dateTimeFormat))                                                 
                                resultApps = publishTools.publishApp(app_info=publishingConfig['AppDetails'],map_info=resultMaps)
                                print "Creating apps completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)     
            
                   
                        print "Publishing complete in config %s completed, time to complete: %s" % (configFile, str(datetime.datetime.now() - startTime))
            
                        print "-----Publishing Section Complete-----"
                       
            else:
                print "Config %s not found" % configFile        
                               
        if combinedApp:
            if os.path.exists(combinedApp):
                print " "                   
                startSectTime = datetime.datetime.now()
                print "Creating combind result: %s" % str(startSectTime.strftime(dateTimeFormat))                                               
    
                config = common.init_config_json(config_file=combinedApp)
                combinedResults = publishTools.publishCombinedWebMap(maps_info=config['PublishingDetails']['MapDetails'],webmaps=webmaps)
                if 'PublishingDetails' in config:
                    publishingConfig = config['PublishingDetails']                        
    
                    if 'PublishData' in publishingConfig:
                        publishData = publishingConfig['PublishData']
                    else:
                        print "PublishingDetails is missing the PublishData parameter:  type string, values, True or False"                    
                        publishData = 'TRUE'                                    
    
                    if (str(publishData).upper() =="TRUE" or str(publishData).upper() =="YES"):       
    
                        if 'AppDetails' in publishingConfig:  
                            resultApps = publishTools.publishApp(app_info=publishingConfig['AppDetails'],map_info=combinedResults)    
                        print "Creating combind result completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)                   
    except(TypeError,ValueError,AttributeError),e:
        print e
    except (common.ArcRestHelperError,ReportTools.ReportToolsError,DataPrep.DataPrepError),e:
        print("error in function: %s" % e[0]['function'])
        print("error on line: %s" % e[0]['line'])
        print("error in file name: %s" % e[0]['filename'])
        print("with error message: %s" % e[0]['synerror'])
        if 'arcpyError' in e[0]:
            print("with arcpy message: %s" % e[0]['arcpyError'])       

    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)

    finally:
        print "Script complete, time to complete: %s" % str(datetime.datetime.now() - scriptStartTime)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()
        if publishTools is not None:
            publishTools.dispose()

        log = None
        log_file = None
        configFiles = None
        globalLoginInfo = None
        dateTimeFormat = None
        combinedApp = None
        publishTools = None
        webmaps = None
        cred_info = None
        loginInfo = None
        config = None
        resultFS = None
        resultMaps = None
        resultApps = None
        combinedResults = None

        del log
        del log_file
        del configFiles
        del globalLoginInfo
        del dateTimeFormat
        del combinedApp
        del publishTools
        del webmaps
        del cred_info
        del loginInfo
        del config
        del resultFS
        del resultMaps
        del resultApps
        del combinedResults

        gc.collect()
