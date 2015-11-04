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
import csv

from arcpy import env

import publishingtools
import orgtools
import common
from securityhandlerhelper import securityhandlerhelper

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


class portalautomation(securityhandlerhelper):
    _log = None
    def setLog(self,log_file):
        if log_file is None:
            log_file = "log.txt"
        self._log = common.init_log(log_file=log_file)
    def __del__(self):
        if self._log is not None:
            common.close_log(log_file = self._log)
 
    #----------------------------------------------------------------------
    def stageContent(self,configFiles,dateTimeFormat=None):
      
        results = None    
        groups = None    
        items = None    
        group = None
        content = None
        contentInfo = None
        startTime = None
        orgTools = None
        
        
        if dateTimeFormat is None:
            dateTimeFormat = '%Y-%m-%d %H:%M'
        env.overwriteOutput = True    
        
       
        scriptStartTime = datetime.datetime.now()
        try:
    
            print "********************Stage Content Started********************"
    
            print "Script started at %s" % scriptStartTime.strftime(dateTimeFormat)
                  
            if self.securityhandler.valid == False:
                print "Login required"
            else:
                orgTools = orgtools.orgtools(securityinfo=self)
    
                if orgTools is None:
                    print "Error creating org tools"
                else:
                 
                    for configFile in configFiles:
    
                        config = common.init_config_json(config_file=configFile)
                        if config is not None:
                            if 'ContentItems' in config:
                                startTime = datetime.datetime.now()
                                print "Processing config %s, starting at: %s" % (configFile,startTime.strftime(dateTimeFormat))
                                contentInfo = config['ContentItems']
                                for cont in contentInfo:
                                    content = cont['Content']
                                    group = cont['ShareToGroup']
                        
                                    print "Sharing content to: %s" % group
                                    if os.path.isfile(content):
                                        with open(content, 'rb') as csvfile:
                                            items = []
                                            groups = []
                                            for row in csv.DictReader(csvfile,dialect='excel'):
                                                if cont['Type'] == "Group":
                                                    groups.append(row['id'])
                                                elif cont['Type'] == "Items":
                                                    items.append(row['id'])
                                            results = orgTools.shareItemsToGroup(shareToGroupName=group,items=items,groups=groups)
        
                                print "Config %s completed, time to complete: %s" % (configFile, str(datetime.datetime.now() - startTime))
                            else:
                                print "Config file missing ContentItems section"    
                        else:
                            print "Config %s not found" % configFile
    
    
        except(TypeError,ValueError,AttributeError),e:
            print e
        except (common.ArcRestHelperError),e:
            print "error in function: %s" % e[0]['function']
            print "error on line: %s" % e[0]['line']
            print "error in file name: %s" % e[0]['filename']
            print "with error message: %s" % e[0]['synerror']
            if 'arcpyError' in e[0]:
                print "with arcpy message: %s" % e[0]['arcpyError']
    
        except Exception as e:
            if (reportToolsInstalled):
                if isinstance(e,(ReportTools.ReportToolsError,DataPrep.DataPrepError)):
                    print "error in function: %s" % e[0]['function']
                    print "error on line: %s" % e[0]['line']
                    print "error in file name: %s" % e[0]['filename']
                    print "with error message: %s" % e[0]['synerror']
                    if 'arcpyError' in e[0]:
                        print "with arcpy message: %s" % e[0]['arcpyError']
                else:
                    line, filename, synerror = trace()
                    print "error on line: %s" % line
                    print "error in file name: %s" % filename
                    print "with error message: %s" % synerror
            else:
                line, filename, synerror = trace()
                print "error on line: %s" % line
                print "error in file name: %s" % filename
                print "with error message: %s" % synerror
        finally:
            print "Script complete, time to complete: %s" % str(datetime.datetime.now() - scriptStartTime)
            print "###############Stage Content Completed#################"
            print ""
            #if orgTools is not None:
                #orgTools.dispose()
    
            results = None    
            groups = None    
            items = None    
            group = None
            content = None
            contentInfo = None
            startTime = None
            orgTools = None
    
            del results
            del groups
            del items
            del group
            del content
            del contentInfo
            del startTime
            del orgTools
            
            gc.collect()
    #----------------------------------------------------------------------
    def createGroups(self,configFiles,dateTimeFormat=None):
        groupInfo = None    
        groupFile = None    
        iconPath = None    
        startTime = None
        thumbnail = None
        result = None
        config = None
        sciptPath = None
        orgTools = None
        
        if dateTimeFormat is None:
            dateTimeFormat = '%Y-%m-%d %H:%M'
        env.overwriteOutput = True    
        
        scriptStartTime = datetime.datetime.now()
        try:
    
            print "********************Create Groups********************"
    
            print "Script started at %s" % scriptStartTime.strftime(dateTimeFormat)
         
            if self.securityhandler.valid == False:
                print "Login required"
            else:
                orgTools = orgtools.orgtools(securityinfo=self)
    
                if orgTools is None:
                    print "Error creating orgtools"
                else:
    
                    for configFile in configFiles:
    
                        config = common.init_config_json(config_file=configFile)
                        if config is not None:
                           
                            startTime = datetime.datetime.now()
                            print "Processing config %s, starting at: %s" % (configFile,startTime.strftime(dateTimeFormat))
    
                            groupInfo = config['Groups']
                            groupFile = groupInfo['GroupInfo']
                            iconPath = groupInfo['IconPath']
    
                            if os.path.isfile(groupFile):
                                with open(groupFile, 'rb') as csvfile:
    
                                    for row in csv.DictReader(csvfile,dialect='excel'):
                                        if os.path.isfile(os.path.join(iconPath,row['thumbnail'])):
                                            thumbnail = os.path.join(iconPath,row['thumbnail'])
                                            if not os.path.isabs(thumbnail):
    
                                                sciptPath = os.getcwd()
                                                thumbnail = os.path.join(sciptPath,thumbnail)
    
                                            result = orgTools.createGroup(title=row['title'],description=row['description'],tags=row['tags'],snippet=row['snippet'],phone=row['phone'],access=row['access'],sortField=row['sortField'],sortOrder=row['sortOrder'], \
                                                             isViewOnly=row['isViewOnly'],isInvitationOnly=row['isInvitationOnly'],thumbnail=thumbnail)
    
                                        else:
                                            result = orgTools.createGroup(title=row['title'],description=row['description'],tags=row['tags'],snippet=row['snippet'],phone=row['phone'],access=row['access'],sortField=row['sortField'],sortOrder=row['sortOrder'], \
                                                             isViewOnly=row['isViewOnly'],isInvitationOnly=row['isInvitationOnly'])
    
                                        if result is None:
                                            pass
                                        else:
                                            print "Group created: " + result.title
    
    
    
                            print "Config %s completed, time to complete: %s" % (configFile, str(datetime.datetime.now() - startTime))
    
                        else:
                            print "Config %s not found" % configFile
    
    
        except(TypeError,ValueError,AttributeError),e:
            print e
        except (common.ArcRestHelperError),e:
            print "error in function: %s" % e[0]['function']
            print "error on line: %s" % e[0]['line']
            print "error in file name: %s" % e[0]['filename']
            print "with error message: %s" % e[0]['synerror']
            if 'arcpyError' in e[0]:
                print "with arcpy message: %s" % e[0]['arcpyError']
    
        except Exception as e:
            if (reportToolsInstalled):
                if isinstance(e,(ReportTools.ReportToolsError,DataPrep.DataPrepError)):
                    print "error in function: %s" % e[0]['function']
                    print "error on line: %s" % e[0]['line']
                    print "error in file name: %s" % e[0]['filename']
                    print "with error message: %s" % e[0]['synerror']
                    if 'arcpyError' in e[0]:
                        print "with arcpy message: %s" % e[0]['arcpyError']
                else:
                    line, filename, synerror = trace()
                    print "error on line: %s" % line
                    print "error in file name: %s" % filename
                    print "with error message: %s" % synerror
            else:
                line, filename, synerror = trace()
                print "error on line: %s" % line
                print "error in file name: %s" % filename
                print "with error message: %s" % synerror
        finally:
            print "Script complete, time to complete: %s" % str(datetime.datetime.now() - scriptStartTime)
            print "###############Create Groups Completed#################"
            print ""
           
            #if orgTools is not None:
                #orgTools.dispose()
            groupInfo = None
            groupFile = None
            iconPath = None
            startTime = None
            thumbnail = None
            result = None
            config = None
            sciptPath = None
            orgTools = None
            del groupInfo
            del groupFile
            del iconPath
            del startTime
            del thumbnail
            del result
            del config
            del sciptPath
            del orgTools  
    
            gc.collect()
    #----------------------------------------------------------------------
    def publishfromconfig(self,configFiles,combinedApp=None,dateTimeFormat=None):
        publishTools = None
        webmaps = None
        config = None
        resultsItems = None
        resultFS = None
        resultMaps = None
        resultApps = None
        combinedResults = None
    
        if dateTimeFormat is None:
            dateTimeFormat = '%Y-%m-%d %H:%M'
        env.overwriteOutput = True
    
        scriptStartTime = datetime.datetime.now()
        try:
            
            webmaps = []
            print "********************Script Started********************"
          
            print "Script started at %s" % scriptStartTime.strftime(dateTimeFormat)
          
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
    
    
                            publishTools = publishingtools.publishingtools(securityinfo=self)
                            if publishTools.valid == False :
                                print "Error creating publishing tools: %s" % publishTools.message
                            else:
                                print "Publishing tools created: %s" % publishTools.message
                                resultFS = []
                                if 'Items' in publishingConfig:
                                    startSectTime = datetime.datetime.now()
                                    print " "
                                    print "Creating Items: %s" % str(startSectTime.strftime(dateTimeFormat))
                                    resultsItems = publishTools.publishItems(items_info=publishingConfig['Items'])
                                    print "Items created, time to complete: %s" % str(datetime.datetime.now() - startSectTime)                         
                                
                                if 'FeatureCollections' in publishingConfig:
                                    startSectTime = datetime.datetime.now()
                                    print " "
                                    print "Creating Feature Collection: %s" % str(startSectTime.strftime(dateTimeFormat))
                                    resultFS = publishTools.publishFeatureCollections(configs=publishingConfig['FeatureCollections'])
                                    print "Feature Collection published, time to complete: %s" % str(datetime.datetime.now() - startSectTime)                         
                                if 'FeatureServices' in publishingConfig:
                                    startSectTime = datetime.datetime.now()
                                    print " "
                                    print "Creating Feature Services: %s" % str(startSectTime.strftime(dateTimeFormat))
                                    resultFS = resultFS + publishTools.publishFsFromMXD(fs_config=publishingConfig['FeatureServices'])
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
                                    resultMaps = publishTools.publishMap(maps_info=publishingConfig['MapDetails'],fsInfo=resultFS,itInfo=resultsItems)
                                    for maps in resultMaps:
                                        if 'MapInfo' in maps:
                                            if 'Results' in maps['MapInfo']:
                                                if 'itemId' in maps['MapInfo']['Results']:
                                                    webmaps.append(maps['MapInfo']['Results']['itemId'])
                                    print "Creating maps completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)
                                if 'AppDetails' in publishingConfig:
                                    startSectTime = datetime.datetime.now()
                                    print " "
                                    print "Creating apps: %s" % str(startSectTime.strftime(dateTimeFormat))
                                    resultApps = publishTools.publishApp(app_info=publishingConfig['AppDetails'],map_info=resultMaps,fsInfo=resultFS)
                                    print "Creating apps completed, time to complete: %s" % str(datetime.datetime.now() - startSectTime)
    
    
                            print "Publishing complete in config %s completed, time to complete: %s" % (configFile, str(datetime.datetime.now() - startTime))
    
                            print "-----Publishing Section Complete-----"
    
                else:
                    print "Config %s not found" % configFile
    
            if combinedApp:
                if os.path.exists(combinedApp):
                    print " "
                    startSectTime = datetime.datetime.now()
                    print "Creating combined result: %s" % str(startSectTime.strftime(dateTimeFormat))
    
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
        except (common.ArcRestHelperError),e:
            print "error in function: %s" % e[0]['function']
            print "error on line: %s" % e[0]['line']
            print "error in file name: %s" % e[0]['filename']
            print "with error message: %s" % e[0]['synerror']
            if 'arcpyError' in e[0]:
                print "with arcpy message: %s" % e[0]['arcpyError']
    
        except Exception as e:
            if (reportToolsInstalled):
                if isinstance(e,(ReportTools.ReportToolsError,DataPrep.DataPrepError)):
                    print "error in function: %s" % e[0]['function']
                    print "error on line: %s" % e[0]['line']
                    print "error in file name: %s" % e[0]['filename']
                    print "with error message: %s" % e[0]['synerror']
                    if 'arcpyError' in e[0]:
                        print "with arcpy message: %s" % e[0]['arcpyError']
                else:
                    line, filename, synerror = trace()
                    print "error on line: %s" % line
                    print "error in file name: %s" % filename
                    print "with error message: %s" % synerror
            else:
                line, filename, synerror = trace()
                print "error on line: %s" % line
                print "error in file name: %s" % filename
                print "with error message: %s" % synerror
    
        finally:
            print "Script complete, time to complete: %s" % str(datetime.datetime.now() - scriptStartTime)
            print "###############Script Completed#################"
            print ""
            if publishTools is not None:
                publishTools.dispose()
          
            publishTools = None
            webmaps = None
            config = None
            resultFS = None
            resultsItems = None
            resultMaps = None
            resultApps = None
            combinedResults = None
    
            del publishTools
            del webmaps
            del config
            del resultFS
            del resultMaps
            del resultApps
            del combinedResults
            del resultsItems
            gc.collect()
