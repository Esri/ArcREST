"""
   This sample shows how to create groups from a
   csv files, sample csv and icon provided in the
   create_groups_support_material.zip

"""
import arcrest
import os
import csv
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
    username = "<username>"
    password = "<password>"
    url = "<portal or AGOL url>"
    csvgroups = "<path to csv file>"
    pathtoicons = "<path to icons folder>"
      
    try:

            orgt = orgtools.orgtools(username = username, password=password,org_url=url,
                                               token_url=None, 
                                               proxy_url=None, 
                                               proxy_port=None)
            
                   
            if orgt.valid:
                        
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
                               
                            if 'error' in result:
                                print "             Error Creating Group %s" % result['error']
                            else:
                                print "             Group created: " + row['title']
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)