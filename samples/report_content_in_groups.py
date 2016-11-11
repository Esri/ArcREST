"""
   This sample shows how to create a list in json
   of all items in a group

   Python 2.x/3.x
   ArcREST 3.5,6
"""
from __future__ import print_function
from __future__ import absolute_import

import arcrest
import os
import json
from arcresthelper import orgtools, common
import csv
import sys
from arcresthelper.packages import six

def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect,sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror
def _unicode_convert(obj):
    """ converts unicode to anscii """
    if isinstance(obj, dict):
        return {_unicode_convert(key): _unicode_convert(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_unicode_convert(element) for element in obj]
    elif isinstance(obj, str):
        return obj 
    elif isinstance(obj, six.text_type):
        return obj.encode('utf-8')
    elif isinstance(obj, six.integer_types):
        return obj
    else:
        return obj

if __name__ == "__main__":
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

    groups = ["Demographic Content"] #Name of groups
    outputlocation = r"C:\TEMP"
    outputfilename = "group.json"
    outputitemID = "id.csv"
    try:

        orgt = orgtools.orgtools(securityinfo)

        groupRes = []
        if orgt.valid:
            fileName = os.path.join(outputlocation,outputfilename)
            csvFile = os.path.join(outputlocation,outputitemID)
            iconPath = os.path.join(outputlocation,"icons")
            if not os.path.exists(iconPath):
                os.makedirs(iconPath)
                
            if sys.version_info[0] == 2:
                access = 'wb+'
                kwargs = {}
            else:
                access = 'wt+'
                kwargs = {'newline':''}
            file = open(fileName, "w")
            with open(fileName, access, **kwargs) as csvFile:
                idwriter = csv.writer(csvFile)
                for groupName in groups:
                    results = orgt.getGroupContent(groupName=groupName,
                                                   onlyInOrg=True,
                                                   onlyInUser=True)

                    if not results is None:
                        for result in results:
                            idwriter.writerow([result['title'],result['id']])
                            thumbLocal = orgt.getThumbnailForItem(itemId=result['id'],
                                                                  fileName=result['title'],
                                                              filePath=iconPath)
                            result['thumbnail']=thumbLocal
                            groupRes.append(result)

                if len(groupRes) > 0:
                    print ("%s items found" % str(len(groupRes)))
                    groupRes = _unicode_convert(groupRes)
                    file.write(json.dumps(groupRes, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
            file.close()
    except (common.ArcRestHelperError) as e:
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