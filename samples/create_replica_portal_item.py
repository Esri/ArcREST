"""
   This sample shows how to create a 
   replica from portal of a feature service

"""
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
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
    itemId = "<Id of feature service item>"    
    savePath = "<Path to save replica>"
    try:      
        agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)

        admin = arcrest.manageorg.Administration(securityHandler=agolSH)
         
        item = admin.content.getItem(itemId)
        user = admin.content.users.user(username=item.owner)
       
        exportItem = user.exportItem(title="TestExport",
                            itemId=itemId,
                            exportFormat="File Geodatabase",
                            wait=False)
     
        itemDataPath = exportItem.itemData(f=None, savePath=savePath)
        uc.deleteItem(item_id=exportItem.id)
        print itemDataPath
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror