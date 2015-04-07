from _abstract import abstract

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest
from arcrest.agol import FeatureLayer
from arcrest.agol import FeatureService
from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
import common 
import gc
import arcpy
#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror


class publishingtools(abstract.baseToolsClass):

    #----------------------------------------------------------------------
    def publishMap(self,maps_info,fsInfo=None):
        itemInfo = None
        itemID = None
        map_results = None
        replaceInfo = None
        replaceItem = None
        map_info = None
        admin = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            map_results = []
            for map_info in maps_info:
                itemInfo = {}

                if map_info.has_key('ReplaceInfo'):
                    replaceInfo = map_info['ReplaceInfo']
                else:
                    replaceInfo = None


                if replaceInfo != None:

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Layer':

                            if fsInfo is not None:

                                for fs in fsInfo:
                                    if fs is not None and replaceItem['ReplaceString'] == fs['ReplaceTag']:
                                        replaceItem['ReplaceString'] = fs['FSInfo']['serviceurl']
                                        replaceItem['ItemID'] = fs['FSInfo']['serviceItemId']
                                        replaceItem['ItemFolder'] = fs['FSInfo']['folderId']
                                    elif replaceItem.has_key('ItemID'):
                                        if replaceItem.has_key('ItemFolder') == False:

                                            itemID = replaceItem['ItemID']
                                            itemInfo = admin.content.item(itemId=itemID)
                                            if 'owner' in itemInfo:
                                                if itemInfo['owner'] == self._securityHandler.username and 'ownerFolder' in itemInfo:
                                                    replaceItem['ItemFolder'] = itemInfo['ownerFolder']
                                                else:
                                                    replaceItem['ItemFolder'] = None


                if map_info.has_key('ReplaceTag'):

                    itemInfo = {"ReplaceTag":map_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{WebMap}" }

                itemInfo['MapInfo']  = self._publishMap(config=map_info,
                                                   replaceInfo=replaceInfo)
                map_results.append(itemInfo)
                if not itemInfo is None:
                    if not 'error' in itemInfo['MapInfo']['Results']:
                        print "%s webmap created" % itemInfo['MapInfo']['Name']
                    else:
                        print str(itemInfo['MapInfo']['Results'])
                else:
                    print "Map not created"
            return map_results
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            itemInfo = None
            itemID = None
            replaceInfo = None
            replaceItem = None
            map_info = None
            admin = None

            del itemInfo
            del itemID
            del replaceInfo
            del replaceItem
            del map_info
            del admin

            gc.collect()
    #----------------------------------------------------------------------
    def _publishMap(self,config,replaceInfo=None,operationalLayers=None,tableLayers=None):
        name = None
        tags = None
        description = None
        extent = None
        webmap_data = None
        itemJson = None
        update_service = None
        admin = None
        adminusercontent = None
        resultMap = None
        json_data = None
        replaceItem = None
        opLayers = None
        opLayer = None
        layers = None
        item = None
        response = None
        layerIdx = None
        updatedLayer = None
        updated = None
        text = None
        itemParams = None
        updateResults = None
        loc_df = None
        datestring = None
        snippet = None
        everyone = None
        org = None
        groupNames = None
        folderName = None
        thumbnail = None
        itemType = None
        typeKeywords = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemID = None
        group_ids = None
        shareResults = None
        updateParams = None
        try:
            name = ''
            tags = ''
            description = ''
            extent = ''
            webmap_data = ''

            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:
                return {"Results":{"error": "%s does not exist" % itemJson}  }

            update_service = config['UpdateService']
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            adminusercontent = admin.content.usercontent()
            resultMap = {'Layers':[],'Tables':[],'Results':None}

            with open(itemJson) as json_data:
                try:
                    webmap_data = json.load(json_data)
                except:
                    raise ValueError("%s is not a valid JSON File" % itemJson)
                if operationalLayers:
                    webmap_data['operationalLayers'] = operationalLayers
                if tableLayers:
                    webmap_data['tables'] = tableLayers
                if replaceInfo:
                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Global':
                            webmap_data = common.find_replace(webmap_data,replaceItem['SearchString'],replaceItem['ReplaceString'])
                        elif replaceItem['ReplaceType'] == 'Layer':
                            if webmap_data.has_key('tables'):
                                opLayers = webmap_data['tables']
                                for opLayer in opLayers:
                                    if replaceItem['SearchString'] in opLayer['url']:

                                        opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                        if replaceItem.has_key('ItemID'):
                                            opLayer['itemId'] = replaceItem['ItemID']
                                        else:
                                            opLayer['itemId'] = None
                                            #opLayer['itemId'] = get_guid()

                                        if str(update_service).upper() == "TRUE" and opLayer['itemId'] != None:
                                            layers = []
                                            item = admin.content.item(itemId = replaceItem['ItemID'])
                                            response = item.itemData()
                                            if 'layers' in response:
                                                layers = response['layers']

                                            str(opLayer['url'] ).split("/")

                                            layerIdx = common.getLayerIndex(url=opLayer['url'])
                                            if opLayer.has_key("popupInfo"):
                                                updatedLayer = {"id" : layerIdx ,
                                                                "popupInfo" : opLayer["popupInfo"]
                                                                }
                                            else:
                                                updatedLayer = None

                                            updated = False
                                            for layer in layers:
                                                if str(layer['id']) == str(layerIdx):
                                                    layer = updatedLayer
                                                    updated = True
                                            if updated == False and not updatedLayer is None:
                                                layers.append(updatedLayer)
                                            if len(layers):
                                                text = {
                                                    "layers" :layers
                                                }

                                                itemParams = arcrest.manageorg.ItemParameter()
                                                itemParams.type = "Feature Service"


                                                updateResults = adminusercontent.updateItem(itemId = replaceItem['ItemID'],
                                                                            updateItemParameters=itemParams,
                                                                            folderId=replaceItem['ItemFolder'],
                                                                            text=json.dumps(text))
                                                if 'error' in updateResults:
                                                    print updateResults

                        opLayers = webmap_data['operationalLayers']
                        for opLayer in opLayers:
                            if replaceItem['SearchString'] in opLayer['url']:

                                opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                if replaceItem.has_key('ItemID'):
                                        opLayer['itemId'] = replaceItem['ItemID']
                                else:
                                    opLayer['itemId'] = None
                                    #opLayer['itemId'] = get_guid()

                                if str(update_service).upper() == "TRUE" and opLayer['itemId'] != None:
                                    layers = []
                                    item = admin.content.item(itemId = replaceItem['ItemID'])
                                    response = item.itemData()
                                    if 'layers' in response:
                                        layers = response['layers']

                                    str(opLayer['url'] ).split("/")
                                    layerIdx = common.getLayerIndex(url=opLayer['url'])
                                    if opLayer.has_key("popupInfo"):
                                        updatedLayer = {"id" : layerIdx,
                                                        "popupInfo" : opLayer["popupInfo"]
                                                        }
                                    else:
                                        updatedLayer = None

                                    updated = False
                                    for layer in layers:
                                        if str(layer['id']) == str(layerIdx):
                                            layer = updatedLayer
                                            updated = True
                                    if updated == False and not updatedLayer is None:
                                        layers.append(updatedLayer)
                                    if len(layers):
                                        text = {
                                            "layers" :layers
                                        }

                                        itemParams = arcrest.manageorg.ItemParameter()
                                        itemParams.type = "Feature Service"


                                        updateResults = adminusercontent.updateItem(itemId = replaceItem['ItemID'],
                                                                    updateItemParameters=itemParams,
                                                                    folderId=replaceItem['ItemFolder'],
                                                                    text=json.dumps(text))
                                        if 'error' in updateResults:
                                            print updateResults

                opLayers = webmap_data['operationalLayers']
                for opLayer in opLayers:
                    opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))
                    resultMap['Layers'].append({"Name":opLayer['title'],"ID":opLayer['id']})


                if webmap_data.has_key('tables'):

                    opLayers = webmap_data['tables']
                    for opLayer in opLayers:
                        opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))
                        resultMap['Tables'].append({"Name":opLayer['title'],"ID":opLayer['id']})


            name = config['Title']

            if config.has_key('DateTimeFormat'):
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']

            extent = config['Extent']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            if webmap_data is None:
                return None

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = "Web Map"
            itemParams.overwrite = True
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.extent = extent
            itemParams.tags = tags
            itemParams.typeKeywords = ",".join(typeKeywords)

            adminusercontent = admin.content.usercontent()
            userCommunity = admin.community
            userContent = admin.content.getUserContent()

            folderId = admin.content.getFolderID(name=folderName,userContent=userContent)
            if folderId is None:
                res = adminusercontent.createFolder(name=folderName)
                if 'success' in res:
                    folderId = res['folder']['id']
                else:
                    pass

            folderContent = admin.content.getUserContent(folderId=folderId)

            itemID = admin.content.getItemID(title=name,itemType='Web Map',userContent=folderContent)

            if not itemID is None:
                resultMap['Results'] = adminusercontent.updateItem(itemId=itemID,
                                            updateItemParameters=itemParams,
                                            folderId=folderId,
                                            text=json.dumps(webmap_data))

            else:

                resultMap['Results'] = adminusercontent.addItem( itemParameters=itemParams,
                        overwrite=True,
                        folder=folderId,
                        url=None,
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None,
                        text=json.dumps(webmap_data))


            if not 'error' in resultMap['Results']:

                group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                shareResults = adminusercontent.shareItems(items=resultMap['Results']['id'],
                                       groups=','.join(group_ids),
                                       everyone=everyone,
                                       org=org)
                updateParams = arcrest.manageorg.ItemParameter()
                updateParams.title = name
                updateResults = adminusercontent.updateItem(itemId=resultMap['Results']['id'],
                                                            updateItemParameters=updateParams,
                                                            folderId=folderId)
                resultMap['folderId'] = folderId
                resultMap['Name'] = name
            return resultMap

        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            name = None
            tags = None
            description = None
            extent = None
            webmap_data = None
            itemJson = None
            update_service = None
            admin = None
            adminusercontent = None
            resultMap = None
            json_data = None
            replaceItem = None
            opLayers = None
            opLayer = None
            layers = None
            item = None
            response = None
            layerIdx = None
            updatedLayer = None
            updated = None
            text = None
            itemParams = None
            updateResults = None
            loc_df = None
            datestring = None
            snippet = None
            everyone = None
            org = None
            groupNames = None
            folderName = None
            thumbnail = None
            itemType = None
            typeKeywords = None
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemID = None
            group_ids = None
            shareResults = None
            updateParams = None

            del name
            del tags
            del description
            del extent
            del webmap_data
            del itemJson
            del update_service
            del admin
            del adminusercontent
            del resultMap
            del json_data
            del replaceItem
            del opLayers
            del opLayer
            del layers
            del item
            del response
            del layerIdx
            del updatedLayer
            del updated
            del text
            del itemParams
            del updateResults
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del thumbnail
            del itemType
            del typeKeywords
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemID
            del group_ids
            del shareResults
            del updateParams

            gc.collect()

    #----------------------------------------------------------------------
    def publishCombinedWebMap(self,maps_info,webmaps):
        admin = None
        map_results = None
        map_info = None
        operationalLayers = None
        tableLayers = None
        item = None
        response = None
        opLays = None
        operationalLayers = None
        tblLays = None
        tblLayer = None
        itemInfo = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            map_results = []
            for map_info in maps_info:

                operationalLayers = []
                tableLayers = []
                for webmap in webmaps:
                    item = admin.content.item(itemId=webmap)
                    response = item.itemData()
                    if 'operationalLayers' in response:

                        opLays = []
                        for opLayer in response['operationalLayers']:
                            opLays.append(opLayer)
                        opLays.extend(operationalLayers)
                        operationalLayers = opLays
                    if 'tables' in response:

                        tblLays = []
                        for tblLayer in response['tables']:
                            tblLays.append(tblLayer)
                        tblLays.extend(tableLayers)
                        tableLayers = tblLays

                if map_info.has_key('ReplaceTag'):

                    itemInfo = {"ReplaceTag":map_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{WebMap}" }

                itemInfo['MapInfo'] = self._publishMap(config=map_info,
                                                                       replaceInfo=None,
                                                                       operationalLayers=operationalLayers,
                                                                       tableLayers=tableLayers)


                map_results.append(itemInfo)
                if not itemInfo is None:
                    if not 'error' in itemInfo['MapInfo']['Results']:
                        print "            %s webmap created" % itemInfo['MapInfo']['Name']
                    else:
                        print "            " + str(itemInfo['MapInfo']['Results'])
                else:
                    print "            Map not created"

                return map_results
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishedCombinedWebMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishedCombinedWebMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            admin = None

            map_info = None

            tableLayers = None
            item = None
            response = None
            opLays = None
            operationalLayers = None
            tblLays = None
            tblLayer = None
            itemInfo = None

            del admin
            del map_info

            del tableLayers
            del item
            del response
            del opLays
            del operationalLayers
            del tblLays
            del tblLayer
            del itemInfo

            gc.collect()
    #----------------------------------------------------------------------
    def publishFsFromMXD(self,fs_config):
        """
            publishs a feature service from a mxd
            Inputs:
                feature_service_config: Json file with list of feature service publishing details
            Output:
                feature service item information

        """
        fs = None
        res = None
        try:
            res = []
            if isinstance(fs_config, list):
                for fs in fs_config:
                    if fs.has_key('ReplaceTag'):

                        resItm = {"ReplaceTag":fs['ReplaceTag'] }
                    else:
                        resItm = {"ReplaceTag":"{FeatureService}" }

                    resItm['FSInfo'] = self._publishFSfromConfig(config=fs)
                    
                    if 'serviceurl' in resItm['FSInfo']:
                        print "%s created" % resItm['FSInfo']['serviceurl']
                        res.append(resItm)
                    else:
                        print str(resFS)
                
            else:
                if fs_config.has_key('ReplaceTag'):

                    resItm = {"ReplaceTag":fs_config['ReplaceTag'] }
                else:
                    resItm = {"ReplaceTag":"{FeatureService}" }

                resItm['FSInfo'] = self._publishFSfromConfig(config=fs_config)
              
                if 'serviceurl' in resItm['FSInfo']:
                    print "%s created" % resItm['FSInfo']['serviceurl']
                    res.append(resItm)
                else:
                    print str(resFS)              
       
            return res
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishFsFromMXD",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishFsFromMXD",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            resFS = None
            fs = None

            del resFS
            del fs

            gc.collect()
    #----------------------------------------------------------------------
    def _publishFSfromConfig(self,config):
        mxd = None
        q = None
        everyone = None
        org = None
        groupNames = None

        folderName = None
        thumbnail = None
        capabilities = None
        maxRecordCount = None
        loc_df = None
        datestring = None
        service_name = None
        service_name_safe = None
        sd_Info = None
        admin = None
        itemParams = None
        adminusercontent = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemID = None
        resultSD = None
        publishParameters = None
        resultFS = None
        delres = None
        status = None
        group_ids = None
        shareResults = None
        updateParams = None
        enableEditTracking = None
        adminFS = None
        json_dict = None
        enableResults = None
        layer = None
        layers = None
        layUpdateResult = None
        definition = None
        try:
            # Report settings
            mxd = config['Mxd']

            # Service settings
            service_name = config['Title']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated
            if config.has_key('EnableEditTracking'):
                enableEditTracking = config['EnableEditTracking']
            else:
                print "Please add an EnableEditTracking parameter to your feature service section"
                enableEditTracking = False
            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            if 'Capabilities' in config:
                capabilities = config['Capabilities']
            if 'Definition' in config:
                definition = config['Definition']

                if 'capabilities' in definition:
                    capabilities = definition['capabilities']
            if config.has_key("maxRecordCount"):
                maxRecordCount =  config["maxRecordCount"]
            else:
                maxRecordCount =1000

            if config.has_key('DateTimeFormat'):
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat


            datestring = datetime.datetime.now().strftime(loc_df)
            service_name = service_name.replace('{DATE}',datestring)
            service_name = service_name.replace('{Date}',datestring)

            service_name_safe = service_name.replace(' ','_')
            service_name_safe = service_name_safe.replace(':','-')

            if os.path.exists(path=mxd) == False:
                raise ValueError("MXD does not exit")

            sd_Info = arcrest.common.servicedef.MXDtoFeatureServiceDef(mxd_path=mxd,
                                                                 service_name=service_name_safe,
                                                                 tags=None,
                                                                 description=None,
                                                                 folder_name=None,
                                                                 capabilities=capabilities,
                                                                 maxRecordCount=maxRecordCount,
                                                                 server_type='MY_HOSTED_SERVICES')

            if sd_Info is None:
                return

            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)


            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = service_name
            itemParams.thumbnail = thumbnail
            itemParams.type = "Service Definition"
            itemParams.overwrite = True

            adminusercontent = admin.content.usercontent()
            userCommunity = admin.community
            userContent = admin.content.getUserContent()

            folderId = admin.content.getFolderID(name=folderName,userContent=userContent)
            if folderId is None:
                res = adminusercontent.createFolder(name=folderName)
                if 'success' in res:
                    folderId = res['folder']['id']
                else:
                    pass

            #q = "title:\""+ service_name + "\"AND owner:\"" + self._securityHandler.username + "\" AND type:\"" + "Service Definition" + "\""

            #items = admin.query(q=q, bbox=None, start=1, num=10, sortField=None,
                       #sortOrder="asc")

            #if items['total'] >= 1:
                #pass
            folderContent = admin.content.getUserContent(folderId=folderId)

            itemID = admin.content.getItemID(title=service_name,itemType='Service Definition',userContent=folderContent)
            if not itemID is None:
                resultSD = adminusercontent.updateItem(itemId=itemID,
                                            updateItemParameters=itemParams,
                                            folderId=folderId,
                                            filePath=sd_Info['servicedef'])

            else:

                resultSD = adminusercontent.addItem( itemParameters=itemParams,
                        filePath=sd_Info['servicedef'],
                        overwrite=True,
                        folder=folderId,
                        url=None,
                        text=None,
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None)


            if not 'error' in resultSD:
                publishParameters = arcrest.manageorg.PublishSDParmaeters(tags=sd_Info['tags'],overwrite='true')
                #itemID = admin.content.getItemID(title=service_name,itemType='Feature Service',userContent=folderContent)
                #if not itemID is None:
                    #delres=adminusercontent.deleteItems(items=itemID)

                resultFS = adminusercontent.publishItem(
                    fileType="serviceDefinition",
                    itemId=resultSD['id'],
                    publishParameters=publishParameters)

                if 'services' in resultFS:
                    if len(resultFS['services']) > 0:

                        if 'error' in resultFS['services'][0]:
                            print "            Overwrite failed, attempting to delete, then recreate"

                            q = "title:\""+ service_name + "\"AND owner:\"" + self._securityHandler.username + "\" AND type:\"" + "Feature Service" + "\""
                            items = admin.query(q=q, bbox=None, start=1, num=10, sortField=None,
                                       sortOrder="asc")
                            if items['total'] >= 1:
                                itemID = items['results'][0]['id']

                            else:
                                q = "title:\""+ service_name_safe + "\"AND owner:\"" + self._securityHandler.username + "\" AND type:\"" + "Feature Service" + "\""
                                items = admin.query(q=q, bbox=None, start=1, num=10, sortField=None,
                                                                      sortOrder="asc")
                                if items['total'] >= 1:
                                    itemID = items['results'][0]['id']
                                #itemID = admin.content.getItemID(title=service_name,itemType='Feature Service',userContent=folderContent)
                                #if  itemID is None:
                                    #itemID = admin.content.getItemID(title=service_name_safe,itemType='Feature Service',userContent=folderContent)

                            if not itemID is None:
                                delres=adminusercontent.deleteItems(items=itemID)
                                if 'error' in delres:
                                    print delres
                                    return delres
                                print "            Delete successful"
                            else:
                                print "            Item cannot be found"

                            resultFS = adminusercontent.publishItem(
                                           fileType="serviceDefinition",
                                           itemId=resultSD['id'],
                                           publishParameters=publishParameters)

                        if 'error' in resultFS:
                            return resultFS
                        #if 'services' in resultFS:
                            #if resultFS['services']['success']     == 'false':
                                #return
                        status = adminusercontent.status(itemId=resultFS['services'][0]['serviceItemId'],
                                                         jobId=resultFS['services'][0]['jobId'],
                                                         jobType='publish')
                        if 'error' in status:
                            print  "            %s" % status
                        elif 'status' in status:
                            while status['status'] == 'processing' or status['status'] == 'partial':
                                time.sleep(.5)
                                status = adminusercontent.status(itemId=resultFS['services'][0]['serviceItemId'],
                                                                                     jobId=resultFS['services'][0]['jobId'],
                                                                                             jobType='publish')
                                if 'error' in status:
                                    print status
                            if status['status'] == 'failed':
                                print "            Overwrite failed, attempting to delete, then recreate"

                                delres=adminusercontent.deleteItems(items=resultFS['services'][0]['serviceItemId'])
                                if 'error' in delres:
                                    print delres
                                    return delres
                                print "            Delete successful"

                                resultFS = adminusercontent.publishItem(
                                                fileType="serviceDefinition",
                                                itemId=resultSD['id'],
                                                publishParameters=publishParameters)
                                if 'error' in resultFS:
                                    return resultFS
                                status = adminusercontent.status(itemId=resultFS['services'][0]['serviceItemId'],
                                                                                     jobId=resultFS['services'][0]['jobId'],
                                                                                     jobType='publish')
                                if 'error' in status:
                                    print status
                                    return status
                                while status['status'] == 'processing' or status['status'] == 'partial':
                                    time.sleep(.5)
                                    status = adminusercontent.status(itemId=resultFS['services'][0]['serviceItemId'],
                                                                                         jobId=resultFS['services'][0]['jobId'],
                                                                                                 jobType='publish')
                                    if 'error' in status:
                                        print status
                                        return status
                            if status['status'] == 'completed':

                                group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                                shareResults = adminusercontent.shareItems(items=resultFS['services'][0]['serviceItemId'],
                                                       groups=','.join(group_ids),
                                                       everyone=everyone,
                                                       org=org)
                                updateParams = arcrest.manageorg.ItemParameter()
                                updateParams.title = service_name
                                updateResults = adminusercontent.updateItem(itemId=resultFS['services'][0]['serviceItemId'],
                                                                            updateItemParameters=updateParams,
                                                                            folderId=folderId)
                                adminFS = AdminFeatureService(url=resultFS['services'][0]['serviceurl'], securityHandler=self._securityHandler)

                                if enableEditTracking == True or str(enableEditTracking).upper() == 'TRUE':

                                    json_dict = {'editorTrackingInfo':{}}
                                    json_dict['editorTrackingInfo']['allowOthersToDelete'] = True
                                    json_dict['editorTrackingInfo']['allowOthersToUpdate'] = True
                                    json_dict['editorTrackingInfo']['enableEditorTracking'] = True
                                    json_dict['editorTrackingInfo']['enableOwnershipAccessControl'] = False

                                    enableResults = adminFS.updateDefinition(json_dict=json_dict)
                                    if 'error' in enableResults:
                                        resultFS['services'][0]['messages'] = enableResults

                                    json_dict = {'editFieldsInfo':{}}

                                    json_dict['editFieldsInfo']['creationDateField'] = ""
                                    json_dict['editFieldsInfo']['creatorField'] = ""
                                    json_dict['editFieldsInfo']['editDateField'] = ""
                                    json_dict['editFieldsInfo']['editorField'] = ""
                                    layers = adminFS.layers
                                    for layer in layers:
                                        layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                                        if 'error' in layUpdateResult:
                                            resultFS['services'][0]['messages'] = resultFS['services'][0]['messages'] + "|" + layUpdateResult['error']


                                if definition is not None:
                                    enableResults = adminFS.updateDefinition(json_dict=definition)
                                    if 'error' in enableResults:
                                        resultFS['services'][0]['messages'] = enableResults

                                resultFS['services'][0]['folderId'] = folderId
                                return resultFS['services'][0]

                        else:
                            return status
                    else:
                        return resultFS
                else:
                    return resultFS
            else:
                return resultSD
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishFsFromConfig",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishFsFromConfig",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            definition = None
            mxd = None
            q = None
            everyone = None
            org = None
            groupNames = None

            folderName = None
            thumbnail = None
            capabilities = None
            maxRecordCount = None
            loc_df = None
            datestring = None
            service_name = None
            service_name_safe = None
            sd_Info = None
            admin = None
            itemParams = None
            adminusercontent = None
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemID = None
            resultSD = None
            publishParameters = None
            resultFS = None
            delres = None
            status = None
            group_ids = None
            shareResults = None
            updateParams = None
            enableEditTracking = None
            adminFS = None
            json_dict = None
            enableResults = None
            layer = None
            layers = None
            layUpdateResult = None

            del definition
            del layer
            del layers
            del layUpdateResult
            del mxd

            del q
            del everyone
            del org
            del groupNames

            del folderName
            del thumbnail
            del capabilities
            del maxRecordCount
            del loc_df
            del datestring
            del service_name
            del service_name_safe
            del sd_Info
            del admin
            del itemParams
            del adminusercontent
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemID
            del resultSD
            del publishParameters
            del resultFS
            del delres
            del status
            del group_ids
            del shareResults
            del updateParams
            del enableEditTracking
            del adminFS
            del json_dict
            del enableResults
            gc.collect()
    #----------------------------------------------------------------------
    def _publishAppLogic(self,appDet,map_info=None):
        itemInfo = None
        replaceInfo = None
        replaceItem = None
        mapDet = None
        lay = None
        itemId = None
        admin = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            itemInfo = {}

            if appDet.has_key('ReplaceInfo'):
                replaceInfo = appDet['ReplaceInfo']
            else:
                replaceInfo = None

            if replaceInfo != None:

                for replaceItem in replaceInfo:

                    for mapDet in map_info:
                        if mapDet.has_key('ReplaceTag'):
                            if mapDet is not None and replaceItem['ReplaceString'] == mapDet['ReplaceTag'] and replaceItem['ReplaceType'] == 'Map':

                                replaceItem['ItemID'] = mapDet['MapInfo']['Results']['id']
                                replaceItem['ItemFolder'] = mapDet['MapInfo']['folderId']
                            elif mapDet is not None and replaceItem['ReplaceType'] == 'Layer':
                                repInfo = replaceItem['ReplaceString'].split("|")
                                if len(repInfo) == 2:
                                    if repInfo[0] == mapDet['ReplaceTag']:
                                        for lay in  mapDet['MapInfo']['Layers']:
                                            if lay["Name"] == repInfo[1]:
                                                replaceItem['ReplaceString'] = lay["ID"]

                            elif replaceItem.has_key('ItemID'):
                                if replaceItem.has_key('ItemFolder') == False:

                                    itemId = replaceItem['ItemID']
                                    itemInfo = admin.content.item(itemId=itemId)
                                    if 'owner' in itemInfo:
                                        if itemInfo['owner'] == self._securityHandler.username and 'ownerFolder' in itemInfo:
                                            replaceItem['ItemFolder'] = itemInfo['ownerFolder']
                                        else:
                                            replaceItem['ItemFolder'] = None


            if appDet.has_key('ReplaceTag'):

                itemInfo = {"ReplaceTag":appDet['ReplaceTag'] }
            else:
                itemInfo = {"ReplaceTag":"{App}" }

            if appDet['Type'] == 'Web Mapping Application':
                itemInfo['AppInfo']  = self._publishApp(config=appDet,
                                                               replaceInfo=replaceInfo)
            elif appDet['Type'] == 'Operation View':
                itemInfo['AppInfo']  = self._publishDashboard(config=appDet,
                                                               replaceInfo=replaceInfo)
            else:
                itemInfo['AppInfo']  = self._publishApp(config=appDet,
                                               replaceInfo=replaceInfo)

            if not itemInfo['AppInfo']  is None:
                if not 'error' in itemInfo['AppInfo']['Results'] :
                    print "            %s app created" % itemInfo['AppInfo']['Name']
                else:
                    print "            " + str(itemInfo['AppInfo']['Results'])
            else:
                print "            " + "App was not created"
            return itemInfo
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishAppLogic",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishAppLogic",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            replaceInfo = None
            replaceItem = None
            mapDet = None
            lay = None
            itemId = None
            admin = None

            del admin
            del replaceInfo
            del replaceItem
            del mapDet
            del lay
            del itemId
            gc.collect()
    #----------------------------------------------------------------------
    def publishApp(self,app_info,map_info=None):
        appDet = None
        try:
            app_results = []
            if isinstance(app_info, list):
                for appDet in app_info:
                    app_results.append(self._publishAppLogic(appDet=appDet,map_info=map_info))
            else:
                app_results.append(self._publishAppLogic(appDet=app_info,map_info=map_info))
            return app_results
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            appDet = None

            del appDet
            gc.collect()
    #----------------------------------------------------------------------
    def _publishApp(self, config, replaceInfo):
        resultApp = None
        name = None
        tags = None
        description = None
        extent = None
        itemJson = None
        admin = None
        adminusercontent = None
        json_data = None
        itemData = None
        replaceItem = None
        loc_df = None
        datestring = None
        snippet = None
        everyone = None
        org = None
        groupNames = None
        folderName = None
        url = None
        thumbnail = None
        itemType = None
        typeKeywords  = None
        itemParams = None
        userCommunity = None
        userContent = None
        res = None
        folderId = None
        folderContent = None
        itemID = None
        group_ids = None
        shareResults = None
        updateParams = None
        url = None
        updateResults = None
        portal = None
        try:
            resultApp = {'Results':None}
            name = ''
            tags = ''
            description = ''
            extent = ''

            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:

                return {"Results":{"error": "%s does not exist" % itemJson}  }
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            adminusercontent = admin.content.usercontent()
            if os.path.exists(itemJson):
                with open(itemJson) as json_data:
                    try:
                        itemData = json.load(json_data)
                    except:
                        raise ValueError("%s is not a valid JSON File" % itemJson)

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Map' and 'ItemID' in replaceItem:
                            if 'values' in itemData:
                                if 'webmap' in itemData['values']:
                                    if itemData['values']['webmap'] == replaceItem['SearchString']:
                                        itemData['values']['webmap'] = replaceItem['ItemID']
                                        if 'folderId' in itemData:
                                            itemData['folderId'] = replaceItem['ItemFolder']
                        elif replaceItem['ReplaceType'] == 'Layer' and 'ReplaceString' in replaceItem:
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])

                        elif replaceItem['ReplaceType'] == 'Global':
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])

            else:
                print "%s does not exist." %itemJson
                itemData = None

            name = config['Title']

            if config.has_key('DateTimeFormat'):
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']


            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            url = config['Url']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = itemType

            itemParams.overwrite = True
            itemParams.description = description
            itemParams.tags = tags
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.typeKeywords = ",".join(typeKeywords)

            adminusercontent = admin.content.usercontent()
            userCommunity = admin.community
            userContent = admin.content.getUserContent()

            folderId = admin.content.getFolderID(name=folderName,userContent=userContent)
            if folderId is None:
                res = adminusercontent.createFolder(name=folderName)
                if 'success' in res:
                    folderId = res['folder']['id']
                else:
                    pass

            folderContent = admin.content.getUserContent(folderId=folderId)
            if 'folderId' in itemData:
                itemData['folderId'] = folderId

            itemID = admin.content.getItemID(title=name,itemType=itemType,userContent=folderContent)
            if not itemID is None:
                resultApp['Results'] = adminusercontent.updateItem(itemId=itemID,
                                            updateItemParameters=itemParams,
                                            folderId=folderId,
                                            text=json.dumps(itemData))

            else:

                resultApp['Results']  = adminusercontent.addItem( itemParameters=itemParams,
                        folder=folderId,
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None,
                        text=json.dumps(itemData))


            if not 'error' in resultApp['Results']:

                group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                shareResults = adminusercontent.shareItems(items=resultApp['Results']['id'],
                                       groups=','.join(group_ids),
                                       everyone=everyone,
                                       org=org)
                updateParams = arcrest.manageorg.ItemParameter()
                updateParams.title = name
                portal = admin.portals()
                url = url.replace("{AppID}",resultApp['Results']['id'])
                portalProp = portal.portalProperties
                url = url.replace("{OrgURL}", portalProp['urlKey'] + '.' + portalProp['customBaseUrl'])

                updateResults = adminusercontent.updateItem(itemId=resultApp['Results']['id'],
                                                            url=url,
                                                            updateItemParameters=updateParams,
                                                            folderId=folderId)
                resultApp['folderId'] = folderId
                resultApp['Name'] = name
            return resultApp

        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:

            name = None
            tags = None
            description = None
            extent = None
            itemJson = None
            admin = None
            adminusercontent = None
            json_data = None
            itemData = None
            replaceItem = None
            loc_df = None
            datestring = None
            snippet = None
            everyone = None
            org = None
            groupNames = None
            folderName = None
            url = None
            thumbnail = None
            itemType = None
            typeKeywords  = None

            itemParams = None
            userCommunity = None
            userContent = None
            res = None
            folderId = None
            folderContent = None
            itemID = None
            group_ids = None
            shareResults = None
            updateParams = None
            url = None
            updateResults = None
            portal = None

            del name
            del portal
            del tags
            del description
            del extent
            del itemJson
            del admin
            del adminusercontent
            del json_data
            del itemData
            del replaceItem
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del url
            del thumbnail
            del itemType
            del typeKeywords
            del itemParams
            del userCommunity
            del userContent
            del res
            del folderId
            del folderContent
            del itemID
            del group_ids
            del shareResults
            del updateParams

            del updateResults

            gc.collect()
    #----------------------------------------------------------------------
    def _publishDashboard(self,config, replaceInfo):
        resultApp = None
        tags = None
        description = None
        extent = None
        itemJson = None
        layerIDSwitch = None
        admin = None
        adminusercontent = None
        json_data = None
        itemData = None
        replaceItem = None
        item = None
        response = None
        layerNamesID = None
        layerIDs = None
        tableNamesID = None
        tableIDs = None
        opLayer = None
        widget = None
        widgets = None
        mapTool = None
        dataSource = None
        configFileAsString = None
        repl = None
        name = None
        loc_df = None
        datestring = None
        snippet = None
        everyone  = None
        org  = None
        groupNames = None
        folderName = None
        thumbnail = None
        itemType = None
        typeKeywords = None
        itemParams = None
        adminusercontent = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemID = None
        group_ids = None
        shareResults = None
        updateParams = None
        resultApp = None
        updateResults = None
        try:
            resultApp = {'Results':None}

            tags = ''
            description = ''
            extent = ''


            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:
                print "            Error: %s does not exist" % itemJson
                return None
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            adminusercontent = admin.content.usercontent()

            layerIDSwitch = []

            if os.path.exists(itemJson):
                with open(itemJson) as json_data:
                    try:
                        itemData = json.load(json_data)
                    except:
                        raise ValueError("%s is not a valid JSON File" % itemJson)

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Global':
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])
                        elif replaceItem['ReplaceType'] == 'Map' and 'ItemID' in replaceItem:
                            item = admin.content.item(itemId=replaceItem['ItemID'])
                            response = item.itemData()

                            layerNamesID = {}
                            layerIDs =[]

                            tableNamesID = {}
                            tableIDs =[]

                            if 'operationalLayers' in response:
                                for opLayer in response['operationalLayers']:
                                    layerNamesID[opLayer['title']] = opLayer['id']
                                    layerIDs.append(opLayer['id'])
                            if 'tables' in response:
                                for opLayer in response['tables']:
                                    tableNamesID[opLayer['title']] = opLayer['id']
                                    tableIDs.append(opLayer['id'])

                            widgets = itemData['widgets']
                            for widget in widgets:

                                if widget.has_key('mapId'):
                                    if replaceItem['SearchString'] == widget['mapId']:
                                        widget['mapId'] = replaceItem['ItemID']
                                        if widget.has_key('mapTools'):
                                            for mapTool in widget['mapTools']:
                                                if mapTool.has_key('layerIds'):
                                                    mapTool['layerIds'] = layerIDs
                                        if widget.has_key('dataSources'):
                                            for dataSource in widget['dataSources']:
                                                if dataSource.has_key('layerId'):
                                                    if layerNamesID.has_key(dataSource['name']):
                                                        layerIDSwitch.append({"OrigID":dataSource['layerId'],"NewID":layerNamesID[dataSource['name']] })
                                                        dataSource['layerId'] = layerNamesID[dataSource['name']]



            configFileAsString = json.dumps(itemData)
            for repl in layerIDSwitch:
                configFileAsString.replace(repl['OrigID'],repl['NewID'])

            itemData = json.loads(configFileAsString)


            name = config['Title']

            if config.has_key('DateTimeFormat'):
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']


            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = itemType

            itemParams.overwrite = True
            itemParams.description = description
            itemParams.snippet = snippet
            itemParams.typeKeywords = ",".join(typeKeywords)

            adminusercontent = admin.content.usercontent()
            userCommunity = admin.community
            userContent = admin.content.getUserContent()

            folderId = admin.content.getFolderID(name=folderName,userContent=userContent)
            if folderId is None:
                res = adminusercontent.createFolder(name=folderName)
                if 'success' in res:
                    folderId = res['folder']['id']
                else:
                    pass

            folderContent = admin.content.getUserContent(folderId=folderId)

            itemID = admin.content.getItemID(title=name,itemType=itemType,userContent=folderContent)
            if not itemID is None:
                resultApp['Results'] = adminusercontent.updateItem(itemId=itemID,
                                            updateItemParameters=itemParams,
                                            folderId=folderId,
                                            text=json.dumps(itemData))

            else:

                resultApp['Results'] = adminusercontent.addItem( itemParameters=itemParams,
                        folder=folderId,
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None,
                        text=json.dumps(itemData))


            if not 'error' in resultApp['Results']:

                group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                shareResults = adminusercontent.shareItems(items=resultApp['Results']['id'],
                                       groups=','.join(group_ids),
                                       everyone=everyone,
                                       org=org)
                updateParams = arcrest.manageorg.ItemParameter()
                updateParams.title = name
                updateResults = adminusercontent.updateItem(itemId=resultApp['Results']['id'],
                                                            updateItemParameters=updateParams,
                                                            folderId=folderId)
                resultApp['folderId'] = folderId
                resultApp['Name'] = name
            return resultApp
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishDashboard",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "_publishDashboard",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:

            tags = None
            description = None
            extent = None
            itemJson = None
            layerIDSwitch = None
            admin = None
            adminusercontent = None
            json_data = None
            itemData = None
            replaceItem = None
            item = None
            response = None
            layerNamesID = None
            layerIDs = None
            tableNamesID = None
            tableIDs = None
            opLayer = None
            widget = None
            widgets = None
            mapTool = None
            dataSource = None
            configFileAsString = None
            repl = None
            name = None
            loc_df = None
            datestring = None
            snippet = None
            everyone  = None
            org  = None
            groupNames = None
            folderName = None
            thumbnail = None
            itemType = None
            typeKeywords = None
            itemParams = None
            adminusercontent = None
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemID = None
            group_ids = None
            shareResults = None
            updateParams = None

            updateResults = None


            del tags
            del description
            del extent
            del itemJson
            del layerIDSwitch
            del admin

            del json_data
            del itemData
            del replaceItem
            del item
            del response
            del layerNamesID
            del layerIDs
            del tableNamesID
            del tableIDs
            del opLayer
            del widget
            del widgets
            del mapTool
            del dataSource
            del configFileAsString
            del repl
            del name
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del thumbnail
            del itemType
            del typeKeywords
            del itemParams
            del adminusercontent
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemID
            del group_ids
            del shareResults
            del updateParams

            del updateResults
            gc.collect()
    #----------------------------------------------------------------------
    def updateFeatureService(self,efs_config):

        fsRes = None
        fst = None
        fURL = None
        resItm= None
        try:

            fsRes = []
            fst = featureservicetools(securityHandler=self._securityHandler)


            if isinstance(efs_config, list):
                for ext_service in efs_config:
                    resItm={"DeleteDetails": None,"AddDetails":None}
                    fURL = ext_service['URL']

                    if 'DeleteInfo' in ext_service:
                        if str(ext_service['DeleteInfo']['Delete']).upper() == "TRUE":
                            resItm['DeleteDetails'] = fst.DeleteFeaturesFromFeatureLayer(url=fURL, sql=ext_service['DeleteInfo']['DeleteSQL'])
                            if not 'error' in resItm['DeleteDetails'] :
                                print "            Delete Successful: %s" % fURL
                            else:
                                print "            " + str(resItm['DeleteDetails'])

                    resItm['AddDetails'] = fst.AddFeaturesToFeatureLayer(url=fURL, pathToFeatureClass = ext_service['FeatureClass'])

                    fsRes.append(resItm)

                    if not 'error' in resItm['AddDetails']:
                        print "            Add Successful: %s " % fURL
                    else:
                        print "            " + str(resItm['AddDetails'])

            else:
                resItm={"DeleteDetails": None,"AddDetails":None}
                fURL = efs_config['URL']

                if 'DeleteInfo' in efs_config:
                    if str(efs_config['DeleteInfo']['Delete']).upper() == "TRUE":
                        resItm['DeleteDetails'] = fst.DeleteFeaturesFromFeatureLayer(url=fURL, sql=efs_config['DeleteInfo']['DeleteSQL'])
                        if not 'error' in resItm['DeleteDetails'] :
                            print "            Delete Successful: %s" % fURL
                        else:
                            print "            " + str(resItm['DeleteDetails'])

                resItm['AddDetails'] = fst.AddFeaturesToFeatureLayer(url=fURL, pathToFeatureClass = efs_config['FeatureClass'])

                fsRes.append(resItm)

                if not 'error' in resItm['AddDetails']:
                    print "            Add Successful: %s " % fURL
                else:
                    print "            " + str(resItm['AddDetails'])

            return fsRes
        except arcpy.ExecuteError:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "updateFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                                        }
                                        )
        except:
            line, filename, synerror = trace()
            raise ArcRestHelperError({
                        "function": "updateFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )
        finally:
            fst = None
            fURL = None
            resItm= None

            del fst
            del fURL
            del resItm

            gc.collect()
