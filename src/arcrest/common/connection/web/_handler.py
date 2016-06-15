from ...packages.six.moves.urllib import request


__version__ = "5.0.0"
########################################################################
class RedirectHandler(request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = request.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result
    #----------------------------------------------------------------------
    def http_error_302(self, req, fp, code, msg, headers):
        result = request.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result