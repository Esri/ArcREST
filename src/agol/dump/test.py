
import httplib
import urllib
import urllib2
import os
from base import BaseAGOLClass
import base64
########################################################################
class AGOL2(BaseAGOLClass):
    """ performs the admin functions for portal/agol """
    _base_url = ""
    _token_url = ""
    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """Constructor"""
        self._username = username
        self._password = password
        self._token = self.generate_token()
       
if __name__ == "__main__":
    import urllib2
    import urllib
    p = AGOL2("AndrewSolutions", "fujiFUJI1")
    #filesUp = {"file": open(sd, 'rb')}
    base_url = "{}/content/users/{}/addItem".format("http://www.arcgis.com/sharing/rest", 
                                                    p.username)    
    url = base_url + "?f=json&token="+ p.generate_token() + \
        "&filename="+ "test.csv" + \
        "&type=CSV"\
        "&title="+ "service_name" + \
        "&tags="+ "csv" +\
        "&description="+ "description"       
    dataObj = open(r"C:\temp\test.csv", 'rb').read()
    
    data = {"file": base64.b64encode(dataObj)}
    #dataObj.close()
    #del dataObj
    req = urllib2.Request(url, urllib.urlencode(data))
    req.add_header('Content-Length', '%d' % os.stat(r"c:\temp\test.csv").st_size )
    req.add_header('Content-Type', 'application/octet-stream')
    res = urllib2.urlopen(req)
    print res.read()
    print 'stop'
    
    