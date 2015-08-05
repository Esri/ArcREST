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

class BaseWebOperations(object):
    """ base class that holds all the common web request operations """
    _referer_url = None
    _useragent = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def _download_file(self,
                            url, save_path,
                            securityHandler=None,
                            file_name=None, param_dict=None,
                            proxy_url=None, proxy_port=None):
        """ downloads a file """
        try:
            handlers = []
            cj = None
            handler = None
            param_dict, handler, cj = self.__processHandler(securityHandler=securityHandler,
                                                           param_dict={})
            handlers.append(urllib2.HTTPHandler(debuglevel=0))
            handlers.append(AGOLRedirectHandler())
            if proxy_url is not None:
                if proxy_port is None:
                    proxy_port = 80
                proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                           "https":"https://%s:%s" % (proxy_url, proxy_port)}
                proxy_support = urllib2.ProxyHandler(proxies)
                handlers.append(proxy_support)
            if handler is not None:
                handlers.append(handler)
            if cj is not None:
                handlers.append(urllib2.HTTPCookieProcessor(cj))
            opener = urllib2.build_opener(*handlers)
            urllib2.install_opener(opener)
            if param_dict is not None and \
               len(param_dict.keys()) > 0:
                encoded_args = urllib.urlencode(param_dict)
                url = url + '?' + encoded_args

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
                if securityHandler.method.lower() == "token":
                    self._download_file(url=file_data.geturl(),
                                        save_path=save_path,
                                        file_name=file_name,
                                        securityHandler=None,
                                        proxy_url=self._proxy_url,
                                        proxy_port=self._proxy_port)
                else:
                    self._download_file(url=file_data.geturl(),
                                        save_path=save_path,
                                        file_name=file_name,
                                        securityHandler=securityHandler,
                                        proxy_url=self._proxy_url,
                                        proxy_port=self._proxy_port)
                return save_path + os.sep + file_name
            if (file_data.info().getheader('Content-Length')):
                total_size = int(file_data.info().getheader('Content-Length').strip())
                downloaded = 0
                CHUNK = 4096
                with open(save_path + os.sep + file_name, 'wb') as out_file:
                    while True:
                        chunk = file_data.read(CHUNK)
                        downloaded += len(chunk)
                        if not chunk: break
                        out_file.write(chunk)
            elif file_data.headers.maintype=='image':
                with open(save_path + os.sep + file_name, 'wb') as out_file:
                    buf = file_data.read()
                    out_file.write(buf)
            return save_path + os.sep + file_name
        except urllib2.HTTPError, e:
            print "HTTP Error:",e.code , url
            return None
        except urllib2.URLError, e:
            print "URL Error:",e.reason , url
            return None
    #----------------------------------------------------------------------
    def _get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    #----------------------------------------------------------------------
    def __processHandler(self, securityHandler, param_dict):
        """proceses the handler and returns the cookiejar"""
        cj = None
        handler = None
        if securityHandler is None:
            pass
        elif securityHandler.method.lower() == "token":
            param_dict['token'] = securityHandler.token
            if hasattr(securityHandler, 'cookiejar'):
                cj = securityHandler.cookiejar
            if hasattr(securityHandler, 'handler'):
                handler = securityHandler.handler
        elif securityHandler.method.lower() == "handler":
            #if "token" in param_dict :
                #del param_dict['token']
            handler = securityHandler.handler
            cj = securityHandler.cookiejar


        return param_dict, handler, cj
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, securityHandler=None,
                header=None, proxy_url=None, proxy_port=None,
                compress=True):
        """
        Performs a standard GET method.
        Inputs:
           url - string of URI
           param_dict - parameters dictionary that holds key/values for
                        each function call.
           handler - security Handler object
           header - optional headers to add to a call
           proxy_url - URI/IP of the proxy
           proxy_port - port of the proxy
           compress - compression of the call
        """
        handlers = []
        param_dict, handler, cj = self.__processHandler(securityHandler=securityHandler,
                                                        param_dict=param_dict)

        headers = [('User-Agent', self._useragent),
                   ('Accept-Encoding', '')]
        if securityHandler is not None:
            headers.append (('Referer', securityHandler._referer_url))
        else:
            headers.append (('Referer', self._referer_url))
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
            handlers.append(proxy_support)
        if handler is not None:
            handlers.append(handler)
        if cj is not None:
            handlers.append(urllib2.HTTPCookieProcessor(cj))
        handlers.append(AGOLRedirectHandler())
        if len(handlers) > 0:
            opener = urllib2.build_opener(*handlers)
        opener.addheaders = headers
        if len(str(urllib.urlencode(param_dict))) + len(url)> 1999:
            resp = opener.open(url, data=urllib.urlencode(param_dict))
        else:
            format_url = url + "?%s" % urllib.urlencode(param_dict)
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
            return resp_data
        if result is None:
            return None

        if 'error' in result:
            if 'message' in result['error']:
                if result['error']['message'] == 'Request not made over ssl':
                    if url.startswith('http://'):
                        url = url.replace('http://', 'https://')
                        return self._do_get(url=url,
                                            param_dict=param_dict,
                                            securityHandler=securityHandler,
                                            proxy_url=proxy_url,
                                            proxy_port=proxy_port,
                                            compress=compress)
                else:
                    print result['error']
        if 'status' in result and type(result) is dict:
            if result['status'] == 'error':
                print str(result['code']) + " " + str(result['messages'])
        return self._unicode_convert(result)

    #----------------------------------------------------------------------
    def _do_post(self,
                 url,
                 param_dict,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 header={}):
        """ performs the POST operation and returns dictionary result """
        handlers = []
        opener= None
        param_dict, handler, cj = self.__processHandler(securityHandler=securityHandler,
                                                        param_dict=param_dict)
        headers = {
           'User-Agent': self._useragent,
           'Accept-Encoding': ''}
        if securityHandler is not None:
            headers['Referer'] = securityHandler._referer_url
        else:
            headers['Referer'] = self._referer_url
        if len(header) > 0 :
            headers = dict(headers.items() + header.items())

        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = urllib2.ProxyHandler(proxies)
            handlers.append(proxy_support)
        if handler is not None:
            handlers.append(handler)
        if cj is not None:
            handlers.append(urllib2.HTTPCookieProcessor(cj))
        handlers.append(AGOLRedirectHandler())
        if len(handlers) > 0:
            opener = urllib2.build_opener(*handlers)
        urllib2.install_opener(opener)

        request = urllib2.Request(url, urllib.urlencode(param_dict), headers=headers)
        result = ""
        try:
            result = urllib2.urlopen(request,data=urllib.urlencode(param_dict)).read()
            if result =="":
                return ""
            jres = json.loads(result)
        except urllib2.HTTPError,e:
            return {'error':{'code':e.code}}
        except Exception, f:
            print f
            return result
        #jres = json.loads(result)
        if 'error' in jres:
            if 'message' in jres['error']:
                if jres['error']['message'] == 'Request not made over ssl':
                    if url.startswith('http://'):
                        url = url.replace('http://', 'https://')
                        return self._do_post(url,
                                             param_dict,
                                             securityHandler=securityHandler,
                                             header=header,
                                             proxy_url=proxy_url,
                                             proxy_port=proxy_port)
                else:
                    print jres['error']
        if 'status' in jres:
            if jres['status'] == 'error':
                print str(jres['code']) + " " + str(jres['messages'])
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _post_multipart(self, host, selector,
                        fields, files,
                        securityHandler=None,
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
        cj = None
        handlers = []
        param_dict, handler, cj = self.__processHandler(securityHandler=securityHandler,
                                                       param_dict=fields)
        content_type, body = self._encode_multipart_formdata(param_dict, files)
        url = self._assemble_url(host, selector, port, ssl)
        handlers.append(AGOLRedirectHandler())
        handlers.append(urllib2.HTTPHandler(debuglevel=0))
        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            handlers.append(urllib2.ProxyHandler(proxies))
        if handler is not None:
            handlers.append(handler)
        if cj is not None:
            handlers.append(urllib2.HTTPCookieProcessor(cj))
        opener = urllib2.build_opener(*handlers)
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
                                                securityHandler=securityHandler,
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
                buf.write('Content-Type: %s\r\n' % (self._get_content_type(filename)))
                file = open(filepath, "rb")
                try:
                    buf.write('\r\n' + file.read() + '\r\n')
                finally:
                    file.close()
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, buf
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
    def _assemble_url(self, host, selector, port=80, ssl=False):
        """creates the url string for the request"""
        if not port is None and \
           port != 80:
            if ssl:
                url = "https://%s:%s%s" % (host, port, selector)
            else:
                url = "http://%s:%s%s" % (host, port, selector)
        else:
            if ssl:
                url = "https://%s%s" % (host, selector)
            else:
                url = "http://%s%s" % (host, selector)
        return url
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
