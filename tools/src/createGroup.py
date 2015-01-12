"""
    @author: ArcREST Team
    @contact: www.github.com/Esri/ArcREST
    @company: Esri
    @version: 1.0.0
    @description: creates a user group
    @requirements: Python 2.7.x, ArcGIS 10.2.2, ArcREST 2.0
    @copyright: Esri, 2015
"""
from arcpy import env
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
        #   Inputs
        #
        adminUsername = argv[0]
        adminPassword = argv[1]
        siteURL = argv[2]
        groupTitle = argv[3]
        groupTags = argv[4]
        description = argv[5]
        access = argv[6]

        #   Logic
        #
        #   Connect to the site
        #
        sh = arcrest.AGOLTokenSecurityHandler(adminUsername, adminPassword)
        admin = arcrest.manageorg.Administration(url=siteURL,
                                                securityHandler=sh,
                                                initialize=True)
        community = admin.community
        #   Create Group
        #
        res = community.createGroup(title=groupTitle,
                                    tags=groupTags,
                                    description=description,
                                    snippet="",
                                    phone="",
                                    access=access,
                                    sortField="title",
                                    sortOrder="asc",
                                    isViewOnly=False,
                                    isInvitationOnly=False,
                                    thumbnail=None)
        arcpy.SetParameterAsText(7, str(res))
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