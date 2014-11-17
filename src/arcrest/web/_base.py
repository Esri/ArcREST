"""
   Base Class that all class that perform
   web operations will inherit from.
"""
import gzip
import os
import urllib
import urllib2
import json
import mimetypes
#import httplib
import mimetools
from cStringIO import StringIO
import re
class AGOLRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result


########################################################################
class BaseWebOperations(object):
    """ base class that holds operations for web requests """
    _token = None
    _referer_url = ""
    _useragent = "ArcREST"
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def _download_file(self, url, save_path, file_name=None, proxy_url=None, proxy_port=None):
        """ downloads a file """
        try:
            if url.find("http://") > -1:
                url = url.replace("http://", "https://")
            if proxy_url is not None:
                if proxy_port is None:
                    proxy_port = 80
                proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                           "https":"https://%s:%s" % (proxy_url, proxy_port)}
                proxy_support = urllib2.ProxyHandler(proxies)
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=0),AGOLRedirectHandler())
                urllib2.install_opener(opener)
            else:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0),AGOLRedirectHandler())
                urllib2.install_opener(opener)
            file_data = urllib2.urlopen(url)
            file_data.getcode()
            file_data.geturl()
            if file_name is None:
                url = file_data.geturl()
                a = file_data.info().getheader('Content-Disposition')
                if a is not None:
                    a = a.strip()
                    file_name = re.findall(r'filename=\"(.+?)\"', a)[0]
                else:
                    file_name = os.path.basename(file_data.geturl().split('?')[0])
            if hasattr(file_data, "status") and \
               (int(file_data.status) >= 300 and int(file_data.status) < 400):
                self._download_file(url=file_data.geturl(),
                                    save_path=save_path,
                                    file_name=file_name,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port)
                return save_path + os.sep + file_name
            total_size = int(file_data.info().getheader('Content-Length').strip())
            downloaded = 0
            CHUNK = 4096
            with open(save_path + os.sep + file_name, 'wb') as out_file:
                while True:
                    chunk = file_data.read(CHUNK)
                    downloaded += len(chunk)
                    if not chunk: break
                    out_file.write(chunk)
            return save_path + os.sep + file_name
        except urllib2.HTTPError, e:
            print "HTTP Error:",e.code , url
            return False
        except urllib2.URLError, e:
            print "URL Error:",e.reason , url
            return False
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict, proxy_url=None, proxy_port=None, header={}):
        """ performs the POST operation and returns dictionary result """

        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=0))
            urllib2.install_opener(opener)
        request = urllib2.Request(url, urllib.urlencode(param_dict), headers=header)
        result = urllib2.urlopen(request).read()
        if result =="":
            return ""
        jres = json.loads(result)
        if 'error' in jres:
            if jres['error']['message'] == 'Request not made over ssl':
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
                    return self._do_post( url, param_dict, proxy_url, proxy_port)

        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header=None, proxy_url=None, proxy_port=None,compress=True):
        """ performs a get operation """
        format_url = url + "?%s" % urllib.urlencode(param_dict)

        headers = [('Referer', self._referer_url),
                   ('User-Agent', self._useragent)]
        if not header is None  :
            headers.append(header)

        if compress:
            headers.append(('Accept-encoding', 'gzip'))
        opener= None

        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support, AGOLRedirectHandler())
        else:
            opener = urllib2.build_opener(AGOLRedirectHandler())
        opener.addheaders = headers
        resp = opener.open(format_url)
        if resp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(resp.read())
            f = gzip.GzipFile(fileobj=buf)
            resp_data = f.read()
        else:
            resp_data = resp.read()
        if resp_data == "" or resp_data == None or resp_data == 'null':
            return ""
        result = None
        try:
            result = json.loads(resp_data)
        except Exception,e:
            print e
        if result is None:
            return None

        if 'error' in result:
            if result['error']['message'] == 'Request not made over ssl':
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
                    return self._do_get(url=url,
                                        param_dict=param_dict,
                                        proxy_url=proxy_url,
                                        proxy_port=proxy_port,
                                        compress=compress)
        return self._unicode_convert(result)
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
    #----------------------------------------------------------------------------------
    def _post_multipart(self, host, selector,
                        fields, files,
                        ssl=False,port=80,
                        proxy_url=None,proxy_port=None):
        """ performs a multi-post to AGOL, Portal, or AGS
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
        content_type, body = self._encode_multipart_formdata(fields, files)

        if ssl:
            url = "https://%s%s" % (host, selector)
        else:
            url = "http://%s%s" % (host, selector)
        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=0))
            urllib2.install_opener(opener)
        request = urllib2.Request(url)
        request.add_header('User-agent', 'ArcREST')
        request.add_header('Content-type', content_type)
        request.add_header('Content-length', len(body))
        request.add_data(body)
        result = urllib2.urlopen(request).read()
        if result =="":
            return ""
        jres = json.loads(result)
        if 'error' in jres:
            if jres['error']['message'] == 'Request not made over ssl':
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
                    return self._post_multipart(host, selector,
                                                fields, files,
                                                ssl=True,port=port,
                                                proxy_url=proxy_url,
                                                proxy_port=proxy_port)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------------------
    def _encode_multipart_formdata(self, fields, files):
        boundary = mimetools.choose_boundary()
        buf = StringIO()
        for (key, value) in fields.iteritems():
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + self._tostr(value) + '\r\n')
        for (key, filepath, filename) in files:
            if os.path.isfile(filepath):
                buf.write('--%s\r\n' % boundary)
                buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
                buf.write('Content-Type: %s\r\n' % (self._get_content_type3(filename)))
                file = open(filepath, "rb")
                try:
                    buf.write('\r\n' + file.read() + '\r\n')
                finally:
                    file.close()
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, buf

    def _encode_multipart_formdataZip(self, fields, files):
        LIMIT = mimetools.choose_boundary()
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.iteritems():
            L.append('--' + LIMIT)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            if isinstance(value, bool):
                L.append(json.dumps(value))
            elif isinstance(value, list):
                L.append(str(value))
            else:
                L.append(self._tostr(value))
        for (key, value, filename) in files:
            L.append('--' + LIMIT)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self._get_content_type3(filename))
            L.append('')
            L.append(open(value, 'rb').read())

        L.append('--' + LIMIT + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % LIMIT
        return content_type, body

    def _get_content_type3(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    #----------------------------------------------------------------------
    def _tostr(self,obj):
        """ converts a object to list, if object is a list, it creates a
            comma seperated string.
        """
        if not obj:
            return ''
        elif isinstance(obj, list):
            return ', '.join(map(self._tostr, obj))
        elif isinstance(obj, bool):
            return json.dumps(obj)
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