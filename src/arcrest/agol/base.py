"""

.. module:: base
   :platform: Windows, Linux
   :synopsis: Base Class from which AGOL function inherit from.

.. moduleauthor:: Esri


"""

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

########################################################################
class Geometry(object):
    """ Base Geometry Class """
    pass
########################################################################
class BaseAGOLClass(object):
    _token_url = None
    _token = None
    _username = None
    _password = None
    _org_url ="http://www.arcgis.com"
    _url = "http://www.arcgis.com/sharing/rest"
    _surl = "https://www.arcgis.com/sharing/rest"
    _referer_url = "https://www.arcgis.com"

    def initURL(self,org_url=None, rest_url=None,token_url=None,referer_url=None):

        if org_url is not None:
            if not org_url.startswith('http://') and not org_url.startswith('https://'):
                org_url = 'http://' + org_url
            self._org_url = org_url

        if rest_url is not None:
            self._url = rest_url
        else:
            self._url = self._org_url + "/sharing/rest"

        if self._url.startswith('http://'):
            self._surl = self._url.replace('http://', 'https://')
        else:
             self._surl  =  self._url

        if token_url is None:
            self._token_url = self._surl  + '/generateToken'
        else:
            self._token_url = token_url

        if referer_url is None:
            if not self._org_url.startswith('http://'):
                self._referer_url = self._org_url.replace('http://', 'https://')
            else:
                self._referer_url = self._org_url
        else:
            self._referer_url = referer_url



    #----------------------------------------------------------------------
    def _unzip_file(self, zip_file, out_folder):
        """ unzips a file to a given folder """
        try:
            zf = zipfile.ZipFile(zip_file, 'r')
            zf.extractall(path=out_folder)
            zf.close()
            del zf
            return True
        except:
            return False
    #----------------------------------------------------------------------
    def _date_handler(self, obj):
        if isinstance(obj, datetime.datetime):
            return calendar.timegm(obj.utctimetuple()) * 1000
        else:
            return obj
    #----------------------------------------------------------------------
    def _list_files(self, path):
        """lists files in a given directory"""
        files = []
        for f in glob.glob(pathname=path):
            files.append(f)
        files.sort()
        return files
    #----------------------------------------------------------------------
    def _download_file(self, url, save_path, file_name):
        """ downloads a file """
        file_data = urllib2.urlopen(url)
        with open(save_path + os.sep + file_name, 'wb') as writer:
            writer.write(file_data.read())
        return save_path + os.sep + file_name
    #----------------------------------------------------------------------
    def generate_token(self, referer=None, tokenURL=None):
        """ generates a token for a feature service """
        if referer is None:
            referer=self._referer_url
        if tokenURL is None:
            tokenUrl  = self._token_url

        query_dict = {'username': self._username,
                      'password': self._password,
                      'expiration': str(60),
                      'referer': referer,
                      'f': 'json'}
        query_string = urllib.urlencode(query_dict)
        result = urllib.urlopen(tokenUrl + "?f=json", query_string).read()
        try:
            token = json.loads(result)
        except:
            return None
        if "token" not in token:
            self._token = None
            return None
        else:
            httpPrefix = self._url
            if token['ssl'] == True:
                httpPrefix = self._surl
            self._token = token['token']
            return token['token'], httpPrefix
    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the user name """
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, value):
        """ sets the username """
        self._username = value
    #----------------------------------------------------------------------
    @property
    def password(self):
        """ getter for password """
        return "***"
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """ sets the username's password """
        self._password = value
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict):
        """ performs the POST operation and returns dictionary result """
        request = urllib2.Request(url, urllib.urlencode(param_dict))
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header={}):
        """ performs a get operation """
        url = url + "?%s" % urllib.urlencode(param_dict)
        request = urllib2.Request(url, headers=header)
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _post_multipart(self, host, selector, fields, files, ssl=False,port=None):
        """ performs a multi-post to AGOL or AGS
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               fields - dictionary - additional parameters like token and format information
               files - tuple array- tuple with the file name type, filename, full path
               ssl - option to use SSL
               port - interger - port value if not on port 80
            Output:
               JSON response as dictionary
            Useage:
               import urlparse
               url = "http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/SanFrancisco/311Incidents/FeatureServer/0/10261291"
               parsed_url = urlparse.urlparse(url)
               params = {"f":"json"}
               print _post_multipart(host=parsed_url.hostname,
                               selector=parsed_url.path,
                               files=files,
                               fields=params
                               )
        """
        boundary, body = self._encode_multipart_formdata(fields, files)
        headers = {
        'User-Agent': "ArcREST",
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary
        }
        if ssl:
            h = httplib.HTTPSConnection(host, port=port)
            h.request('POST', selector, body, headers)
        else:
            h = httplib.HTTPConnection(host, port=port)
            h.request('POST', selector, body, headers)
        return h.getresponse().read()
    #----------------------------------------------------------------------
    def _encode_multipart_formdata(self, fields, files):
        boundary = mimetools.choose_boundary()
        buf = StringIO()
        for (key, value) in fields.iteritems():
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + self._tostr(value) + '\r\n')
        for (key, filepath, filename) in files:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % (self._get_content_type(filename)))
            file = open(filepath, "rb")
            try:
                buf.write('\r\n' + file.read() + '\r\n')
            finally:
                file.close()
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf
    #----------------------------------------------------------------------
    def _get_content_type(self, filename):
        """ gets the content type of a file """
        mntype = mimetypes.guess_type(filename)[0]
        filename, fileExtension = os.path.splitext(filename)
        if mntype is None and\
            fileExtension.lower() == ".csv":
            mntype = "text/csv"
        elif mntype is None and \
            fileExtension.lower() == ".sd":
            mntype = "File/sd"
        elif mntype is None:
            #mntype = 'application/octet-stream'
            mntype= "File/%s" % fileExtension.replace('.', '')
        return mntype
    #----------------------------------------------------------------------
    def _tostr(self,obj):
        """ converts a object to list, if object is a list, it creates a
            comma seperated string.
        """
        if not obj:
            return ''
        if isinstance(obj, list):
            return ', '.join(map(self._tostr, obj))
        return str(obj)
    #----------------------------------------------------------------------
    def _unicode_convert(self, obj):
        """ converts unicode to anscii """
        if isinstance(obj, dict):
            return {self._unicode_convert(key): self._unicode_convert(value) for key, value in obj.iteritems()}
        elif isinstance(obj, list):
            return [self._unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj
