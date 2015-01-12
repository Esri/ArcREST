"""
    @author: ArcREST Team
    @contact: www.github.com/Esri/ArcREST
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.2, ArcREST 2.0
    @copyright: Esri, 2015
"""
import os
from arcpy import env
from arcpy import mapping
from arcpy import da
import arcpy
import ConfigParser
import arcrest
#--------------------------------------------------------------------------
class FunctionError(Exception):
    """ raised when a function fails to run """
    pass
#--------------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror
#--------------------------------------------------------------------------
def deleteItems(usercontentObj, itemId, folderId=None):
    """ erases an item """


#--------------------------------------------------------------------------
def main(*argv):
    """ main driver of program """
    try:
        #   Inputs
        #
        adminUsername = argv[0]
        adminPassword = argv[1]
        siteURL = argv[2]
        username = argv[3]
        subFolders = argv[4].lower() == "true"
        #   Logic
        #
        sh = arcrest.AGOLTokenSecurityHandler(adminUsername, adminPassword)
        admin = arcrest.manageorg.Administration(url=siteURL,
                                                 securityHandler=sh)
        content = admin.content
        if isinstance(content, arcrest.manageorg._content.Content):pass
        usercontent = content.usercontent(username=username)
        res = usercontent.listUserContent(username=adminUsername)
        #   Delete Root Items
        #
        eItems = ""
        itemsToErase = ",".join([item['id'] for item in res['items']])
        usercontent.deleteItems(items=itemsToErase)
        #  Walk Each Folder and erase items if subfolder == True
        #
        if subFolders:
            for folder in res['folders']:
                c = usercontent.listUserContent(username=username, folderId=folder['id'])
                itemsToErase = ",".join([item['id'] for item in c['items']])
                if len(itemsToErase.split(',')) > 0:
                    usercontent.deleteItems(items=itemsToErase)
                del c
                usercontent.deleteFolder(folderId=folder['id'])
                del folder

        arcpy.AddMessage("User %s content has been deleted." % username)
        arcpy.SetParameterAsText(4, True)
    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        arcpy.AddError("error on line: %s" % line)
        arcpy.AddError("error in file name: %s" % filename)
        arcpy.AddError("with error message: %s" % synerror)
        arcpy.AddError("ArcPy Error Message: %s" % arcpy.GetMessages(2))
    except FunctionError, f_e:
        messages = f_e.args[0]
        arcpy.AddError("error in function: %s" % messages["function"])
        arcpy.AddError("error on line: %s" % messages["line"])
        arcpy.AddError("error in file name: %s" % messages["filename"])
        arcpy.AddError("with error message: %s" % messages["synerror"])
        arcpy.AddError("ArcPy Error Message: %s" % messages["arc"])
    except:
        line, filename, synerror = trace()
        arcpy.AddError("error on line: %s" % line)
        arcpy.AddError("error in file name: %s" % filename)
        arcpy.AddError("with error message: %s" % synerror)
#--------------------------------------------------------------------------
if __name__ == "__main__":
    env.overwriteOutput = True
    argv = tuple(str(arcpy.GetParameterAsText(i))
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)