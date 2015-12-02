
"""
    @author: ArcREST Team
    @contact:  www.github.com/Esri/ArcREST
    @company: Esri
    @version: 1.0.0
    @description:  Querys a layer using ArcMap Creds.
    @requirements: Python 2.7.x, ArcGIS 10.3, ArcREST 3.5.0
    @copyright: Esri, 2015
"""
import os
from arcpy import env
from arcpy import mapping
from arcpy import da
import arcpy
import arcrest
from arcrest.security import ArcGISTokenSecurityHandler
from arcrest.agol import FeatureLayer

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
        url = str(argv[0])

        arcgisSH = ArcGISTokenSecurityHandler()
        if arcgisSH.valid == False:
            arcpy.AddError(arcgisSH.message)
            return
        fl = FeatureLayer(
            url=url,
            securityHandler=arcgisSH,
            initialize=True)

        res = fl.query(where="1=1",out_fields='*',returnGeometry=False)
        arcpy.AddMessage(res)
        arcpy.SetParameterAsText(1, str(res))
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