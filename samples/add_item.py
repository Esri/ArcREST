"""
   This sample shows how to add an item
   version 3.0.1
   Python 2
"""
import arcrest
from arcresthelper import securityhandlerhelper
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
    securityinfo['username'] = ""
    securityinfo['password'] = ""
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    upload_file = r"c:\test\test.png"
    try:

        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if shh.valid == False:
            print shh.message
        else:
            admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            content = admin.content
            userInfo = content.users.user()

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = 'Sample'
            #itemParams.thumbnail = None
            """
            Valid types
            "Shapefile", "CityEngine Web Scene", "Web Scene", "KML",
                         "Code Sample",
                         "Code Attachment", "Operations Dashboard Add In",
                         "CSV", "CSV Collection", "CAD Drawing", "Service Definition",
                         "Microsoft Word", "Microsoft Powerpoint",
                         "Microsoft Excel", "PDF", "Image",
                         "Visio Document", "iWork Keynote", "iWork Pages",
                         "iWork Numbers", "Map Document", "Map Package",
                         "Basemap Package", "Tile Package", "Project Package",
                         "Task File", "ArcPad Package", "Explorer Map",
                         "Globe Document", "Scene Document", "Published Map",
                         "Map Template", "Windows Mobile Package", "Pro Map",
                         "Layout", "Layer", "Layer Package", "File Geodatabase",
                         "Explorer Layer", "Geoprocessing Package", "Geoprocessing Sample",
                         "Locator Package", "Rule Package", "Workflow Manager Package",
                         "Desktop Application", "Desktop Application Template",
                         "Code Sample", "Desktop Add In", "Explorer Add In",
                         "ArcGIS Desktop Add-In", "ArcGIS Explorer Add-In",
                         "ArcGIS Explorer application configuration", "ArcGIS Explorer document"
            """
            itemParams.type = "Image"
            itemParams.overwrite = True
            itemParams.description = "Test File"
            itemParams.tags = "tags"
            itemParams.snippet = "Test File"
            itemParams.typeKeywords = "Data,Image,png"
            itemParams.filename = upload_file
            item = userInfo.addItem(
                itemParameters=itemParams,
                overwrite=True,
                relationshipType=None,
                originItemId=None,
                destinationItemId=None,
                serviceProxyParams=None,
                metadata=None)
            print item.title + " created"

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

if __name__ == "__main__":
    main()