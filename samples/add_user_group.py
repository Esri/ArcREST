"""
   This sample shows how to add a user to a group
   Python 2/3
   ArcREST 3.5.1
"""
from __future__ import print_function
import arcrest
from arcresthelper import securityhandlerhelper
from arcresthelper import common
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
    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfo['username'] = ""#<UserName>
    securityinfo['password'] = ""#<Password>
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    username = "" #Username to add
    groupname = "" #Group Name

    try:
        shh = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
        if shh.valid == False:
            print (shh.message)
        else:
            admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            community = admin.community
            groups = community.groups
            groupIds = community.getGroupIDs(groupNames=groupname)
            if groupIds is None:
                print ("Group not found")
            if len(groupIds) == 0:
                print ("Group not found")
            groupId = groupIds[0]

            group = groups.group(groupId=groupId)
            if group is None:
                print ("Group not found")
            res = group.addUsersToGroups(users=username)

            print (res)
    except (common.ArcRestHelperError),e:
        print ("error in function: %s" % e[0]['function'])
        print ("error on line: %s" % e[0]['line'])
        print ("error in file name: %s" % e[0]['filename'])
        print ("with error message: %s" % e[0]['synerror'])
        if 'arcpyError' in e[0]:
            print ("with arcpy message: %s" % e[0]['arcpyError'])

    except:
        line, filename, synerror = trace()
        print ("error on line: %s" % line)
        print ("error in file name: %s" % filename)
        print ("with error message: %s" % synerror)

if __name__ == "__main__":
    main()