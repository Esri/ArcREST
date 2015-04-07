import sys, os, datetime
import csv
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common


log_file='..//logs/CreateGroups.log'

configFiles=  ['..//configs/WaterGroups.json']
globalLoginInfo = '..//configs/___GlobalLoginInfoPortal.json'

dateTimeFormat = '%Y-%m-%d %H:%M'

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
            
                for configFile in configFiles:
        
                    config = Common.init_config_json(config_file=configFile)
                    if config is not None:
                       
                        print " "
                        print "    ---------"
                        print "        Processing config %s" % configFile

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
            
                                        result = arh.createGroup(title=row['title'],description=row['description'],tags=row['tags'],snippet=row['snippet'],phone=row['phone'],access=row['access'],sortField=row['sortField'],sortOrder=row['sortOrder'], \
                                                         isViewOnly=row['isViewOnly'],isInvitationOnly=row['isInvitationOnly'],thumbnail=thumbnail)
                                                
                                    else:
                                        result =arh.createGroup(title=row['title'],description=row['description'],tags=row['tags'],snippet=row['snippet'],phone=row['phone'],access=row['access'],sortField=row['sortField'],sortOrder=row['sortOrder'], \
                                                         isViewOnly=row['isViewOnly'],isInvitationOnly=row['isInvitationOnly'])
                                       
                                    if 'error' in result:
                                        print "             Error Creating Group %s" % result['error']
                                    else:
                                        print "             Group created: " + row['title']
                                    


                        print "        Config %s completed" % configFile
                        print "    ---------"                                            
                    else:
                        print "Config %s not found" % configFile
                    
            
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