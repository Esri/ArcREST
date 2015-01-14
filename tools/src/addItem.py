"""
    @author: ArcREST Team
    @contact:  www.github.com/Esri/ArcREST
    @company: Esri
    @version: 1.0.0
    @description:  Adds an SD to AGOL.
    @requirements: Python 2.7.x, ArcGIS 10.3, ArcREST 2.x
    @copyright: Esri, 2015
"""
import os
from arcpy import env
from arcpy import mapping
from arcpy import da
import arcpy
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
def main(*argv):
    """ main driver of program """
    try:
        username = str(argv[0])
        password = str(argv[1])
        baseURL = str(argv[2])
        folderId = str(argv[3])
        filePath = str(argv[4])
        #   Local variables
        #
        sh = None
        agol = None
        usercontent = None
        folderId = None
        proxy_port = None
        proxy_url = None
        #   Logic
        #
        if folderId == "":
            folderId = None
        if baseURL is None or \
           baseURL == "":
            baseURL = "https://www.arcgis.com/sharing/rest"
        sh = arcrest.AGOLTokenSecurityHandler(username=username, password=password)
        agol = arcrest.manageorg.Administration(url=baseURL, securityHandler=sh)
        usercontent = agol.content.usercontent(username)
        if isinstance(usercontent, arcrest.manageorg.administration._content.UserContent):
            pass
        res = usercontent.addItem(itemParameters=None, filePath=filePath, overwrite=True, folder=folderId)
        arcpy.SetParameterAsText(5, str(res))
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
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)