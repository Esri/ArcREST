import httplib
import os
import sys
import shutil
from xml.etree import ElementTree as ET
import arcpy
from arcpy import mapping
from arcpy import env
from base import BaseAGOLClass
class AGOL(BaseAGOLClass):
    """ publishes to AGOL """
    _username = None
    _password = None
    _token = None
    base_url = "http://www.arcgis.com/sharing/rest"
    def __init__(self, username, password):
        """ constructor """
        self._username = username
        self._password = password
        self._token = self.generate_token()
    #----------------------------------------------------------------------
    @property
    def contentRootURL(self):
        """ returns the Portal's content root """
        return self.base_url + "/content"
    #----------------------------------------------------------------------
    def addComment(self, item_id, comment):
        """ adds a comment to a given item.  Must be authenticated """
        url = self.contentRootURL + "/items/%s/addComment" % item_id
        params = {
            "f" : "json",
            "comment" : comment,
            "token" : self._token
        }
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def addRating(self, item_id, rating=5.0):
        """Adds a rating to an item between 1.0 and 5.0"""
        if rating > 5.0:
            rating = 5.0
        elif rating < 1.0:
            rating = 1.0
        url = self.contentRootURL + "/items/%s/addRating" % item_id
        params = {
            "f": "json",
            "token" : self._token,
            "rating" : "%s" % rating
        }
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def createFolder(self, folder_name):
        """ creats a folder for a user's agol account """
        url = self.contentRootURL + "/users/%s/createFolder" % self._username
        params = {
            "f" : "json",
            "token" : self._token,
            "title" : folder_name
        }
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def deleteFolder(self, item_id):
        """ deletes a user's folder """
        url = self.contentRootURL + "/users/%s/%s/delete" % (self._username, item_id)
        params = {
            "f" : "json",
            "token" : self._token
        }
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def item(self, item_id):
        """ returns information about an item on agol/portal """
        params = {
            "f" : "json",
            "token" : self._token
        }
        url = self.contentRootURL + "/items/%s" % item_id
        return self._do_get(url, params)
    #----------------------------------------------------------------------
    def _prep_mxd(self, mxd):
        """ ensures the requires mxd properties are set to something """
        changed = False
        if mxd.author.strip() == "":
            mxd.author = "NA"
            changed = True
        if mxd.credits.strip() == "":
            mxd.credits = "NA"
            changed = True
        if mxd.description.strip() == "":
            mxd.description = "NA"
            changed = True
        if mxd.summary.strip() == "":
            mxd.summary = "NA"
            changed = True
        if mxd.tags.strip() == "":
            mxd.tags = "NA"
            changed = True
        if mxd.title.strip() == "":
            mxd.title = "NA"
            changed = True
        if changed == True:
            mxd.save()
        return mxd
    #----------------------------------------------------------------------
    def getUserContent(self):
        """ gets a user's content on agol """
        data = {"token": self._token,
                "f": "json"}
        url = "http://www.arcgis.com/sharing/content/users/%s" % (self._username,)
        jres = self._do_get(url=url, param_dict=data, header={"Accept-Encoding":""})
        return jres
    #----------------------------------------------------------------------
    def addFile(self, file_path, agol_type, name, tags, description):
        """ loads a file to AGOL """
        params = {
                    "f" : "json",
                    "filename" : os.path.basename(file_path),
                    "type" : agol_type,
                    "title" : name,
                    "tags" : tags,
                    "description" : description
                }
        url = "{}/content/users/{}/addItem".format(self.base_url,
                                                   self._username)
        return self._do_post_file(url=url,
                                  params=params,
                                  file_path=file_path)
    #----------------------------------------------------------------------
    def deleteItem(self, item_id):
        """ deletes an agol item by it's ID """
        deleteURL = '{}/content/users/{}/items/{}/delete'.format(self.base_url, self._username, item_id)
        query_dict = {'f': 'json',
                      'token': self._token}
        jres = self._do_post(deleteURL, query_dict)
        return jres
    #----------------------------------------------------------------------
    def _modify_sddraft(self, sddraft):
        """ modifies the sddraft for agol publishing """

        doc = ET.parse(sddraft)

        root_elem = doc.getroot()
        if root_elem.tag != "SVCManifest":
            raise ValueError("Root tag is incorrect. Is {} a .sddraft file?".format(sddraft))

        # The following 6 code pieces modify the SDDraft from a new MapService
        # with caching capabilities to a FeatureService with Query,Create,
        # Update,Delete,Uploads,Editing capabilities as well as the ability to set the max
        # records on the service.
        # The first two lines (commented out) are no longer necessary as the FS
        # is now being deleted and re-published, not truly overwritten as is the
        # case when publishing from Desktop.
        # The last three pieces change Map to Feature Service, disable caching
        # and set appropriate capabilities. You can customize the capabilities by
        # removing items.
        # Note you cannot disable Query from a Feature Service.

        # Change service type from map service to feature service
        for desc in doc.findall('Type'):
            if desc.text == "esriServiceDefinitionType_New":
                desc.text = 'esriServiceDefinitionType_Replacement'

        for config in doc.findall("./Configurations/SVCConfiguration/TypeName"):
            if config.text == "MapServer":
                config.text = "FeatureServer"

        #Turn off caching
        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/" +
                                    "ConfigurationProperties/PropertyArray/" +
                                    "PropertySetProperty"):
            if prop.find("Key").text == 'isCached':
                prop.find("Value").text = "false"
            if prop.find("Key").text == 'maxRecordCount':
                prop.find("Value").text = "1000"

        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Extensions/SVCExtension"):
            if prop.find("TypeName").text == 'KmlServer':
                prop.find("Enabled").text = "false"

        # Turn on feature access capabilities
        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Info/PropertyArray/PropertySetProperty"):
            if prop.find("Key").text == 'WebCapabilities':
                prop.find("Value").text = "Query,Create,Update,Delete,Uploads,Editing"

        # Add the namespaces which get stripped, back into the .SD
        root_elem.attrib["xmlns:typens"] = 'http://www.esri.com/schemas/ArcGIS/10.1'
        root_elem.attrib["xmlns:xs"] = 'http://www.w3.org/2001/XMLSchema'
        newSDdraft = os.path.dirname(sddraft) + os.sep + "draft_mod.sddraft"
        # Write the new draft to disk
        with open(newSDdraft, 'w') as f:
            doc.write(f, 'utf-8')
        del doc
        return newSDdraft
    #----------------------------------------------------------------------
    def _upload_sd_file(self, sd, service_name, tags="None", description="None"):
        """ uploads the sd file to agol """
        url = "{}/content/users/{}/addItem".format(self.base_url,
                                                   self._username)
        params = {
            "f" : "json",
            "token" : self._token,
            "filename" : os.path.basename(sd),
            "type" : "Service Definition",
            "title" : service_name,
            "tags" : tags,
            "description" : description
        }
        vals = self._do_post_file(url, params, file_path=sd)
        if "success" in vals:
            return vals['id']
        else:
            return "Error Uploadings"
    #----------------------------------------------------------------------
    def enableSharing(self, agol_id, everyone='true', orgs='true', groups='None'):
        """ changes and items sharing permissions """
        share_url = '{}/content/users/{}/items/{}/share'.format(self.base_url,
                                                               self._username,
                                                               agol_id)
        if groups == None:
            groups = ''
        query_dict = {'f': 'json',
                      'everyone' : everyone,
                      'org' : orgs,
                      'groups' : groups,
                      'token': self._token}
        vals = self._do_post(share_url, query_dict)
        return vals
    #----------------------------------------------------------------------
    def publish_to_agol(self, mxd_path, service_name, tags="None", description="None"):
        """ publishes a service to AGOL """
        mxd = mapping.MapDocument(mxd_path)
        sddraftFolder = env.scratchFolder + os.sep + "draft"
        sdFolder = env.scratchFolder + os.sep + "sd"
        sddraft = sddraftFolder + os.sep + service_name + ".sddraft"
        sd = sdFolder + os.sep + "%s.sd" % service_name
        mxd = self._prep_mxd(mxd)
        if os.path.isdir(sddraftFolder) == False:
            os.makedirs(sddraftFolder)
        else:
            shutil.rmtree(sddraftFolder, ignore_errors=True)
            os.makedirs(sddraftFolder)
        if os.path.isfile(sddraft):
            os.remove(sddraft)
        analysis = mapping.CreateMapSDDraft(mxd, sddraft,
                                            service_name,
                                            "MY_HOSTED_SERVICES")
        sddraft = self._modify_sddraft(sddraft)
        analysis = mapping.AnalyzeForSD(sddraft)
        if os.path.isdir(sdFolder):
            shutil.rmtree(sdFolder, ignore_errors=True)
            os.makedirs(sdFolder)
        else:
            os.makedirs(sdFolder)
        if analysis['errors'] == {}:
            # Stage the service
            arcpy.StageService_server(sddraft, sd)
            print "Created {}".format(sd)

        else:
            # If the sddraft analysis contained errors, display them and quit.
            print analysis['errors']
            sys.exit()
        # POST data to site
        content = self.getUserContent()
        #Title, item
        for item in content['items']:
            if item['title'] == service_name and \
               item['item'] == os.path.basename(sd):
                print self.deleteItem(item['id'])
            elif item['title'] == service_name:
                print self.deleteItem(item['id'])

        self._agol_id = self._upload_sd_file(sd, service_name=service_name,
                                             tags=tags, description=description)

        if self._agol_id != "Error Uploadings":
            p_vals = self._publish(self._agol_id)
            for service in p_vals['services']:
                print self.enableSharing(service['serviceItemId'])
                del service
            del p_vals
        del mxd
    #----------------------------------------------------------------------
    def _publish(self, agol_id):
        """"""
        publishURL = '{}/content/users/{}/publish'.format(self.base_url,
                                                          self._username)
        query_dict = {'itemID': agol_id,
                     'filetype': 'serviceDefinition',
                     'f': 'json',
                     'token': self._token}
        return self._do_post(publishURL, query_dict)

# This function is a workaround to deal with what's typically described as a
# problem with the web server closing a connection. This is problem
# experienced with www.arcgis.com (first encountered 12/13/2012). The problem
# and workaround is described here:
# http://bobrochel.blogspot.com/2010/11/bad-servers-chunked-encoding-and.html
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

#if __name__ == "__main__":
    #p = AGOL(username="", password="")
    #mxd_path = r"c:\temp\test.mxd"
    ## PASSED - print p.getUserContent()
    ## PASSED - print p.password
    ## PASSED - print p.username
    ## PASSED - print p.generate_token()
    ## PASSED - print p.createFolder("TESTFOLDER")
    ## PASSED - print p.deleteFolder("52a45e7c1f7c4c678b7012b27c771714")
    ## PASSED - p.publish_to_agol(mxd_path,"Triangle")
    #print 'fin'
