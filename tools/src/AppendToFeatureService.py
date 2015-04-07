"""
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0.0
    @description: Used to stage the app in your organization.
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

import sys, os, datetime
from arcpy import env
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common
import json

log_file='..//logs/AppendToFeatureService.log'
dateTimeFormat = '%Y-%m-%d %H:%M'
globalLoginInfo = '..//configs/___GlobalLoginInfo.json'

if __name__ == "__main__":
    env.overwriteOutput = True

    log = Common.init_log(log_file=log_file)

    try:

        if log is None:
            print "Log file could not be created"

        print "********************Script Started********************"
        print datetime.datetime.now().strftime(dateTimeFormat)
        cred_info = None
        if os.path.isfile(globalLoginInfo):
            loginInfo = Common.init_config_json(config_file=globalLoginInfo)
            if 'Credentials' in loginInfo:
                cred_info = loginInfo['Credentials']
       
        arh = ArcRestHelper.featureservicetools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                           token_url=None, 
                                           proxy_url=None, 
                                           proxy_port=None)
        layerName='Leak Report'
        itemId="15a35240e1c54c74ae877761963464fb"
        fc=r'C:\Work\ArcGIS for Utilities\_Water\Staging\A4W-LeaksInvestigator_v1_4\Maps and GDBs\LeaksInvestigator.gdb\LeakReport'
        atTable=r'C:\Work\ArcGIS for Utilities\_Water\Staging\A4W-LeaksInvestigator_v1_4\Maps and GDBs\LeaksInvestigator.gdb\LeakReport__ATTACH'
        if not arh is None:
            print "Security handler created"       
            fs = arh.GetFeatureService(itemId=itemId,returnURLOnly=False)
            if arh.valid:
                print("Logged in successful")         
                if not fs is None:                
                    fl = arh.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                    if not fl is None:
                        results = fl.addFeatures(fc=fc,attachmentTable=atTable)        
                        print json.dumps(results)
                    else:
                        print "Layer %s was not found, please check your credentials and layer name" % layerName     
                else:
                    print "Feature Service with id %s was not found" % fsId                                               
            else:
                print(arh.message)                                   
        else:
            print("Security handler not created, exiting")        
    except(TypeError,ValueError,AttributeError),e:
        print e
              
    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()