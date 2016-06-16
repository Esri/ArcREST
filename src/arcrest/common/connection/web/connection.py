"""
   Contains POST and GET web operations for
   ArcREST Python Package.
"""
from __future__ import absolute_import
from __future__ import print_function
import io
import os
import re
import ssl
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
except ImportError:
    from io import StringIO
from ._handler import RedirectHandler
from ...packages.six.moves.urllib import request
from ...packages.six.moves import http_cookiejar as cookiejar
from ...packages.six.moves.urllib_parse import urlencode

__version__ = "4.0.0"
__all__ = ['_connection']
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
    def __init__(self, param_dict=None, files=None):
        if param_dict is None:
            param_dict = {}
        if files is None:
            files = {}
        self.boundary = None
        self.files = []
        self.form_data = ""
        if len(self.form_fields) > 0:
            self.form_fields = []

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
                if isinstance(v, list):
                    fileName = os.path.basename(v[1])
                    filePath = v[0]
                else:
                    filePath = v
                    fileName = os.path.basename(v)
                self.add_file(fieldname=key,
                              filename=fileName,
                              filePath=filePath,
                              mimetype=None)
        self.boundary = "-%s" % email.generator._make_boundary()
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
###########################################################################
class _connection(object):
    PY3 = sys.version_info.major == 3
    PY2 = sys.version_info.major == 2
    _useragent = "ArcREST/{}".format(__version__)
    _verify = None
    _handlers = None
    _securityHandler = None
    _opener = None
    _proxy_handler = None
    _proxy_auth_handler = None
    #----------------------------------------------------------------------
    def __init__(self, verify=False):
        self._verify = verify
        self._handlers = []
        self._headers = {
            "User-Agent" : self._useragent,
            "Accept" : "*/*",
            "Accept-Encoding" : ""
        }
        if self._verify == False:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self._handlers.append(request.HTTPSHandler(context=ctx))
        self._handlers.append(request.HTTPCookieProcessor(cookiejar.CookieJar()))
        self._handlers.append(RedirectHandler())
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
            self._useragent = "geosaurus/{}".format(__version__)
        elif self._useragent != value:
            self._useragent = value
    #----------------------------------------------------------------------
    @property
    def handlers(self):
        """gets the handlers installed in the opener object"""
        return self._handlers
    #----------------------------------------------------------------------
    def reset(self):
        """resets the object back to the default state"""
        self._handlers = []
        self._opener = None
        if self._verify == False:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self._handlers.append(request.HTTPSHandler(context=ctx))
        self._handlers.append(request.HTTPCookieProcessor(cookiejar.CookieJar()))
        self._handlers.append(RedirectHandler())
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
    def _create_opener(self, securityHandler=None):
        """
        Builds the OpenDirector for the connection class
        """
        self._opener = None
        if self._opener is None:
            if securityHandler is not None and \
               securityHandler.method == "HANDLER":
                self._handlers.append(securityHandler.handler)
            if self._proxy_handler:
                self._handlers.insert(0,self._proxy_handler)
                if self._proxy_auth_handler:
                    self._handlers.append(self._proxy_handler)
            self._opener = request.build_opener(*self._handlers)
        return self._opener
    #----------------------------------------------------------------------
    def install_proxy(self, https=None, http=None, username=None, password=None):
        """
        Adds Proxy Support to the connection class with optional
        authentication

        Inputs:
         :https: the URL:PORT via the https scheme
         :http: the URL:PORT via the http scheme
         :username: if authentication, pass the proxy username
         :password: if authentication, pass the proxies' password for the
          username above.
        Output:
         None
        """
        if https or http:
            self._opener = None
            proxies = {}
            if https:
                proxies['https'] = https
            if http:
                proxies['http'] = http
            if username and password:
                password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
                if http:
                    password_mgr.add_password(None, http, username, password)
                if https:
                    password_mgr.add_password(None, https, username, password)
                self._proxy_handler = request.ProxyHandler(proxies)
                self._proxy_auth_handler = request.ProxyBasicAuthHandler(password_mgr)
            else:
                self._proxy_auth_handler = None
                self._proxy_handler = request.ProxyHandler(proxies)
                self._handlers.append(self._proxy_handler)
                return self._proxy_handler
        else:
            self._proxy_handler = None
            self._proxy_auth_handler = None
            if not self._opener is None:
                self._opener = None
    #----------------------------------------------------------------------
    def remove_proxy_handler(self):
        """
        Uninstalls all the handlers and resets the OpenDirector Object
        Input:
         None
        Output:
         boolean
        """
        self._proxy_handler = None
        self._proxy_auth_handler = None
        keeps = []
        for handler in self._handlers:
            if isinstance(handler, (request.ProxyBasicAuthHandler,
                                    request.ProxyHandler)) == False:
                keeps.append(handler)
        self._handlers = keeps
        if not self._opener is None:
            self._opener = None
        return True
    #----------------------------------------------------------------------
    @property
    def headers(self):
        return self._headers
    #----------------------------------------------------------------------
    def add_header(self, key, value):
        """
        Adds/Updates a header
        Inputs:
         :key: header value name
         :value: header value
        """
        self._headers[key] = value
    #----------------------------------------------------------------------
    def delete_header(self, key):
        """
        removes a header value
        Input
         :key: name of header to remove
        Output:
         boolean
        """
        if key in self._headers:
            del self._headers[key]
            return True
        return False
    #----------------------------------------------------------------------
    def _sanitize(self, param_dict):
        """proceses the handler and returns the cookiejar"""
        if len(param_dict) > 0:
            for k,v in param_dict.items():
                if isinstance(v, bool):
                    param_dict[k] = json.dumps(v)
        return param_dict
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
    def _process_response(self, resp, out_folder=None,  file_name=None):
        """ processes the response object"""
        CHUNK = 4056
        maintype = self._mainType(resp)
        contentDisposition = resp.headers.get('content-disposition')
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
            if file_name is None:
                file_name = os.path.join(out_folder, fname)
            else:
                file_name = os.path.join(out_folder, file_name)
            with open(file_name, 'wb') as writer:
                for data in self._chunk(response=resp):
                    writer.write(data)
                    del data
                del writer
            return file_name
        else:
            read = ""
            if file_name and out_folder:
                f_n_path = os.path.join(out_folder, file_name)
                with open(f_n_path, 'wb') as writer:
                    for data in self._chunk(response=resp, size=4096):
                        if self.PY3 == True:
                            writer.write(data.decode('utf-8'))
                        else:
                            writer.write(data)
                        del data
                    writer.flush()
                return f_n_path
            else:
                for data in self._chunk(response=resp, size=4096):
                    if self.PY3 == True:
                        read += data.decode('utf-8')
                    else:
                        read += data
                    del data
            try:
                return json.loads(read.strip())
            except:
                return read
        return None
    #----------------------------------------------------------------------
    def get(self,
             url,
             param_dict=None,
             securityhandler=None,
             compress=True,
             out_folder=None,
             file_name=None,
             additional_headers=None):
        """
        Performs a GET operation
        """
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        if compress:
            self._headers['Accept-Encoding'] = 'gzip'
        elif compress == False:
            if 'Accept-Encoding' in self._headers:
                self._headers['Accept-Encoding'] = ''
        if isinstance(additional_headers, dict):
            for k,v in additional_headers.items():
                self._headers[k] = v
        if param_dict is None:
            param_dict = {}
        if self._opener is None:
            self._opener = self._create_opener(securityHandler=securityhandler)
        if securityhandler is not None and \
           securityhandler.method == "TOKEN":
            param_dict['token'] = securityhandler.token
        param_dict = self._sanitize(param_dict)
        data = urlencode(param_dict)
        if len(url) + len(data) < 1999:
            url = "{url}?{data}".format(url=url, data=data)
            req = request.Request(url,
                                  headers=self.headers)
        else:
            return self.post(url=url,
                          param_dict=param_dict,
                          securityhandler=securityhandler,
                          files=None,
                          compress=compress,
                          out_folder=out_folder,
                          file_name=file_name)
        response = self._opener.open(req)
        return_value = self._process_response(resp=response,
                                              out_folder=out_folder,
                                              file_name=file_name)
        return return_value
    #----------------------------------------------------------------------
    def post(self,
              url,
              param_dict=None,
              securityhandler=None,
              files=None,
              compress=True,
              out_folder=None,
              file_name=None,
              additional_headers=None):
        """
        Performs a POST operation
        """
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        if compress:
            self._headers['Accept-Encoding'] = 'gzip'
        elif compress == False:
            if 'Accept-Encoding' in self._headers:
                self._headers['Accept-Encoding'] = ''
        if isinstance(additional_headers, dict):
            for k,v in additional_headers.items():
                self._headers[k] = v
        if param_dict is None:
            param_dict = {}
        if files is None:
            files = {}
        if self._opener is None:
            self._opener = self._create_opener(securityHandler=securityhandler)
        if securityhandler is not None and \
           securityhandler.method == "TOKEN":
            param_dict['token'] = securityhandler.token
        param_dict = self._sanitize(param_dict)
        if len(files) > 0:
            mpf = MultiPartForm(param_dict=param_dict,
                                files=files)
            req = request.Request(url,
                                  headers=self._headers)
            body = mpf.make_result
            req.add_header('User-agent', self.useragent)
            req.add_header('Content-type', mpf.get_content_type())
            req.add_header('Content-length', len(body))
            req.data = body
        else:
            data = urlencode(param_dict)
            if self.PY3:
                data = data.encode('ascii')
            req = request.Request(url,
                                  data=data,
                                  headers=self.headers)
        response = self._opener.open(req)
        return_value = self._process_response(resp=response,
                                              out_folder=out_folder,
                                              file_name=file_name)
        return return_value
