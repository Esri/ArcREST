"""
   This sample shows how to create groups from a
   csv files, sample csv and icon provided in the
   create_groups_support_material.zip

"""
import os
import csv
import arcrest
from arcresthelper import securityhandlerhelper
from arcresthelper import orgtools
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
    proxy_port = None
    proxy_url = None    

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfo['username'] = ""#username
    securityinfo['password'] = ""#password
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None   
    csvgroups = r""
    pathtoicons = r""
      
    try:
        orgt = orgtools.orgtools(securityinfo=securityinfo)

        if orgt.valid == False:
            print orgt.message
        else:        
                        
            if os.path.isfile(csvgroups):
                with open(csvgroups, 'rb') as csvfile:

                    for row in csv.DictReader(csvfile,dialect='excel'):
                        if os.path.isfile(os.path.join(pathtoicons,row['thumbnail'])):
                            thumbnail = os.path.join(pathtoicons,row['thumbnail'])
                            if not os.path.isabs(thumbnail):

                                sciptPath = os.getcwd()
                                thumbnail = os.path.join(sciptPath,thumbnail)

                            result = orgt.createGroup(title=row['title'], description=row['description'], tags=row['tags'], \
                                                     snippet=row['snippet'], phone=row['phone'], access=row['access'], \
                                                     sortField=row['sortField'], sortOrder=row['sortOrder'], \
                                                     isViewOnly=row['isViewOnly'], isInvitationOnly=row['isInvitationOnly'],thumbnail=thumbnail)
                                    
                        else:
                            result = orgt.createGroup(title=row['title'],description=row['description'],tags=row['tags'], \
                                                    snippet=row['snippet'],phone=row['phone'],access=row['access'], \
                                                    sortField=row['sortField'],sortOrder=row['sortOrder'], \
                                                    isViewOnly=row['isViewOnly'],isInvitationOnly=row['isInvitationOnly'])
                           
                        if result is None:
                            pass
                        else:
                            print "Group created: " + result.title
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror