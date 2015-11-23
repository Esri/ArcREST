from __future__ import absolute_import
from __future__ import print_function
import six
import os
import shutil
from xml.etree import ElementTree as ET

if six.PY2:
    import arcpy
    from arcpy import mapping
    from arcpy import env

    ########################################################################
    def MXDtoFeatureServiceDef( mxd_path,
                                service_name=None,
                                tags=None,
                                description=None,
                                folder_name=None,
                                capabilities ='Query,Create,Update,Delete,Uploads,Editing,Sync',
                                maxRecordCount=1000,
                                server_type='MY_HOSTED_SERVICES',
                                url='http://www.arcgis.com'):
        """
            converts an MXD to a service defenition
            Inputs:
                mxd_path - Path to the ArcMap Map Document(MXD)
                service_name - Name of the Feature Service
                tags - Tags for the service, if none, the tags from the MXD are used
                description - Summary for the Feature Service, if none, info from the MXD is used
                folder_name - Folder in the Data store
                capabilities - A Comma delimited list of feature service capabolities 'Query,Create,Update,Delete,Uploads,Editing,Sync'
                maxRecordCount - The max returned record count for the feature service
                server_type - The type of connection or publishing server
                      Values: ARCGIS_SERVER | FROM_CONNECTION_FILE | SPATIAL_DATA_SERVER | MY_HOSTED_SERVICES
            Output:
                Service Definition File - *.sd

        """
        if not os.path.isabs(mxd_path):
            sciptPath = os.getcwd()
            mxd_path = os.path.join(sciptPath,mxd_path)

        mxd = mapping.MapDocument(mxd_path)
        sddraftFolder = env.scratchFolder + os.sep + "draft"
        sdFolder = env.scratchFolder + os.sep + "sd"
        sddraft = sddraftFolder + os.sep + service_name + ".sddraft"
        sd = sdFolder + os.sep + "%s.sd" % service_name
        mxd = _prep_mxd(mxd)

        res = {}

        if service_name is None:
            service_name = mxd.title.strip().replace(' ','_')
        if tags is None:
            tags = mxd.tags.strip()

        if description is None:
            description = mxd.description.strip()

        if os.path.isdir(sddraftFolder) == False:
            os.makedirs(sddraftFolder)
        else:
            shutil.rmtree(sddraftFolder, ignore_errors=True)
            os.makedirs(sddraftFolder)
        if os.path.isfile(sddraft):
            os.remove(sddraft)

        res['service_name'] = service_name
        res['tags'] = tags
        res['description'] = description
        analysis = mapping.CreateMapSDDraft(map_document=mxd,
                                           out_sddraft=sddraft,
                                           service_name=service_name,
                                           server_type=server_type,
                                           connection_file_path=None,
                                           copy_data_to_server=True,
                                           folder_name=folder_name,
                                           summary=description,
                                           tags=tags)

        sddraft = _modify_sddraft(sddraft=sddraft,
                                  capabilities=capabilities,
                                  maxRecordCount=maxRecordCount,
                                  url=url)
        analysis = mapping.AnalyzeForSD(sddraft)
        if os.path.isdir(sdFolder):
            shutil.rmtree(sdFolder, ignore_errors=True)
            os.makedirs(sdFolder)
        else:
            os.makedirs(sdFolder)
        if analysis['errors'] == {}:
            # Stage the service
            arcpy.StageService_server(sddraft, sd)
            res['servicedef'] = sd
            return res
        else:
            # If the sddraft analysis contained errors, display them and quit.
            print (analysis['errors'])
            return None



    def _modify_sddraft(sddraft,
                        capabilities,
                        maxRecordCount='1000',
                        url='http://www.arcgis.com'):
        """ modifies the sddraft for agol publishing
        """

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
                prop.find("Value").text = maxRecordCount

        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Extensions/SVCExtension"):
            if prop.find("TypeName").text == 'KmlServer':
                prop.find("Enabled").text = "false"

        # Turn on feature access capabilities
        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Info/PropertyArray/PropertySetProperty"):
            if prop.find("Key").text == 'WebCapabilities':
                prop.find("Value").text = capabilities

        # Update url for portal
        for prop in doc.findall("./StagingSettings/PropertyArray/PropertySetProperty"):
            if prop.find("Key").text == 'ServerConnectionString':
                prop.find("Value").text = prop.find("Value").text.toString().replace('www.arcgis.com',url)
        # Update url for portal
        for prop in doc.findall("./itemInfo/url"):
            prop.text = prop.text.toString().replace('www.arcgis.com',url)
        # Add the namespaces which get stripped, back into the .SD
        root_elem.attrib["xmlns:typens"] = 'http://www.esri.com/schemas/ArcGIS/10.2'
        root_elem.attrib["xmlns:xs"] = 'http://www.w3.org/2001/XMLSchema'
        newSDdraft = os.path.dirname(sddraft) + os.sep + "draft_mod.sddraft"
        # Write the new draft to disk
        with open(newSDdraft, 'w') as f:
            doc.write(f, 'utf-8')
        del doc
        return newSDdraft

    #----------------------------------------------------------------------
    def _prep_mxd(mxd):
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