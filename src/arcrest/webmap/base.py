"""
   Contains base classes for webmap objects
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
class BaseDomain:
    """ all domain values inherit this class """
    pass
########################################################################
class BaseDefinition(object):
    """ class that all definition objects inherit from """
    pass
########################################################################
class BaseSymbol(object):
    """ class that all symbol object inherit from """
    pass
########################################################################
class BaseRenderer(object):
    """ all renderers inherit this class """
    pass
########################################################################
class Geometry(object):
    ''' all geometry classes inherit this class '''
    pass
########################################################################
class BaseWebOperations(object):
    """ base class that holds operations for web requests """
    _token = None
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
    def _do_post(self, url, param_dict, proxy_url=None, proxy_port=None):
        """ performs the POST operation and returns dictionary result """
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
    def _do_get(self, url, param_dict, header={}, proxy_url=None, proxy_port=None):
        """ performs a get operation """
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
                        ssl=False,port=80,
                        proxy_url=None, proxy_port=None):
        """ performs a multi-post to AGOL or AGS
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               fields - dictionary - additional parameters like token and format information
               files - tuple array- tuple with the file name type, filename, full path
               ssl - option to use SSL
               proxy_url - string - url to proxy server
               proxy_port - interger - port value if not on port 80

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
########################################################################
class BaseOperationalLayer(object):
    """ Base Class for all Operational Layers  """
    _id = None
    _title = None
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the id value """
        return self._id
    #----------------------------------------------------------------------
    @id.setter
    def id(self, value):
        """ sets the id value """
        if value is not None:
            self._id = value
    #----------------------------------------------------------------------
    @property
    def title(self):
        """ returns the title value """
        return self._title
    #----------------------------------------------------------------------
    @title.setter
    def title(self, value):
        """ sets the title value """
        if self._title is not None:
            self._title = value
########################################################################
class BaseSecurityHandler(BaseWebOperations):
    """ All Security Objects inherit from this class """
    _token = None
    pass
