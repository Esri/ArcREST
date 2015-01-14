"""
    @author:
    @contact:
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.2, ArcREST 2.0
    @copyright: Esri, 2014
"""
import os
import json
from arcpy import env
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
def get_config_value(config_file, section, variable):
    """ extracts a config file value """
    try:
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_file)
        return parser.get(section, variable)
    except:
        return None
#--------------------------------------------------------------------------
def main(*argv):
    """ main driver of program """
    try:
        adminUsername = str(argv[0])
        adminPassword = str(argv[1])
        baseURL = str(argv[2]) #"https://www.arcgis.com/sharing/rest"#
        inviteSubject = str(argv[3])
        inviteEmail = str(argv[4])
        newUserName = argv[5]
        firstName = argv[6]
        lastName = argv[7]
        password = argv[8]
        email = argv[9]
        account_role = argv[10]
        #   Local Variables
        #
        isAdded = True
        #   Logic
        #
        #   Access AGOL
        #
        sh = arcrest.AGOLTokenSecurityHandler(adminUsername, adminPassword)
        userInvite = arcrest.manageorg.UserInvite(username=newUserName,
                                                  password=password,
                                                 firstName=firstName,
                                                 lastName=lastName,
                                                 email=email,
                                                 role=account_role)
        admin = arcrest.manageorg.Administration(securityHandler=sh, initialize=True)

        #   Get the Org ID
        #
        community = admin.community
        user = community.user
        userDetails = user.user(username=adminUsername)
        orgID = userDetails['orgId']
        #   Access the Admin's Portal to Add User
        #
        portal = admin.portals(portalId=orgID)
        #   Validate the username to ensure it's free
        #   If it is not, raise error, else continue
        res = community.checkUserName(newUserName)
        if res['usernames'][0]['suggested'] != res['usernames'][0]['requested']:
            arcpy.AddError("Username %s is already taken" % newUserName)
        del community
        #   Add the User
        #
        res = portal.inviteUser(invitationList=userInvite,
                                html="welcome to the group",
                                subject="user invite to AGOL")
        for msg in res['notInvited']:
            arcpy.AddWarning("%s was not invited" % msg)
            isAdded = False
        del sh
        del portal
        del res
        arcpy.SetParameterAsText(11, isAdded)

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