"""
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0.0
    @description: Script to remove all user content and groups!!!!!.
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

import sys, os, datetime
from arcpy import env
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common

log_file='..//logs/Clean.log'
dateTimeFormat = '%Y-%m-%d %H:%M'
globalLoginInfo = '..//configs/___GlobalLoginInfo.json'

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
            arh = ArcRestHelper.resetTools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                           token_url=None,
                                           proxy_url=None,
                                           proxy_port=None)

            if arh is None:
                print "Error: Security handler not created"
            else:
                print "Security handler created"

                #users = {'users':[{'username':cred_info['Username']}]}
                #arh.removeUserData(users=users)
                #arh.removeUserGroups(users=users
                arh.removeUserData()
                arh.removeUserGroups()                
    except(TypeError,ValueError,AttributeError),e:
        print e
    except(ArcRestHelper.ArcRestHelperError),e:
        print e
    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()