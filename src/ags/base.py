import httplib
import urlparse
import urllib
import urllib2
import json
import os
import common
########################################################################
class DynamicData(object):
    """base class for data source"""
    pass
########################################################################
class DataSource(object):
    """base class for data source"""
    pass
########################################################################
class Geometry(object):
    ''' base geometry class'''
    pass
########################################################################
class BaseAGSService(object):
    """ base class from which all service inherit """
    _username = None
    _password = None
    _token = None
    _url = None
    _token_url = None
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value
    @property
    def token_url(self):
        """ gets the token url"""
        return self._token_url
    @token_url.setter
    def token_url(self, value):
        """ sets the service's token url"""
        self._token_url = value
    def _reset(self):
        """ resets the class all values to None """
        self._url = None
        self._token = None
        self._username = None
        self._password = None
    @property
    def password(self):
        """ password is never returned """
        return "*******"
    @password.setter
    def password(self, value):
        """ sets the password """
        self._password = value
    @property
    def username(self):
        """ gets the username """
        return self._username
    @username.setter
    def username(self, value):
        """ sets the username """
        self._username = value
    #----------------------------------------------------------------------
    def _download_file(self, url, save_path, file_name):
        """ downloads a file """
        file_data = urllib2.urlopen(url)
        with open(save_path + os.sep + file_name, 'wb') as writer:
            writer.write(file_data.read())
        return save_path + os.sep + file_name    
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
                       content, fields):
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
            Output:
               response as string
        """
        body = ''
        for field in fields.keys():
            body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="' + field + '"\r\n\r\n' + fields[field] + '\r\n'
        body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="file"; filename="'
        body += filename + '"\r\nContent-Type: ' + filetype + '\r\n\r\n'
        body = body.encode('utf-8')
        body += content + '\r\n------------ThIs_Is_tHe_bouNdaRY_$--\r\n'
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$')
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()
    #----------------------------------------------------------------------
    def generate_token(self):#, username, password, tokenURL
        """ generates a token for AGS """
        params = urllib.urlencode({'username': self._username,
                                   'password': self._password,
                                   'client': 'requestip',
                                   'f': 'json'})        
        parsed_url = urlparse.urlparse(self._token_url)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        port = parsed_url.port
        if port is None:
            port = 80
        # Connect to URL and post parameters
        if parsed_url.scheme.lower() == "https":
            httpConn = httplib.HTTPSConnection(parsed_url.hostname, port)
        else:
            httpConn = httplib.HTTPConnection(parsed_url.hostname, port)
        httpConn.request("POST", parsed_url.path, params, headers)
        response = httpConn.getresponse()
        data = self._unicode_convert(json.loads(response.read()))
        httpConn.close()        
        del httpConn
        del response
        self._token = data['token']
        return  data['token'], data['expires']
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