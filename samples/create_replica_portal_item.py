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

        portalAdmin = arcrest.manageorg.Administration(securityHandler=agolSH)
        content = portalAdmin.content
        
        item = content.item(itemId)
        uc =  content.usercontent(username=item.owner)
        res = uc.exportItem(title="TestExport",
                            itemId=itemId,
                            exportFormat="File Geodatabase")
        exportItemId = res['exportItemId']
        jobId = res['jobId']
        serviceItemId = res['serviceItemId']
        status = uc.status(itemId=exportItemId, jobId=jobId, jobType="export")
        while status['status'].lower() != 'completed':
            status = uc.status(itemId=exportItemId, jobId=jobId, jobType="export")
            if status['status'].lower() == 'failed':
                print status                
                break
        del status
        exportItem = content.item(exportItemId)
        itemDataPath = exportItem.itemData(f=None, savePath=savePath)
        uc.deleteItem(item_id=exportItemId)
        print itemDataPath
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)