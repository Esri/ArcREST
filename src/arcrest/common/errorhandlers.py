"""
contains all error handlers for ArcREST
"""

MSGS = {
    100 : "100: Invalid Inputs",
    200 : "200: Error with the GET Operation",
    201 : "201: Error with the POST operation",
    202 : "202: Error with the MultiPart POST operation",
    203 : "203: Error with the download operation",
    400 : "Invalid Username/Password",
    401 : "Invalid token. Check the username and password and try again.",
    404 : "Invalid URL",
    -99999 : "An unknown error has been raised."

}
import json
#--------------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys, inspect
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror
########################################################################
class ArcRESTError(Exception):
    """default type of error handler raised"""
    pass
if __name__ == "__main__":
    try:
        print trace()
    except ZeroDivisionError, f:
        msg = json.dumps({"message" : MSGS[100],
                            "trace" : trace()})
        print msg, type()
        raise ArcRESTError()
    except ArcRESTError, e:
        print e.message