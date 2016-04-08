"""
Controls the Uploads of file to AGS/AGO
"""
from __future__ import absolute_import
from ..common.packages.six.moves.urllib_parse import urlparse, urlencode
from ._base import BaseService
import os
########################################################################
class Uploads(BaseService):
    """
    The uploads resource is the parent resource for upload related
    operations and resources. This resource is available only if the
    service or an extension supports the uploads capability. For Feature
    and Image Services, upload capability is enabled when editing is turned
    on. For Mobile and GP Services, upload capability can be explicitly
    enabled or disabled at publish time. For a Geodata Service, uploads is
    enabled when replication is turned on. If uploads is enabled for a
    service, it is recommended that the service be secured to allow only
    authenticated users access to this capability.
    """
    _url = None
    _con = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self, connection, url, initialize=False):
        self._url = url
        self._con = connection
    #----------------------------------------------------------------------
    @property
    def info(self):
        """
        The info resource returns the maxUploadFileSize property of a
        service.
        """
        url = self._url + "/info"
        params = {
            "f" : "json"
        }
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    def upload(self, filePath, description=None):
        """
        This operation uploads an item to the server. Each uploaded item is
        identified by a unique itemID. Since this request uploads a file,
        it must be a multi-part request as per IETF RFC1867.
        All uploaded items are subjected to the deletion rules set on the
        upload directory by the administrator of the server. Additionally,
        the administrator can explicitly delete an item as each uploaded
        item shows up in the list of all the uploaded items in Site
        Directory.
        Users can provide arguments to the upload operation as query
        parameters. The parameter details are provided in the parameters
        listed below.
        Inputs:
           filePath - The file to be uploaded.
           description	- An optional description for the uploaded item.
        """
        params = {
            "f" : "json"}
        if description is not None:
            params['description'] = str(description)
        url = self._url + "/upload"
        files = {}
        files['file'] = filePath
        return self._con.post(path_or_url=url,
                          postdata=params,
                          files=files)
    #----------------------------------------------------------------------
    def delete(self, itemID):
        """
        This operation deletes an item.

        Inputs:
           itemID - unique ID of item
        """
        url = self._url + "/%s/delete" % itemID
        params = {
            "f" : "json"
        }
        return self._con.post(path_or_url=url, postdata=params)
    #----------------------------------------------------------------------
    def download(self, itemID, savePath):
        """
        downloads an item to local disk

        Inputs:
           itemID - unique id of item to download
           savePath - folder to save the file in
        """
        if os.path.isdir(savePath) == False:
            os.makedirs(savePath)
        url = self._url + "/%s/download" % itemID
        params = {
        }
        if len(params.keys()):
            url =  url + "?%s" % urlencode(params)
        return self._con.get(path_or_url=url,
                         params=params,
                         out_folder=savePath)
    #----------------------------------------------------------------------
    @property
    def uploads(self):
        """
        returns all uploaded items for this service.
        """
        url = self._url
        params = {
            "f" : "json",

        }
        return self._con.get(path_or_url=url, params=params)