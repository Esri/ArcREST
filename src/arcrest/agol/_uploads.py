"""
handles the upload functions for all viable services
"""
from __future__ import absolute_import
import os
import mmap
import json
from ..packages.six.moves import urllib_parse as urlparse
from ..security import security
from .._abstract import abstract
########################################################################
class Uploads(abstract.BaseAGOLClass):
    """
    handles the upload of the files for services
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._securityHandler = securityHandler
        if self._url.lower().endswith("/uploads"):
            self._url = url
        else:
            self._url = url + "/uploads"
    #----------------------------------------------------------------------
    def upload(self, filePath, description=None):
        """
        uploads a file to server and returns an ID. If the item is under
        10MBs, then this function should be used. If it is over 10MBs, then
        you should register the item, and upload by parts.

        Inputs:
         filePath - path to the file to upload
         description - optional description of the file
        output:
         dictionary json response
        """
        url = self._url + "/upload"
        files = {'file', filePath}
        params = {
            "f" : "json"
        }
        if description is not None and \
           isinstance(description, str):
            params['description'] = description

        return self._post(url=url,
                          param_dict=params,
                          files=files,
                          securityHandler=self._securityHandler,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def registerItem(self, itemName, description=None):
        """
        creates an entry for a given item. Once the entry is created, then
        the item can be uploaded by parts.  Once finished, a commit call is
        made to merge the parts together.
        Inputs:
         itemName - name of the item to upload
         description - optional description describing the file.
        Output:
         dictionary
        """
        url = self._url + "/register"
        params = {
            "f" : "json",
            "itemName" : itemName,
            "description" : ""
        }
        if description is not None:
            params['description'] = description
        return self._post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port,
                             securityHandler=self._securityHandler)
    #----------------------------------------------------------------------
    def uploadByParts(self, registerID, filePath, commit=True):
        """
        loads the data by small parts. If commit is set to true,
        then parts will be merged together.  If commit is false, the
        function will return the registerID so a manual commit can occur.

        If the user's file is over 10mbs, the uploadByParts should be used.

        Inputs:
         registerID - ID of the registered item
         filePath - path of the file to upload
         commit - default True, lets the function know if server will piece
          the file back together on the server side.
        Output:
          dictionary or string
        """
        url = self._url + "/%s/uploadPart" % registerID
        params = {
            "f" : "json"
        }
        with open(filePath, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            size = 1000000
            steps =  int(os.fstat(f.fileno()).st_size / size)
            if os.fstat(f.fileno()).st_size % size > 0:
                steps += 1
            for i in range(steps):
                files = {}
                tempFile = os.path.join(os.environ['TEMP'], "split.part%s" % i)
                if os.path.isfile(tempFile):
                    os.remove(tempFile)
                with open(tempFile, 'wb') as writer:
                    writer.write(mm.read(size))
                    writer.flush()
                    writer.close()
                del writer
                files['file'] = tempFile
                params['partNum'] = i + 1
                res = self._post(url=url,
                                  param_dict=params,
                                  files=files,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port)
                os.remove(tempFile)
                del files
            del mm
        return self.commit(registerID)
    #----------------------------------------------------------------------
    def commit(self, registerID, checksum=None):
        """
        Once a multipart upload is completed, the files need to be merged
        together.  The commit() does just that.
        Inputs:
         registerID - unique identifier of the registered item.
         checksum - upload id.
        output:
         dictionary
        """
        parts = ",".join(self.parts(registerID=registerID))
        url = self._url + "/%s/commit"
        params = {
            "f" : "json",
            "parts" : parts
        }
        if checksum is not None:
            params['checksum'] = checksum
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def delete(self, itemId):
        """deletes either a registered item or uploaded item """
        url = self._url + "/%s/delete" % itemId
        params = {
            "f" : "json"
        }
        return self._post(url=url,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port,
                             param_dict=params)
    #----------------------------------------------------------------------
    def parts(self, registerID):
        """returns the parts uploaded for a given item"""
        url = self._url + "/%s/parts" % registerID
        params = {
            "f" : "json"
        }
        return self._get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port,
                            securityHandler=self._securityHandler)
    #----------------------------------------------------------------------
    @property
    def info(self):
        """returns upload file information"""
        url = self._url + "/info"
        params = {
            "f" : "json"
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)



