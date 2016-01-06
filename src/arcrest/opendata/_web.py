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
import gzip
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

import six
from six.moves.urllib import request
from six.moves import http_cookiejar as cookiejar
from six.moves.urllib_parse import urlencode, urlparse
########################################################################
__all__ = ['_get', '_post']
__version__ = '1.0.0'
_referer_url = None
_useragent = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
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
#----------------------------------------------------------------------
def _get_file_name(contentDisposition, url, ext=".unknown"):
    """ gets the file name from the header or url if possible """
    if six.PY2:
        if contentDisposition is not None:
            return re.findall(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)',
                              contentDisposition.strip().replace('"', ''))[0][0]
        elif os.path.basename(url).find('.') > -1:
            return os.path.basename(url)
    elif six.PY3:
        if contentDisposition is not None:
            p = re.compile(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)')
            return p.findall(contentDisposition.strip().replace('"', ''))[0][0]
        elif os.path.basename(url).find('.') > -1:
            return os.path.basename(url)
    return "%s.%s" % (uuid.uuid4().get_hex(), ext)
#----------------------------------------------------------------------
def _processHandler(securityHandler, param_dict):
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
def _process_response(resp):
    """ processes the response object"""
    CHUNK = 4056
    maintype = _mainType(resp)
    contentDisposition = resp.headers.get('content-disposition')
    contentEncoding = resp.headers.get('content-encoding')
    contentType = resp.headers.get('content-type')
    contentLength = resp.headers.get('content-length')
    if maintype.lower() in ('image',
                            'application/x-zip-compressed') or \
       contentType == 'application/x-zip-compressed' or \
       (contentDisposition is not None and \
        contentDisposition.lower().find('attachment;') > -1):
        fname = _get_file_name(
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
            for data in _chunk(response=resp):
                writer.write(data)
                del data
            del writer
        return file_name
    else:
        read = ""
        for data in _chunk(response=resp, size=4096):
            read += data.decode('ascii')
            del data
        try:
            return json.loads(read.strip())
        except:
            return read
    return None
#----------------------------------------------------------------------
def _make_boundary():
    """ creates a boundary text"""
    if six.PY2:
        return '===============%s==' % uuid.uuid4().get_hex()
    else:
        return '===============%s==' % uuid.uuid4().hex
#----------------------------------------------------------------------
def _get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
#----------------------------------------------------------------------
def _mainType(resp):
    """ gets the main type from the response object"""
    if six.PY2:
        return resp.headers.maintype
    elif six.PY3:
        return resp.headers.get_content_maintype()
    else:
        return None
#----------------------------------------------------------------------
def _chunk(response, size=4096):
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
def _post(url,
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
    headers = {}
    lheaders = []
    opener = None
    return_value = None
    handlers = [RedirectHandler()]
    param_dict, handler, cj = _processHandler(securityHandler, param_dict)
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
        if six.PY3:
            data = data.encode('ascii')
        opener.data = data
        resp = opener.open(url, data=data)
    else:
        mpf = MultiPartForm(param_dict=param_dict,
                            files=files)
        req = request.Request(url)
        body = mpf.make_result
        req.add_header('User-agent', _useragent)
        req.add_header('Content-type', mpf.get_content_type())
        req.add_header('Content-length', len(body))
        req.data = body
        resp = request.urlopen(req)
    return_value = _process_response(resp)

    if isinstance(return_value, dict):
        if "error" in return_value and \
           'message' in return_value['error']:
            if return_value['error']['message'].lower() == 'request not made over ssl':
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
                    return _post(url,
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
def _get(url,
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
    CHUNK = 4056
    param_dict, handler, cj = _processHandler(securityHandler, param_dict)
    headers = [] + additional_headers
    if compress:
        headers.append(('Accept-encoding', 'gzip'))
    else:
        headers.append(('Accept-encoding', ''))
    headers.append(('User-Agent', _useragent))
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
        resp = opener.open(url, data=urllib.urlencode(param_dict))
    else:
        format_url = url + "?%s" % urlencode(param_dict)
        resp = opener.open(fullurl=format_url)
    #  Get some headers from the response
    maintype = _mainType(resp)
    contentDisposition = resp.headers.get('content-disposition')
    contentEncoding = resp.headers.get('content-encoding')
    contentType = resp.headers.get('content-Type').split(';')[0].lower()
    contentLength = resp.headers.get('content-length')
    if maintype.lower() in ('image',
                            'application/x-zip-compressed') or \
       contentType == 'application/x-zip-compressed' or \
       (contentDisposition is not None and \
       contentDisposition.lower().find('attachment;') > -1): # "application",

        fname = _get_file_name(
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
            for data in _chunk(response=resp, size=CHUNK):
                writer.write(data)
                writer.flush()
            writer.flush()
            del writer
        return file_name
    else:
        read = ""
        for data in _chunk(response=resp, size=CHUNK):
            try:
                read += data.decode('ascii')
            except:
                read += data.decode('utf-8')

            del data
        try:
            results = json.loads(read)
            if 'error' in results:
                if 'message' in results['error']:
                    if results['error']['message'] == 'Request not made over ssl':
                        if url.startswith('http://'):
                            url = url.replace('http://', 'https://')
                            return _do_get(url,
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
