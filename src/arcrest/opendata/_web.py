"""
   Contains POST and GET web operations for
   OpenData Python Package.
"""

#from __future__ import absolute_import
from __future__ import print_function
import io
import os
import re
import sys
import json
import uuid
import zlib
import shutil
import tempfile
import mimetypes
import email.generator
from io import BytesIO
try:
    from cStringIO import StringIO
except:
    from io import StringIO

from ..packages.six.moves.urllib import request
from ..packages.six.moves import http_cookiejar as cookiejar
from ..packages.six.moves.urllib_parse import urlencode
########################################################################
__version__ = "3.5.3"

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
########################################################################
class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    files = []
    form_fields = []
    boundary = None
    form_data = ""
    #----------------------------------------------------------------------
    def __init__(self, param_dict={}, files={}):
        if len(param_dict) == 0:
            self.form_fields = []
        else:
            for k,v in param_dict.items():
                self.form_fields.append((k,v))
                del k,v
        if len(files) == 0:
            self.files = []
        else:
            for key,v in files.items():
                self.add_file(fieldname=key,
                              filename=os.path.basename(v),
                              filePath=v,
                              mimetype=None)
        self.boundary = email.generator._make_boundary()
    #----------------------------------------------------------------------
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary
    #----------------------------------------------------------------------
    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
    #----------------------------------------------------------------------
    def add_file(self, fieldname, filename, filePath, mimetype=None):
        """Add a file to be uploaded.
        Inputs:
           fieldname - name of the POST value
           fieldname - name of the file to pass to the server
           filePath - path to the local file on disk
           mimetype - MIME stands for Multipurpose Internet Mail Extensions.
             It's a way of identifying files on the Internet according to
             their nature and format. Default is None.
        """
        body = filePath
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
    #----------------------------------------------------------------------
    @property
    def make_result(self):
        if self.PY2:
            self._2()
        elif self.PY3:
            self._3()
        return self.form_data
    #----------------------------------------------------------------------
    def _2(self):
        """python 2.x version of formatting body data"""
        boundary = self.boundary
        buf = StringIO()
        for (key, value) in self.form_fields:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n%s\r\n' % value)
        for (key, filename, mimetype, filepath) in self.files:
            if os.path.isfile(filepath):
                buf.write('--{boundary}\r\n'
                    'Content-Disposition: form-data; name="{key}"; '
                    'filename="{filename}"\r\n'
                    'Content-Type: {content_type}\r\n\r\n'.format(
                        boundary=boundary,
                        key=key,
                        filename=filename,
                        content_type=mimetype))
                with open(filepath, "rb") as f:
                    shutil.copyfileobj(f, buf)
                buf.write('\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        self.form_data = buf
    #----------------------------------------------------------------------
    def _3(self):
        """ python 3 method"""
        boundary = self.boundary
        buf = BytesIO()
        textwriter = io.TextIOWrapper(
            buf, 'utf8', newline='', write_through=True)

        for (key, value) in self.form_fields:
            textwriter.write(
                '--{boundary}\r\n'
                'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                '{value}\r\n'.format(
                    boundary=boundary, key=key, value=value))
        for(key, filename, mimetype, filepath) in self.files:
            if os.path.isfile(filepath):
                textwriter.write(
                    '--{boundary}\r\n'
                    'Content-Disposition: form-data; name="{key}"; '
                    'filename="{filename}"\r\n'
                    'Content-Type: {content_type}\r\n\r\n'.format(
                        boundary=boundary, key=key, filename=filename,
                        content_type=mimetype))
                with open(filepath, "rb") as f:
                    shutil.copyfileobj(f, buf)
                textwriter.write('\r\n')
        textwriter.write('--{}--\r\n\r\n'.format(boundary))
        self.form_data = buf.getvalue()
########################################################################
class WebOperations(object):
    """performs the get/post operations"""
    PY3 = sys.version_info[0] == 3
    PY2 = sys.version_info[0] == 2
    _referer_url = None
    _last_url = None
    _last_code = None
    _last_method = None
    _useragent = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    #----------------------------------------------------------------------
    @property
    def last_method(self):
        """gets the last method used (either POST or GET)"""
        return self._last_method
    #----------------------------------------------------------------------
    @property
    def last_code(self):
        """gets the last code from the last web operation"""
        return self._last_code
    #----------------------------------------------------------------------
    @property
    def last_url(self):
        """gets the last web url called"""
        return self._last_url
    #----------------------------------------------------------------------
    @property
    def referer_url(self):
        """gets/sets the referer url value"""
        return self._referer_url
    #----------------------------------------------------------------------
    @referer_url.setter
    def referer_url(self, value):
        """gets/sets the referer url value"""
        if self._referer_url != value:
            self._referer_url = value
    #----------------------------------------------------------------------
    @property
    def useragent(self):
        """gets/sets the user agent value"""
        return self._useragent
    #----------------------------------------------------------------------
    @useragent.setter
    def useragent(self, value):
        """gets/sets the user agent value"""
        if value is None:
            self._useragent = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
        elif self._useragent != value:
            self._useragent = value
    #----------------------------------------------------------------------
    def _get_file_name(self, contentDisposition,
                       url, ext=".unknown"):
        """ gets the file name from the header or url if possible """
        if self.PY2:
            if contentDisposition is not None:
                return re.findall(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)',
                                  contentDisposition.strip().replace('"', ''))[0][0]
            elif os.path.basename(url).find('.') > -1:
                return os.path.basename(url)
        elif self.PY3:
            if contentDisposition is not None:
                p = re.compile(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)')
                return p.findall(contentDisposition.strip().replace('"', ''))[0][0]
            elif os.path.basename(url).find('.') > -1:
                return os.path.basename(url)
        return "%s.%s" % (uuid.uuid4().get_hex(), ext)
    #----------------------------------------------------------------------
    def _processHandler(self, securityHandler, param_dict):
        """proceses the handler and returns the cookiejar"""
        cj = None
        handler = None
        if securityHandler is None:
            cj = cookiejar.CookieJar()
        elif securityHandler.method.lower() == "token":
            param_dict['token'] = securityHandler.token
            if hasattr(securityHandler, 'cookiejar'):
                cj = securityHandler.cookiejar
            if hasattr(securityHandler, 'handler'):
                handler = securityHandler.handler
        elif securityHandler.method.lower() == "handler":
            handler = securityHandler.handler
            cj = securityHandler.cookiejar
        return param_dict, handler, cj
    #----------------------------------------------------------------------
    def _process_response(self, resp, out_folder=None):
        """ processes the response object"""
        CHUNK = 4056
        maintype = self._mainType(resp)
        contentDisposition = resp.headers.get('content-disposition')
        contentEncoding = resp.headers.get('content-encoding')
        contentType = resp.headers.get('content-type')
        contentLength = resp.headers.get('content-length')
        if maintype.lower() in ('image',
                                'application/x-zip-compressed') or \
           contentType == 'application/x-zip-compressed' or \
           (contentDisposition is not None and \
            contentDisposition.lower().find('attachment;') > -1):
            fname = self._get_file_name(
                contentDisposition=contentDisposition,
                url=resp.geturl())
            if out_folder is None:
                out_folder = tempfile.gettempdir()
            if contentLength is not None:
                max_length = int(contentLength)
                if max_length < CHUNK:
                    CHUNK = max_length
            file_name = os.path.join(out_folder, fname)
            with open(file_name, 'wb') as writer:
                for data in self._chunk(response=resp):
                    writer.write(data)
                    del data
                del writer
            return file_name
        else:
            read = ""
            for data in self._chunk(response=resp, size=4096):
                if self.PY3 == True:
                    read += data.decode('ascii')
                else:
                    read += data
                del data
            try:
                return json.loads(read.strip())
            except:
                return read
        return None
    #----------------------------------------------------------------------
    def _make_boundary(self):
        """ creates a boundary for multipart post (form post)"""
        if self.PY2:
            return '===============%s==' % uuid.uuid4().get_hex()
        elif self.PY3:
            return '===============%s==' % uuid.uuid4().hex
        else:
            from random import choice
            digits = "0123456789"
            letters = "abcdefghijklmnopqrstuvwxyz"
            return '===============%s==' % ''.join(choice(letters + digits) \
                                                   for i in range(15))
    #----------------------------------------------------------------------
    def _get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    #----------------------------------------------------------------------
    def _mainType(self, resp):
        """ gets the main type from the response object"""
        if self.PY2:
            return resp.headers.maintype
        elif self.PY3:
            return resp.headers.get_content_maintype()
        else:
            return None
    #----------------------------------------------------------------------
    def _chunk(self, response, size=4096):
        """ downloads a web response in pieces """
        method = response.headers.get("content-encoding")
        if method == "gzip":
            d = zlib.decompressobj(16+zlib.MAX_WBITS)
            b = response.read(size)
            while b:
                data = d.decompress(b)
                yield data
                b = response.read(size)
                del data
        else:
            while True:
                chunk = response.read(size)
                if not chunk: break
                yield chunk
    #----------------------------------------------------------------------
    def _post(self, url,
              param_dict={},
              files={},
              securityHandler=None,
              additional_headers={},
              custom_handlers=[],
              proxy_url=None,
              proxy_port=80,
              compress=True,
              out_folder=None,
              file_name=None):
        """
        Performs a POST operation on a URL.

        Inputs:
           param_dict - key/value pair of values
              ex: {"foo": "bar"}
           files - key/value pair of file objects where the key is
              the input name and the value is the file path
              ex: {"file": r"c:\temp\myfile.zip"}
           securityHandler - object that handles the token or other site
              security.  It must inherit from the base security class.
              ex: arcrest.AGOLSecurityHandler("SomeUsername", "SOMEPASSWORD")
           additional_headers - are additional key/value headers that a user
              wants to pass during the operation.
              ex: {"accept-encoding": "gzip"}
           custom_handlers - this is additional web operation handlers as a
              list of objects.
              Ex: [CustomAuthHandler]
           proxy_url - url of the proxy
           proxy_port - default 80, port number of the proxy
           compress - default true, determines if gzip should be used of not for
              the web operation.
           out_folder - if the URL requested returns a file, this will be the
              disk save location
           file_name - if the operation returns a file and the file name is not
             given in the header or a user wishes to override the return saved
             file name, provide value here.
        Output:
           returns dictionary or string depending on web operation.
        """
        self._last_method = "POST"
        headers = {}
        opener = None
        return_value = None
        handlers = [RedirectHandler()]
        param_dict, handler, cj = self._processHandler(securityHandler, param_dict)
        if handler is not None:
            handlers.append(handler)
        if cj is not None:
            handlers.append(request.HTTPCookieProcessor(cj))
        if isinstance(custom_handlers, list) and \
           len(custom_handlers) > 0:
            for h in custom_handlers:
                handlers.append(h)
        if compress:
            headers['Accept-Encoding'] = 'gzip'
        else:
            headers['Accept-Encoding'] = ''
        for k,v in additional_headers.items():
            headers[k] = v
            del k,v
        opener = request.build_opener(*handlers)
        request.install_opener(opener)
        opener.addheaders = [(k,v) for k,v in headers.items()]
        if len(files) == 0:
            data = urlencode(param_dict)
            if self.PY3:
                data = data.encode('ascii')
            opener.data = data
            resp = opener.open(url, data=data)
        else:
            mpf = MultiPartForm(param_dict=param_dict,
                                files=files)
            req = request.Request(url)
            body = mpf.make_result
            req.add_header('User-agent', self.useragent)
            req.add_header('Content-type', mpf.get_content_type())
            req.add_header('Content-length', len(body))
            req.data = body
            resp = request.urlopen(req)
        self._last_code = resp.getcode()
        self._last_url = resp.geturl()
        return_value = self._process_response(resp=resp,
                                              out_folder=out_folder)
        if isinstance(return_value, dict):
            if "error" in return_value and \
               'message' in return_value['error']:
                if return_value['error']['message'].lower() == 'request not made over ssl':
                    if url.startswith('http://'):
                        url = url.replace('http://', 'https://')
                        return self._post(url,
                                     param_dict,
                                     files,
                                     securityHandler,
                                     additional_headers,
                                     custom_handlers,
                                     proxy_url,
                                     proxy_port,
                                     compress,
                                     out_folder,
                                     file_name)
            return return_value
        else:
            return return_value
        return return_value
    #----------------------------------------------------------------------
    def _get(self, url,
             param_dict={},
             securityHandler=None,
             additional_headers=[],
             handlers=[],
             proxy_url=None,
             proxy_port=None,
             compress=True,
             custom_handlers=[],
             out_folder=None,
             file_name=None):
        """
        Performs a GET operation
        Inputs:

        Output:
           returns dictionary, string or None
        """
        self._last_method = "GET"
        CHUNK = 4056
        param_dict, handler, cj = self._processHandler(securityHandler, param_dict)
        headers = [] + additional_headers
        if compress:
            headers.append(('Accept-encoding', 'gzip'))
        else:
            headers.append(('Accept-encoding', ''))
        headers.append(('User-Agent', self.useragent))
        if len(param_dict.keys()) == 0:
            param_dict = None
        if handlers is None:
            handlers = []
        if handler is not None:
            handlers.append(handler)
        handlers.append(RedirectHandler())
        if cj is not None:
            handlers.append(request.HTTPCookieProcessor(cj))
        if proxy_url is not None:
            if proxy_port is None:
                proxy_port = 80
            proxies = {"http":"http://%s:%s" % (proxy_url, proxy_port),
                       "https":"https://%s:%s" % (proxy_url, proxy_port)}
            proxy_support = request.ProxyHandler(proxies)
            handlers.append(proxy_support)
        opener = request.build_opener(*handlers)
        opener.addheaders = headers
        if param_dict is None:
            resp = opener.open(url, data=param_dict)
        elif len(str(urlencode(param_dict))) + len(url) >= 1999:
            resp = opener.open(url, data=urlencode(param_dict))
        else:
            format_url = url + "?%s" % urlencode(param_dict)
            resp = opener.open(fullurl=format_url)
        self._last_code = resp.getcode()
        self._last_url = resp.geturl()
        #  Get some headers from the response
        maintype = self._mainType(resp)
        contentDisposition = resp.headers.get('content-disposition')
        contentEncoding = resp.headers.get('content-encoding')
        contentType = resp.headers.get('content-Type').split(';')[0].lower()
        contentLength = resp.headers.get('content-length')
        if maintype.lower() in ('image',
                                'application/x-zip-compressed') or \
           contentType == 'application/x-zip-compressed' or \
           (contentDisposition is not None and \
           contentDisposition.lower().find('attachment;') > -1):

            fname = self._get_file_name(
                contentDisposition=contentDisposition,
                url=url)
            if out_folder is None:
                out_folder = tempfile.gettempdir()
            if contentLength is not None:
                max_length = int(contentLength)
                if max_length < CHUNK:
                    CHUNK = max_length
            file_name = os.path.join(out_folder, fname)
            with open(file_name, 'wb') as writer:
                for data in self._chunk(response=resp,
                                        size=CHUNK):
                    writer.write(data)
                    writer.flush()
                writer.flush()
                del writer
            return file_name
        else:
            read = ""
            for data in self._chunk(response=resp,
                                    size=CHUNK):
                if self.PY3 == True:
                    read += data.decode('ascii')
                else:
                    read += data

                del data
            try:
                results = json.loads(read)
                if 'error' in results:
                    if 'message' in results['error']:
                        if results['error']['message'] == 'Request not made over ssl':
                            if url.startswith('http://'):
                                url = url.replace('http://', 'https://')
                                return self._get(url,
                                               param_dict,
                                               securityHandler,
                                               additional_headers,
                                               handlers,
                                               proxy_url,
                                               proxy_port,
                                               compress,
                                               custom_handlers,
                                               out_folder,
                                               file_name)
                return results
            except:
                return read
