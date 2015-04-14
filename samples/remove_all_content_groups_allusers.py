"""
   This sample shows how to loop through all users
   and delete all their content and groups

"""
import arcrest
from arcresthelper import resettools

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
    try:
        rst = resettools.resetTools(username = username, password=password,org_url=url,
                                               token_url=None, 
                                               proxy_url=None, 
                                               proxy_port=None)
        if rst.valid:
            #users = {'users':[{'username':cred_info['Username']}]}
            #arh.removeUserData(users=users)
            #arh.removeUserGroups(users=users
            rst.removeUserData()
            rst.removeUserGroups()                
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)

