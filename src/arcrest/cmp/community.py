from __future__ import print_function
from __future__ import absolute_import
import json
from six.moves.urllib_parse import quote
from ..agol import FeatureService
from .._abstract.abstract import BaseCMP
from ..security.security import AGOLTokenSecurityHandler, CommunityMapsSecurityHandler
########################################################################
class CommunityMapsProgram(BaseCMP):
    """contains operations to manage community mapping program content"""
    _metadataURL = "http://communitymaps.arcgis.com/arcgis/rest/services/PublicCommunityMaps/PublicContributorMetadata/MapServer"
    _metaFS = None
    _user = None
    _url = None
    _root = None
    _securityHandler = None
    _agolSH = None
    _proxy_url = None
    _proxy_port = None
    _referer_url = None
    _username = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler, #NOTE: if agol security do X elif cmp security handler do Y, else raise
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._root = url
        if isinstance(securityHandler, AGOLTokenSecurityHandler):
            # get the agol username, get the CM handler, get referer
            self._username = securityHandler._username
            self._referer_url = securityHandler._referer_url
            self._agolSH = securityHandler
            self._securityHandler = CommunityMapsSecurityHandler(url=self._root,
                                            username=securityHandler._username,
                                            password=securityHandler._password,
                                            proxy_url=securityHandler._proxy_url,
                                            proxy_port=securityHandler._proxy_port)
        elif isinstance(securityHandler, CommunityMapsSecurityHandler):
            self._username = securityHandler._username
            self._referer_url = securityHandler._referer_url
            self._securityHandler = securityHandler
            self._agolSH = securityHandler._agolSecurityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self._user = self.user
    #----------------------------------------------------------------------
    @property
    def root(self):
        """"""
        return self._root
    #----------------------------------------------------------------------
    @property
    def contributorUID(self):
        """ gets the contributor UID"""
        return self.user.ContributorUID
    #----------------------------------------------------------------------
    @property
    def contributionStatus(self):
        """gets the contribution status of a user"""
        import time
        url = "%s/contributors/%s/activeContribution" % (self.root, quote(self.contributorUID))
        params = {
            "agolUserToken" : self._agolSH.token,
            "f" : "json"
        }
        res = self._get(url=url,
                         param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
        if'Status' in res and \
          res['Status'] == 'start':
            return True
        return False
    #----------------------------------------------------------------------
    def refresh(self):
        """resets the user class"""
        self._user = None
    #----------------------------------------------------------------------
    @property
    def user(self):
        """gets the user properties"""
        if self._user is None:
            url = "%s/users/%s" % (self.root, self._username)
            self._user = CMPUser(url=url,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url,
                                 initialize=False)
        return self._user
    #----------------------------------------------------------------------
    @property
    def metadataURL(self):
        """gets/sets the public metadata url"""
        return self._metadataURL
    #----------------------------------------------------------------------
    @metadataURL.setter
    def metadataURL(self, value):
        """gets/sets the public metadata url"""
        if value != self._metadataURL:
            self._metadataURL = value
            self._metaFS = None
    #----------------------------------------------------------------------
    @property
    def metadataContributer(self):
        """gets the metadata featurelayer object"""
        if self._metaFL is None:
            fl = FeatureService(url=self._metadataURL,
                              proxy_url=self._proxy_url,
                              proxy_port=self._proxy_port)
            self._metaFS = fl
        return self._metaFS
    #----------------------------------------------------------------------
    def addItem(self, filePath):
        """"""
        from six.moves.urllib_parse import urlparse
        #from six.moves.url_parse import urlparse
        #http://sea-web-bm-s01.dmz.esri.com/communitymaps-services-2/rest/sharing/content/users/CommunityMapsTeam
        #http://sea-web-bm-s01.dmz.esri.com/sharing/content/users/CommunityMapsTeam
        url = "%s/sharing/content/users/CommunityMapsTeam" % self.root
        files = {'file' : filePath}
        params = {
            "f" : "json"
        }
        return self._post(url=url,
                          param_dict=params,
                          files=files,
                          securityHandler=self._securityHandler)



########################################################################
class CMPUser(BaseCMP):
    """represents the user information for a given community maps program"""
    _user = None
    _url = None
    _root = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    _json_dict = None
    _PhoneNumber1 = None
    _AgolUsername = None
    _GlobalID = None
    _OBJECTID = None
    _JobTitle = None
    _ContributorUID = None
    _FullName = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._root = url
        self._seucurityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns the root url"""
        return self._root

    #----------------------------------------------------------------------
    def __str__(self):
        """returns raw JSON response as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns properties (key/values) from the JSON response"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def PhoneNumber1(self):
        """gets the PhoneNumber1 property"""
        if self._PhoneNumber1 is None:
            self.__init()
        return self._PhoneNumber1

    #----------------------------------------------------------------------
    @property
    def AgolUsername(self):
        """gets the AgolUsername property"""
        if self._AgolUsername is None:
            self.__init()
        return self._AgolUsername

    #----------------------------------------------------------------------
    @property
    def GlobalID(self):
        """gets the GlobalID property"""
        if self._GlobalID is None:
            self.__init()
        return self._GlobalID
    #----------------------------------------------------------------------
    @property
    def OBJECTID(self):
        """gets the OBJECTID property"""
        if self._OBJECTID is None:
            self.__init()
        return self._OBJECTID
    #----------------------------------------------------------------------
    @property
    def JobTitle(self):
        """gets the JobTitle property"""
        if self._JobTitle is None:
            self.__init()
        return self._JobTitle
    #----------------------------------------------------------------------
    @property
    def ContributorUID(self):
        """gets the ContributorUID property"""
        if self._ContributorUID is None:
            self.__init()
        return self._ContributorUID
    #----------------------------------------------------------------------
    @property
    def FullName(self):
        """gets the FullName property"""
        if self._FullName is None:
            self.__init()
        return self._FullName
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        #http://sea-web-bm-s01.dmz.esri.com/communitymaps-services-2/rest/user/CMP2Demo?f=json
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in CMPUser class.")







