import os
import urllib
import urllib2
import json
import httplib
import zipfile
import glob
import calendar
import datetime
import mimetypes
import mimetools
from cStringIO import StringIO
#import oauth2 as oauth

def _do_get(url, param_dict, header={}):
     """ performs a get operation """
     url = url + "?%s" % urllib.urlencode(param_dict)
     request = urllib2.Request(url, headers=header)
     result = urllib2.urlopen(request).read()
     jres = json.loads(result)
     return jres#self._unicode_convert(jres)

if __name__ == "__main__":
    try:
        client_id = ""
        client_secret = ""
        grant_type="client_credentials"
        request_token_url = "https://www.arcgis.com/sharing/oauth2/token"

        params = {
          "client_id" : "",
          "client_secret" : "",
          "grant_type":"client_credentials"
        }
        token = _do_get(url=request_token_url, param_dict=params)['access_token']
        #consumer = oauth.Consumer(key=client_id,
                         #secret=client_secret)
        #client = oauth.Client(consumer)

        ## The OAuth Client request works just like httplib2 for the most part.
        #resp, content = client.request(request_token_url, "GET")
        #print resp
        #print content
        params = {}
        params['token'] = token
        params['f'] = "json"
        url = "http://services2.arcgis.com/...."
        print _do_get(url, params)

    except ValueError, e:
        print e
