"""
   This sample shows how to create a list in json
   of all items in a group
"""
import arcrest
import os,io
import json
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
    groups = "<[groups, group1]>"
    outputlocation = "<Location to store the results>"
    outputfilename = "<outputfilename.json>"
    fileName = os.path.join(outputlocation,outputfilename)
    iconPath = os.path.join(outputlocation,"icons")  
    
    try:

        if not os.path.exists(iconPath):
            os.makedirs(iconPath)                            
        groups = []
        orgt = orgtools.orgtools(username = username, password=password,org_url=url,
                                 token_url=None, 
                                 proxy_url=None, 
                                 proxy_port=None)


        if orgt.valid:
                                               
            file = io.open(fileName, "w", encoding='utf-8')                                               
            for groupName in searchgroups:
                results = orgt.getGroupContent(groupName=groupName)  
               
                if not results is None and 'results' in results:
                  
                    for result in results['results']:
                        thumbLocal = orgt.getThumbnailForItem(itemId=result['id'],fileName=result['title'],filePath=iconPath)
                        result['thumbnail']=thumbLocal
                        groups.append(result)
                       
            if len(groups) > 0:
                print "%s items found" % str(len(groups))
                file.write(unicode(json.dumps(groups, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))))                                              
            file.close()                                                                                    
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)                      