"""
   Base Class from which AGOL function inherit from.
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
    def generate_token(self, tokenURL=None):
        """ generates a token for a feature service """
        referer='https://www.arcgis.com'
        if tokenURL is None:
            tokenUrl  = 'https://arcgis.com/sharing/rest/generateToken'
        query_dict = {'username': self._username,
                      'password': self._password,
                      'expiration': str(60),
                      'referer': referer,
                      'f': 'json'}
        query_string = urllib.urlencode(query_dict)
        token = json.loads(urllib.urlopen(tokenUrl + "?f=json", query_string).read())
        if "token" not in token:
            self._token = None
            return None
        else:
            httpPrefix = "http://www.arcgis.com/sharing/rest"
            if token['ssl'] == True:
                httpPrefix = "https://www.arcgis.com/sharing/rest"
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
    def _post_multipart(self, host, selector, 
                        filename, filetype, 
                        content, fields,
                        port=None,
                        https=False):
        """ performs a multi-post to AGOL or AGS 
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               filename - string - name file will be called on server
               filetype - string - mimetype of data uploading
               content - binary data - derived from open(<file>, 'rb').read()
               fields - dictionary - additional parameters like token and format information
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
                               filename="Jellyfish.jpg",
                               content=open(r"c:\temp\Jellyfish.jpg, 'rb').read(),
                               fields=params
                               )
        """
        body = ''
        for field in fields.keys():
            body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="' + field + '"\r\n\r\n' + fields[field] + '\r\n'
        body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="file"; filename="'
        body += filename + '"\r\nContent-Type: ' + filetype + '\r\n\r\n'
        body = body.encode('utf-8')
        body += content + '\r\n------------ThIs_Is_tHe_bouNdaRY_$--\r\n'
        if https:
            h = httplib.HTTPSConnection(host, port=port)
        else:
            h = httplib.HTTPConnection(host, port=port)
        h.putrequest('POST', selector)
        h.putheader('content-type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$')
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        res = h.getresponse()
        return res.read()        
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
        