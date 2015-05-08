"""
   This sample shows how to update the
   large thumbnail of an item
"""
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.security import PortalTokenSecurityHandler
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
    
      
    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password,org_url=url)

    portalAdmin = arcrest.manageorg.Administration(securityHandler=agolSH)
    content = portalAdmin.content
    adminusercontent = content.usercontent()
    item = content.item(itemId)
    itemParams = arcrest.manageorg.ItemParameter()
   
    itemParams.largeThumbnail = r"<Path to Image>"

    print adminusercontent.updateItem(itemId = itemId,
                                                updateItemParameters=itemParams,
                                                folderId=item.ownerFolder)