import httplib
import urlparse
import urllib
import urllib2
import json
import os
########################################################################
class BaseFilter(object):
    """ base filter class """
    pass
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
class BaseAGSServer(object):
    """ base class from which all service inherit """
    _username = None
    _password = None
    _token = None
    _url = None
    _token_url = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    @property
    def proxy_port(self):
        """gets the proxy port"""
        return self._proxy_port
    #----------------------------------------------------------------------
    @property
    def proxy_url(self):
        """ gets the proxy URL """
        return self._proxy_url
    #----------------------------------------------------------------------
    @proxy_url.setter
    def proxy_url(self, value):
        """ sets the proxy url """
        self._proxy_url = value
    #----------------------------------------------------------------------
    @proxy_port.setter
    def proxy_port(self, value):
        """ sets the proxy port """
        if isinstance(value, int):
            self._proxy_port = value
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
    def _download_file(self, url, save_path, file_name, proxy_url=None, proxy_port=None):
        """ downloads a file """
        try:
            if proxy_url is not None:
                if proxy_port is None:
                    proxy_port = 80
                proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                           "https":"https://%s:%s" % (proxy_url, proxy_port)}
                proxy_support = urllib2.ProxyHandler(proxies)
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
                urllib2.install_opener(opener)
           
            file_data = urllib2.urlopen(url)
            total_size = int(file_data.info().getheader('Content-Length').strip())
            downloaded = 0
            CHUNK = 4096
            
            with open(save_path + os.sep + file_name, 'wb') as out_file:
                while True:
                    chunk = file_data.read(CHUNK)
                    downloaded += len(chunk)
                    if not chunk: break
                    #print str(int(math.floor(float(downloaded) / float(total_size) * 100 ))) + "% download"
                                                      
                    out_file.write(chunk)       
               
            return save_path + os.sep + file_name
        except urllib2.HTTPError, e:
            print "HTTP Error:",e.code , url
            return False
        except urllib2.URLError, e:
            print "URL Error:",e.reason , url
            return False
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict):
        """ performs the POST operation and returns dictionary result """
        proxy_url = self._proxy_url
        proxy_port = self._proxy_port
        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
            urllib2.install_opener(opener)
        request = urllib2.Request(url, urllib.urlencode(param_dict))
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header={}):
        """ performs a get operation """
        proxy_url = self._proxy_url
        proxy_port = self._proxy_port
        url = url + "?%s" % urllib.urlencode(param_dict)
        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
        request = urllib2.Request(url, headers=header)
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _post_multipart(self, host, selector, fields, files,
                        ssl=False,port=80):
        """ performs a multi-post to AGOL or AGS
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               fields - dictionary - additional parameters like token and format information
               files - tuple array- tuple with the file name type, filename, full path
               ssl - option to use SSL
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
        proxy_url = self._proxy_url
        proxy_port = self._proxy_port
        boundary, body = self._encode_multipart_formdata(fields, files)
        headers = {
        'User-Agent': "ArcREST",
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary
        }
        if proxy_url:
            if ssl:
                h = httplib.HTTPSConnection(proxy_url, proxy_port)
                h.request('POST', 'https://' + host + selector, body, headers)
            else:
                h = httplib.HTTPConnection(proxy_url, proxy_port)
                h.request('POST', 'http://' + host + selector, body, headers)
        else:
            if ssl:
                h = httplib.HTTPSConnection(host,port)
                h.request('POST', selector, body, headers)
            else:
                h = httplib.HTTPConnection(host,port)
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
    #----------------------------------------------------------------------
    def generate_token(self):
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
        ## Connect to URL and post parameters
        if self.proxy_url is not None:
            if parsed_url.scheme.lower() == "https":
                httpConn = httplib.HTTPSConnection(parsed_url.hostname, port)
            else:
                httpConn = httplib.HTTPConnection(parsed_url.hostname, port)
            httpConn.request('POST', '%s://%s%s'% (parsed_url.scheme, parsed_url.hostname, parsed_url.path), params, headers)
        else:
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
# This function is a workaround to deal with what's typically described as a
# problem with the web server closing a connection. This is problem
# experienced with www.arcgis.com (first encountered 12/13/2012). The problem
# and workaround is described here:
# http://bobrochel.blogspot.com/2010/11/bad-servers-chunked-encoding-and.html
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)