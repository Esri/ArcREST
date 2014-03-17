import math
import json
import os
import urllib
import urllib2
import httplib
import mimetypes
import Utilities
from Utilities import __unicode_convert as unicode_convert
from Utilities import FeatureServiceError as FeatureClassError
import urlparse

########################################################################
class FeatureService(object):
    """ Instance of an AGOL feature service. Raises Utilities.FeatureServiceError """
    _token = None
    oidFile = None
    _password = None
    _username = None
    _OIDS = None
    _count = None
    _fields = None
    _hasAttachment = None
    _syncEnabled = None
    _spatialReference = None
    _geometryType = None
    _objectIdField = None
    _url = None
    #----------------------------------------------------------------------
    def __init__(self, url, username="", password=""):
        """Constructor"""
        if self._url is None:
            self._url = url
        if self._username is None:
            self._username = username
        if self._password is None:
            self._password = password
        if username != "" and password != "":
            self._token = self.generate_token()
        else:
            self._token = ""
    def _post_multipart(self, host, selector, 
                       filename, filetype, 
                       content, fields):
        """ performs a multi-post to AGOL or AGS 
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               filename - string - name file will be called on server
               filetype - string - mimetype of data uploading
               content - binary data - derived from open(<file>, 'rb').read()
               fields - dictionary - additional parameters like token and format information
            Output:
               JSON response as dictionary
        """
        body = ''
        for field in fields.keys():
            body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="' + field + '"\r\n\r\n' + fields[field] + '\r\n'
        body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="file"; filename="'
        body += filename + '"\r\nContent-Type: ' + filetype + '\r\n\r\n'
        body = body.encode('utf-8')
        body += content + '\r\n------------ThIs_Is_tHe_bouNdaRY_$--\r\n'
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$')
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()
    #----------------------------------------------------------------------
    def generate_token(self):
        """ generates a token for a feature service """
        try:
            token = Utilities.getToken(username=self._username,
                                       password = self._password,
                                       referer='https://www.arcgis.com')[0]
            self._token = token
            return token
        except Utilities.UtilitesError, f_e:
            messages = f_e.args[0]
            line = messages["line"]
            synerror = messages["synerror"]
            filename = messages['filename']
            Utilities.message("An Error has happened in generate tokens", "ERROR")
            Utilities.message("error on line: %s" % line, "ERROR")
            Utilities.message("error in file name: %s" % filename, "ERROR")
            Utilities.message("with error message: %s" % synerror, "ERROR")            
        except: 
            line, filename, synerror = Utilities.trace(__file__)
            raise FeatureClassError({
                    "function": "generate_token",
                    "line": line,
                    "filename": __file__,
                    "synerror": str(synerror)
            })            
    #----------------------------------------------------------------------
    def _getCount(self):
        """ Returns the count of features on a feature service
            Inputs:
               None
            Returns:
               Integer value
        """
        try:

            params = {"f": "json",
                      "where": "1=1",
                      "returnCountOnly":"true",
                      "token": self._token}
            fURL = self._url + "/query?" + urllib.urlencode(params)
            result = urllib.urlopen(fURL).read()
            jobj = json.loads(result)
            return jobj['count']
        except:
            line, filename, synerror = Utilities.trace(__file__)
            raise FeatureClassError({
                    "function": "getCount",
                    "line": line,
                    "filename": __file__,
                    "synerror": synerror
            })
    #----------------------------------------------------------------------
    def _getOIDField(self):
        """ private method that gets the OID field for the feature service """
        params = {"f": "json",
              "where": "1=1",
              "returnIdsOnly":"true",
              "token": self._token}
        fURL = self._url + "/query?" + urllib.urlencode(params)
        result = urllib.urlopen(fURL).read()
        return json.loads(result)
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the feature services' spatial reference """
        if self._spatialReference is None:
            self._getSpatialReference()
        return self._spatialReference
    #----------------------------------------------------------------------
    def _getSpatialReference(self):
        """ sets the feature service spatial reference """
        #"spatialReference"
        fURL = os.path.dirname(self._url)
        params = {"f" : "json",
                  "token" : self._token
                  }
        fsURL = fURL + "?" + urllib.urlencode(params)
        result = urllib.urlopen(fsURL).read()
        json_data = json.loads(result)
        self._spatialReference = unicode_convert(json_data["spatialReference"])

    #----------------------------------------------------------------------
    @property
    def OIDS(self):
        """ returns a collection of OIDs from the feature service"""
        if self._OIDS is None:
            self._OIDS = self._getOIDField()
        return self._OIDS
    #----------------------------------------------------------------------
    @property
    def count(self):
        """ returns the feature count """
        if self._count is None:
            self._count = self._getCount()
        return self._count
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ returns the token """
        return self._token
    #----------------------------------------------------------------------
    def addAttachment(self, oid, file_path):
        """ Adds an attachment to a feature service 
            Input:
              oid - string - OBJECTID value to add attachment to
              file_path - string - path to file
            Output:
              JSON Repsonse
        """
        if self.supportsAttachment == True:
            attachURL = self.url + "/%s/addAttachment" % oid
            obj = {'token': self._token,'f':'json'}
            content = open(file_path, 'rb').read()
            parsed = urlparse.urlparse(attachURL)
            
            res = self._post_multipart(host=parsed.hostname, 
                                       selector=parsed.path, 
                                       filename=os.path.basename(file_path), 
                                       filetype=mimetypes.guess_type(file_path)[0], 
                                       content=content, 
                                       fields=obj)
            return unicode_convert(json.loads(res))
        else:
            return "Attachments are not supported for this feature service."
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header={}):
            """ performs a get operation """
            url = url + "?%s" % urllib.urlencode(param_dict)
            request = urllib2.Request(url, headers=header)
            result = urllib2.urlopen(request).read()
            jres = json.loads(result)
            return unicode_convert(jres)   
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict):
        """ performs the POST operation and returns dictionary result """
        request = urllib2.Request(url, urllib.urlencode(param_dict))
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return unicode_convert(jres)     
    #----------------------------------------------------------------------
    def deleteAttachments(self, oid, attachment_id):
        """ removes an attachment from a feature service feature
            Input:
              oid - integer or string - id of feature
              attachment_id - integer - id of attachment to erase
            Output:
               JSON response
        """
        url = self.url + "/%s/deleteAttachments" % oid
        params = {
            "f":"json",
            "token": self._token,
            "attachmentIds" : "%s" % attachment_id
        }
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def listAttachments(self, oid):
        """ list attachements for a given OBJECT ID """
        url = self.url + "/%s/attachments" % oid
        params = {
            "f":"json",
            "token": self._token
        }
        return self._do_get(url, params)
    #----------------------------------------------------------------------
    def updateAttachment(self, oid, attachment_id, file_path):
        """ updates an existing attachment with a new file 
            Inputs:
               oid - string/integer - Unique record ID
               attachment_id - integer - Unique attachment identifier 
               file_path - string - path to new attachment
            Output:
               JSON response
        """
        url = self.url + "/%s/updateAttachment" % oid
        print url
        params = {
            "f":"json",
            "token": self._token,
            "attachmentId" : "%s" % attachment_id
        }
        parsed = urlparse.urlparse(url)
        content = open(file_path, 'rb').read()
        return self._post_multipart(host=parsed.hostname, 
                                    selector=parsed.path,  
                                    filename=os.path.basename(file_path).split('.')[0], 
                                    filetype=mimetypes.guess_type(file_path)[0], 
                                    content=content, 
                                    fields=params)
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns feature service's fields """
        if self._fields is None:
            self._fields = self._getFields()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ returns the url of the feature service """
        return self._url
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the service's geometry type """
        if self._geometryType is None:
            self._getGeometryType()
        return self._geometryType
    #----------------------------------------------------------------------
    def _getGeometryType(self):
        """ if the value is None for _geometryType, this will set it from the
            serivce
        """
        params = {"f" : "json",
                  "token" : self._token
                  }
        fsURL = self._url + "?" + urllib.urlencode(params)
        result = urllib.urlopen(fsURL).read()
        json_data = unicode_convert(json.loads(result)["geometryType"])
        self._geometryType = json_data
    #----------------------------------------------------------------------
    def _reset(self):
        self._count = None
        self._OIDS = None
        self._fields = None
        self._syncEnabled = None
        self._spatialReference = None
        self._hasAttachment = None
        self._geometryType = None
        self._objectIdField = None
        if self._username != "" and \
           self._password != "":
            self._token = self.generate_token()
        else:
            self._token = ""
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """ sets the URL for the feature service """
        self._reset()
        self._url = value

    #----------------------------------------------------------------------
    @property
    def username(self):
        """ returns the username used for credentials """
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, value):
        """ sets the username"""
        self._username = value
    #----------------------------------------------------------------------
    @property
    def password(self):
        """ property for password, we do not display the password. """
        return "****"
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """ sets the password """
        self._password = value
    #----------------------------------------------------------------------
    @property
    def supportsAttachment(self):
        """ Returns True/False if it supports attachments """
        if self._hasAttachment is None:
            self._checkAttachments()
        return self._hasAttachment
    #----------------------------------------------------------------------
    @property
    def syncEnable(self):
        """ lets the user know if sync is enabled on feature service """
        if self._syncEnabled is None:
            self._checkSyncEnable()
        return self._syncEnabled
    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        """ returns the Object ID field for feature service """
        if self._objectIdField is None:
            self._getObjectIdField()
        return self._objectIdField
    #----------------------------------------------------------------------
    def _getObjectIdField(self):
        """ sets the object id field for the feature service """
        params = {"f" : "json",
                  "token" : self._token
                  }
        fsURL = self._url + "?" + urllib.urlencode(params)
        result = urllib.urlopen(fsURL).read()
        json_data = unicode_convert(json.loads(result)["objectIdField"])
        self._objectIdField = json_data
    #----------------------------------------------------------------------
    def sync_data(self,
                  out_gdb,
                  out_fc,
                  out_attach_table="",
                  returnAttachments=True,
                  attachment_folder=None):
        """ Syncs data back from Feature Service to local datastore 
            Must use FGDB or SDE database
            Inputs:
              out_gdb - string - path to output geodatabase
              out_fc - string - name of output feature class
              out_attach_table - string - (optional) name of attachment table 
              returnAttachments - boolean - True means return them, false means do not return
              attachment_folder - string - storage folder for attachments.
        """
        if self.syncEnable:
            scratchFolder = Utilities.getScratchFolder()
            dl_file = scratchFolder + os.sep + 'replica.json'
            attach = 'false'
            if returnAttachments == True and self.supportsAttachment:
                attach = 'true'
            syncURL = os.path.dirname(self._url) + "/CreateReplica"
            params = {'f' : 'json',
                      'layers' : '0',  # Add variable for layers
                        'returnAttachments' : attach,
                        'token' : self._token }
            syncData = urllib.urlencode(params)
            syncRequest = urllib2.Request(syncURL, syncData)
            syncResponse = urllib2.urlopen(syncRequest)
            syncJson = json.load(syncResponse)
            del syncData
            del syncRequest
            del syncResponse
            replicaJSONFile = syncJson['URL']
            if os.path.isfile(dl_file):
                os.remove(dl_file)
            urllib.urlretrieve(replicaJSONFile, dl_file)
            with open(dl_file, 'rb') as reader:
                jdata = json.load(reader)
                for key, value in jdata.iteritems():
                    if key == 'layers':
                        fields = self.fields
                        wkid = self.spatialReference
                        geomType = self.geometryType
                        attachments = value[int(os.path.basename(self._url))]['attachments']
                        features = value[int(os.path.basename(self._url))]['features']
                        out_fc = Utilities.sync_to_featureclass(out_workspace=out_gdb,
                                                                fc_name=out_fc,
                                                                fields=fields,
                                                                wkid=wkid,
                                                                geomType=geomType,
                                                                features=features,
                                                                objectIdField=self.objectIdField)
                        # process attachements
                        if self.supportsAttachment:
                            rows = []
                            for attach in attachments:
                                if os.path.isdir(attachment_folder) == False:
                                    os.makedirs(attachment_folder)
                                row = [""] * 2
                                row[0] = attach['parentGlobalId']
                                aUrl = attach['url']
                                aName = attach['name']
                                params = { 'token' : self._token }
                                data = urllib.urlencode(params)
                                urllib.urlretrieve(url=aUrl + '/' + aName, filename=os.path.join(attachment_folder, aName), data=data)
                                row[1] = os.path.join(attachment_folder, aName)
                                rows.append(row)
                            Utilities.process_attachements(rows, ["ParentID", "PATH"], out_fc, out_gdb,
                                                           table_name="attachments", working_folder=attachment_folder)
        else:
            print 'sync not enabled'
    #----------------------------------------------------------------------
    def _checkSyncEnable(self):
        """ checks if sync is enabled """
        fsURL = os.path.dirname(self._url)
        params = { "f" : "json",
                   "token": self._token}
        fsURL = fsURL + "?" + urllib.urlencode(params)
        result = urllib.urlopen(fsURL).read()
        self._syncEnabled = json.loads(result)["syncEnabled"]
    #----------------------------------------------------------------------
    def _checkAttachments(self):
        """ checks the service if attachements is enabled """
        #fsURL = os.path.dirname(self._url)
        params = {"f":"json",
                  "token": self._token}
        fURL = self._url + "?" + urllib.urlencode(params)
        result = urllib.urlopen(fURL).read()
        self._hasAttachment = json.loads(result)["hasAttachments"]
    #----------------------------------------------------------------------
    def _getFields(self):
        """ returns the feature class's fields """
        params = {"f": "json",
                "where": "1=1",
                "token": self._token,
                "outFields": "*"}
        fURL = self._url + "?" + urllib.urlencode(params)#/query
        result = urllib.urlopen(fURL).read()
        jobj = unicode_convert(json.loads(result))
        return jobj['fields']
    #----------------------------------------------------------------------
    def addFeatures(self, fc, attachmentTable=None, 
                    nameField="ATT_NAME", blobField="DATA",
                    contentTypeField="CONTENT_TYPE",
                    rel_object_field="REL_OBJECTID"):
        """ adds a feature to the feature service
           Inputs:
              fc - string - path to feature class data to add.
              attachmentTable - string - (optional) path to attachment table 
              nameField - string - (optional) name of file field in attachment table
              blobField - string - (optional) name field containing blob data
              contentTypeField - string - (optional) name of field containing content type
              rel_object_field - string - (optional) name of field with OID of feature class
           Output:
              boolean, add results message as list of dictionaries

        """
        try:
            messages = []
            if attachmentTable is None:
                messages = []
                count = 0
                max_chunk = 1000
                js = Utilities.featureclass_to_json(fc, True)['features']
                fCount = len(js)
                uURL = self._url + "/addFeatures"
                numIt =(float(fCount) / float(max_chunk))
                numIt = int( math.ceil(numIt))
                for i in range (0, numIt):
                    upLim = count + (max_chunk - 1)
                    params = {'token' : self._token,
                              'f' : 'json',
                              'features' : json.dumps(js[count: upLim])}
                    data = urllib.urlencode(params)
                    req = urllib2.Request(uURL, data)
                    response = urllib2.urlopen(req)
                    result = response.read()
                    messages.append(json.loads(result))
                    count += max_chunk
                    del params
                return True, messages
            else:
                oid_field = Utilities.get_OID_field(fc)
                OIDs = Utilities.get_records_with_attachments(attachment_table=attachmentTable)
                fl = Utilities.create_feature_layer(fc, "%s not in ( %s )" % (oid_field, ",".join(OIDs)))
                val, msgs = self.addFeatures(fl)
                messages.append(msgs)
                del fl
                for oid in OIDs:
                    fl = Utilities.create_feature_layer(fc, "%s = %s" % (oid_field, oid), name="layer%s" % oid)
                    val, msgs = self.addFeatures(fl)                    
                    for result in msgs[0]['addResults']:
                        oid_fs = result['objectId']
                        sends = Utilities.get_attachment_data(attachmentTable, sql="%s = %s" % (rel_object_field, oid))
                        for s in sends:
                            messages.append(self.addAttachment(oid_fs, s['blob']))
                            del s
                        del sends
                        del result
                    messages.append(msgs)
                    del fl
                    del oid
                del OIDs
                return True, messages          
        except:
            print Utilities.trace(__file__)
    #----------------------------------------------------------------------
    def deleteFeatures(self, sql):
        """ removes 1:n features based on a sql statement 
            Input:
              sql - string - where clause used to delete features
            Output:
               JSON response
        """
        dURL = self._url + "/deleteFeatures"
        params = {
            "token":self._token,
            "f": "json",
            "where": sql
        }
        req = urllib2.Request(dURL, urllib.urlencode(params))
        response = urllib2.urlopen(req)
        result = response.read()
        js = json.loads(result)
        if "error" in js:
            Utilities.message("Error with delete %s" % js, 'ERROR')
        self._getCount()
        self._getOIDField()
        return "%s features deleted." % len(js['deleteResults'])
    #----------------------------------------------------------------------
    def query(self, sql="1=1", fields="*", returnShapefile=False, out_fc=None):
        """ queries a feature service based on a sql statement
            Inputs:
               service_url - query URL of the feature service
                             URL should be formatted as http(s)://<base_url/query
                             example: http://sampleserver5.arcgisonline.com/arcgis/rest/services/CommercialDamageAssessment/FeatureServer/0/query
               token - string - sercurity token for service
               sql - string - Query statement
               fields - string - comma seperated string of fields names, * returns all
            Output:
               Dictionary
         """
        params = {"f": "json",
                  "where": sql,
                  "outFields":fields,
                  "token": self._token}
        fURL = self._url + "/query?" + urllib.urlencode(params)
        result = "%s" % urllib.urlopen(fURL).read()
        js = unicode_convert(json.loads(result))
        if returnShapefile:
            return Utilities.dictionary_to_feature_class(js, out_fc)
        return js
    def asFeatureClass(self, out_fc):
        """ Returns a local copy of the feature service without attachments
           Input:
              out_fc - string - save location as shapefile of feature class
           Return:
              path to stored data
        """
        json_data = {}
        sql=""
        bins = 0
        fields="*"
        count = self.count
        OIDS = self.OIDS
        if count <= 1000:
            bins = 1
        else:
            bins = count / 1000
            v = count % 1000
            if v > 0:
                bins += 1
        for i in range(0, bins):
            if i+1 > bins:
                break
            sql = "%s >= %s and %s < %s" % (OIDS['objectIdFieldName'],
                                            i * 1000,
                                            OIDS['objectIdFieldName'],
                                            (i+1)* 1000,)
            query_res = self.query(sql=sql)
            for k, v in query_res.iteritems():
                if k == "features":
                    if k not in json_data.keys():
                        json_data[k] = query_res[k]
                    else:
                        json_data[k] += query_res[k]
                if k not in json_data.keys():
                    json_data[k] = query_res[k]
                del k
            del sql
            del i
            del query_res
        return Utilities.dictionary_to_feature_class(json_data, out_fc)
    #----------------------------------------------------------------------


if __name__ == "__main__":
    
    username = "AndrewSolutions"
    password = "fujiFUJI1"
    feature_service = "http://services2.arcgis.com/PWJUSsdoJDp7SgLj/ArcGIS/rest/services/GridIndexFeatures/FeatureServer/0"#"http://services2.arcgis.com/PWJUSsdoJDp7SgLj/ArcGIS/rest/services/Triangle/FeatureServer/0"
    fs = FeatureService(feature_service, username, password)
    print fs.addFeatures(fc=r"c:\temp\AddFeatsTest_Project.shp")
    
    
    #fs = FeatureService(url=feature_service,
                        #username=username,
                        #password=password)
    #fs.addFeatures(fc=r"c:\temp\scratch.gdb\grid", 
                   #attachmentTable=r"c:\temp\scratch.gdb\grid__ATTACH", 
                   #nameField="ATT_NAME", 
                   #blobField="DATA")
    # PASSED - print fs.addAttachment(oid=1, file_path=r"c:\temp\Desert.jpg")
    #attachments = fs.listAttachments(oid=1)
    
    #for a in attachments['attachmentInfos']:
        ## PASSED - print fs.deleteAttachments(1, "%s" % a['id'])
        #print fs.updateAttachment(oid=1, attachment_id=a['id'], 
                                  #file_path=r"c:\temp\Jellyfish.jpg")
        #del a
        #break
    #del attachments
    #print fs.listAttachments(oid=1)
    #content = open(r"c:\temp\jellyfish.jpg", 'rb').read()
    #obj = {'token': fs.generate_token(),'f':'json'}
    #print fs._post_multipart(host='services2.arcgis.com', 
                             #selector='/PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment', 
                             #filename=r"jellyfish.jpg", 
                             #filetype=mimetypes.guess_type(r"c:\temp\jellyfish.jpg")[0], 
                             #content=content, 
                             #fields=obj)
    # PASSED print fs.supportsAttachment
    # PASSED print fs.syncEnable
    # PASSED print fs.geometryType
    # PASSED print fs.spatialReference
    # PASSED print fs.objectIdField
    # PASSED - fs.addFeatures(fc=r"c:\temp\AddFeatsTest.shp")
    # PASSED print fs.count
    # PASSED print fs.OIDS
    # PASSED print fs.fields
    # PASSED print fs.query(sql="FID=1", returnShapefile=True, out_fc= r"c:\temp\fs2.shp")
    # PASSED print fs.asFeatureClass(out_fc=r"c:\temp\alldata.shp")
    # PASSED print fs.deleteFeatures("FID=2")
    # PASSED print fs.password
    # PASSED print fs.url
    # PASSED print fs.token
    # PASSED print fs.username
    # PASSED print fs.sync_data(r"c:\temp\scratch.gdb", "grid", "attachments", attachment_folder=r"c:\temp\arrar")