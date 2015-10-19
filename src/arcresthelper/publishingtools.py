
from securityhandlerhelper import securityhandlerhelper
import re as re

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest

import arcresthelper.featureservicetools as featureservicetools 

from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
import arcresthelper.common as common
import gc
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False

from urlparse import urlparse

try:
    import pyparsing
    pyparsingInstall = True
    from arcresthelper import select_parser
except:
    pyparsingInstall = False

import inspect
    
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno
#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect, sys 
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror


class publishingtools(securityhandlerhelper):
    def getItemID(self,userContent,title=None, name=None, itemType=None):
        """
           This function retrieves the item ID if the item exist

           Inputs:
              name - the name of the item
            userContent - a list of user contnet
           Output:
              string - ID of item, none if item does not exist
        """
        itemID = None
        if name == None and title == None:
            raise AttributeError('Name or Title needs to be specified')
        for item in userContent:
            if title is None and not name is None:
                if item.name == name and (itemType is None or item.type == itemType):
                    return item.id
                
            elif not title is None and name is None:
                if item.title == title and (itemType is None or item.type == itemType):
                    return item.id
                  
            else:
                if item.name == name and item.title == title and (itemType is None or item.type == itemType):
                    return item.id
        return None          
    def getItem(self,userContent,title=None, name=None, itemType=None):
        """
           This function retrieves the item ID if the item exist

           Inputs:
              name - the name of the item
            userContent - a list of user contnet
           Output:
              string - ID of item, none if item does not exist
        """
        itemID = None
        if name == None and title == None:
            raise AttributeError('Name or Title needs to be specified')
        for item in userContent:
            if title is None and not name is None:
                if item.name == name and (itemType is None or item.type == itemType):
                    return item

            elif not title is None and name is None:
                if item.title == title and (itemType is None or item.type == itemType):
                    return item

            else:
                if item.name == name and item.title == title and (itemType is None or item.type == itemType):
                    return item
        return None              
    #----------------------------------------------------------------------
    def folderExist(self, name, folders):
        """
           Determines if a folder exist

           Inputs:
             name - the name of the folder
             folders - list of folders
           Output:
              boolean - true/false if the folder exist
        """
        if not name == None and not name == '':
         
            folderID = None
          
            for folder in folders:
                if folder['title'].lower() == name.lower():
                    return True;
                   
            del folders

            return folderID

        else:
            return False

    #----------------------------------------------------------------------
    def publishMap(self,maps_info,fsInfo=None):
        itemInfo = None
        itemId = None
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
                                        replaceItem['ReplaceString'] = fs['FSInfo']['url']
                                        replaceItem['ItemID'] = fs['FSInfo']['itemId']
                                        replaceItem['ItemFolder'] = fs['FSInfo']['folderId']
                                        if 'convertCase' in fs['FSInfo']:
                                            replaceItem['convertCase'] = fs['FSInfo']['convertCase']
                                    elif replaceItem.has_key('ItemID'):
                                        if replaceItem.has_key('ItemFolder') == False:

                                            itemId = replaceItem['ItemID']
                                            itemInfo = admin.content.getItem(itemId=itemId)
                                            if itemInfo.owner:
                                                if itemInfo.owner == self._securityHandler.username and itemInfo.ownerFolder:
                                                    replaceItem['ItemFolder'] = itemInfo.ownerFolder
                                                else:
                                                    replaceItem['ItemFolder'] = None


                if map_info.has_key('ReplaceTag'):

                    itemInfo = {"ReplaceTag":map_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{WebMap}" }

                itemInfo['MapInfo']  = self._publishMap(config=map_info,
                                                   replaceInfo=replaceInfo)
                map_results.append(itemInfo)
                print "%s webmap created" % itemInfo['MapInfo']['Name']
            return map_results 
       
        except common.ArcRestHelperError,e:
            raise e
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "publishMap",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
        finally:
            itemInfo = None
            itemId = None
            replaceInfo = None
            replaceItem = None
            map_info = None
            admin = None

            del itemInfo
            del itemId
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
        itemId = None
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
            update_service = 'FALSE'
            
            resultMap = {'Layers':[],'Tables':[],'Results':{}}

            with open(itemJson) as json_data:
                layersInfo= {}
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
                                    layerInfo= {}
                                    if replaceItem['SearchString'] in opLayer['url']:

                                        opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                        if replaceItem.has_key('ItemID'):
                                            opLayer['itemId'] = replaceItem['ItemID']
                                        else:
                                            opLayer['itemId'] = None
                                            #opLayer['itemId'] = get_guid()
                                        if replaceItem.has_key('convertCase'):
                                            if replaceItem['convertCase'] == 'lower':
                                                layerInfo = {}
                                               
                                                layerInfo['convertCase'] = replaceItem['convertCase']
                                                layerInfo['fields'] = []
                                                if opLayer.has_key("layerDefinition"):
                                            
                                                    if opLayer["layerDefinition"].has_key('drawingInfo'):
                                                        if opLayer["layerDefinition"]['drawingInfo'].has_key('renderer'):
                                                            if 'field1' in opLayer["layerDefinition"]['drawingInfo']['renderer']:
                                                                opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'] = opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'].lower()                                                
                                                        if opLayer["layerDefinition"]['drawingInfo'].has_key('labelingInfo'):
                                            
                                                            lblInfos = opLayer["layerDefinition"]['drawingInfo']['labelingInfo']
                                                            if len(lblInfos) > 0:
                                                                for lblInfo in lblInfos:
                                                                    if 'labelExpression' in lblInfo:
                                                                        result = re.findall(r"\[.*\]", lblInfo['labelExpression'])
                                                                        if len(result)>0:
                                                                            for res in result:
                                                                                lblInfo['labelExpression'] = str(lblInfo['labelExpression']).replace(res,str(res).lower())
                                            
                                                                    if 'labelExpressionInfo' in lblInfo:
                                                                        if 'value' in lblInfo['labelExpressionInfo']:
                                            
                                                                            result = re.findall(r"{.*}", lblInfo['labelExpressionInfo']['value'])
                                                                            if len(result)>0:
                                                                                for res in result:
                                                                                    lblInfo['labelExpressionInfo']['value'] = str(lblInfo['labelExpressionInfo']['value']).replace(res,str(res).lower())

                                                                    
                                                if opLayer.has_key("popupInfo"):
                                        
                                                    if 'mediaInfos' in opLayer['popupInfo'] and not opLayer['popupInfo']['mediaInfos'] is None:
                                                        for chart in opLayer['popupInfo']['mediaInfos']:
                                                            if 'value' in chart:
                                                                if 'normalizeField' in chart and not chart['normalizeField'] is None:
                                                                    chart['normalizeField'] = chart['normalizeField'].lower()
                                                                if 'fields' in chart['value']:
                                        
                                                                    for i in range(len(chart['value']['fields'])):
                                                                        chart['value']['fields'][i] = str(chart['value']['fields'][i]).lower()
                                                    if opLayer['popupInfo'].has_key("fieldInfos"):
                                        
                                                        for field in opLayer['popupInfo']['fieldInfos']:
                                                            newFld = str(field['fieldName']).lower()
                                                            if 'description' in opLayer['popupInfo']:
                                                                opLayer['popupInfo']['description'] = common.find_replace(obj = opLayer['popupInfo']['description'], 
                                                                                                                          find = "{" + field['fieldName'] + "}", 
                                                                                                                          replace = "{" + newFld + "}")
                                        
                                        
                                                            layerInfo['fields'].append({"PublishName":field['fieldName'],
                                                                                        'ConvertName':newFld})                                                
                                                            field['fieldName'] = newFld
                                                layersInfo[opLayer['id']] = layerInfo
                                
                            opLayers = webmap_data['operationalLayers']
                            for opLayer in opLayers:
                                layerInfo= {}
                                if replaceItem['SearchString'] in opLayer['url']:
    
                                    opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                    if replaceItem.has_key('ItemID'):
                                        opLayer['itemId'] = replaceItem['ItemID']
                                    else:
                                        opLayer['itemId'] = None
                                        #opLayer['itemId'] = get_guid()
                                    if replaceItem.has_key('convertCase'):
                                        if replaceItem['convertCase'] == 'lower':
                                            layerInfo = {}
                                            
                                            layerInfo['convertCase'] = replaceItem['convertCase']
                                            layerInfo['fields'] = []
                                            if opLayer.has_key("layerDefinition"):
                                                
                                                if opLayer["layerDefinition"].has_key('drawingInfo'):
                                                    if opLayer["layerDefinition"]['drawingInfo'].has_key('renderer'):
                                                        if 'field1' in opLayer["layerDefinition"]['drawingInfo']['renderer']:
                                                            opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'] = opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'].lower()                                                
                                                    if opLayer["layerDefinition"]['drawingInfo'].has_key('labelingInfo'):
                                            
                                                        lblInfos = opLayer["layerDefinition"]['drawingInfo']['labelingInfo']
                                                        if len(lblInfos) > 0:
                                                            for lblInfo in lblInfos:
                                                                if 'labelExpression' in lblInfo:
                                                                    result = re.findall(r"\[.*\]", lblInfo['labelExpression'])
                                                                    if len(result)>0:
                                                                        for res in result:
                                                                            lblInfo['labelExpression'] = str(lblInfo['labelExpression']).replace(res,str(res).lower())
                                                                    
                                                                if 'labelExpressionInfo' in lblInfo:
                                                                    if 'value' in lblInfo['labelExpressionInfo']:
                                                                      
                                                                        result = re.findall(r"{.*}", lblInfo['labelExpressionInfo']['value'])
                                                                        if len(result)>0:
                                                                            for res in result:
                                                                                lblInfo['labelExpressionInfo']['value'] = str(lblInfo['labelExpressionInfo']['value']).replace(res,str(res).lower())
                                                                                                                    
                                            if opLayer.has_key("popupInfo"):
                                                    
                                                if 'mediaInfos' in opLayer['popupInfo'] and not opLayer['popupInfo']['mediaInfos'] is None:
                                                    for k in range(len(opLayer['popupInfo']['mediaInfos'])):
                                                        chart = opLayer['popupInfo']['mediaInfos'][k]
                                                        if 'value' in chart:
                                                            if 'normalizeField' in chart and not chart['normalizeField'] is None:
                                                                chart['normalizeField'] = chart['normalizeField'].lower()
                                                            if 'fields' in chart['value']:
                                                                
                                                                for i in range(len(chart['value']['fields'])):
                                                                    chart['value']['fields'][i] = str(chart['value']['fields'][i]).lower()
                                                            opLayer['popupInfo']['mediaInfos'][k] = chart
                                                if opLayer['popupInfo'].has_key("fieldInfos"):
                                                              
                                                    for field in opLayer['popupInfo']['fieldInfos']:
                                                        newFld = str(field['fieldName']).lower()
                                                        if 'description' in opLayer['popupInfo']:
                                                            opLayer['popupInfo']['description'] = common.find_replace(obj = opLayer['popupInfo']['description'], 
                                                                               find = "{" + field['fieldName'] + "}", 
                                                                               replace = "{" + newFld + "}")
                                                        
                                                                                
                                                        layerInfo['fields'].append({"PublishName":field['fieldName'],
                                                                                    'ConvertName':newFld})                                                
                                                        field['fieldName'] = newFld
                                            layersInfo[opLayer['id']] = layerInfo
                                          
                   
                opLayers = webmap_data['operationalLayers']
                resultMap['Layers'] = {}
                for opLayer in opLayers:
                    currentID = opLayer['id']
                             
                    #if 'url' in opLayer:    
                        #opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))
                        
                    if 'applicationProperties' in webmap_data:
                        if 'editing' in webmap_data['applicationProperties'] and \
                           not webmap_data['applicationProperties']['editing'] is None:  
                            if 'locationTracking' in webmap_data['applicationProperties']['editing'] and \
                                not webmap_data['applicationProperties']['editing']['locationTracking'] is None: 
                                if 'info' in webmap_data['applicationProperties']['editing']['locationTracking'] and \
                                   not webmap_data['applicationProperties']['editing']['locationTracking']['info'] is None: 
                                    if 'layerId' in webmap_data['applicationProperties']['editing']['locationTracking']['info']: 
                                        if webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] == currentID:
                                            webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] = opLayer['id']
                        if 'viewing' in webmap_data['applicationProperties'] and \
                           not webmap_data['applicationProperties']['viewing'] is None:                    
                            if 'search' in webmap_data['applicationProperties']['viewing'] and \
                                not webmap_data['applicationProperties']['viewing']['search'] is None:
                                if 'layers' in webmap_data['applicationProperties']['viewing']['search'] and \
                                    not webmap_data['applicationProperties']['viewing']['search']['layers'] is None: 
                                        
                                    for k in range(len(webmap_data['applicationProperties']['viewing']['search']['layers'])):
                                        searchlayer =  webmap_data['applicationProperties']['viewing']['search']['layers'][k]                                  
                                        if searchlayer['id'] == currentID:
                                            searchlayer['id'] = opLayer['id']
                                            if 'fields' in searchlayer and \
                                               not searchlayer['fields'] is None:                                       
                                                for i in range(len(searchlayer['fields'])):
                                                    
                                                    searchlayer['fields'][i]['Name'] = str(searchlayer['fields'][i]['Name']).lower() 
                                            if 'field' in searchlayer and \
                                               not searchlayer['field'] is None:                                       
                                                searchlayer['field']['name'] = searchlayer['field']['name'].lower() 
                                                                                                 
                                            webmap_data['applicationProperties']['viewing']['search']['layers'][k] = searchlayer
                                            
                    if 'applicationProperties' in webmap_data:
                        webmap_data['applicationProperties'] = common.find_replace(webmap_data['applicationProperties'], currentID, opLayer['id'])
                    
                    resultLayer = {"Name":opLayer['title'],
                                  "ID":opLayer['id']
                                  } 
                    
                    if currentID in layersInfo:
                        resultLayer['FieldInfo'] = layersInfo[currentID]
                    resultMap['Layers'][currentID] = resultLayer


                if webmap_data.has_key('tables'):

                    opLayers = webmap_data['tables']
                    for opLayer in opLayers:
                        currentID = opLayer['id']
                    
                        #opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))
                        if 'applicationProperties' in webmap_data:
                            if 'editing' in webmap_data['applicationProperties'] and \
                               not webmap_data['applicationProperties']['editing'] is None:  
                                if 'locationTracking' in webmap_data['applicationProperties']['editing'] and \
                                   not webmap_data['applicationProperties']['editing']['locationTracking'] is None: 
                                    if 'info' in webmap_data['applicationProperties']['editing']['locationTracking'] and \
                                       not webmap_data['applicationProperties']['editing']['locationTracking']['info'] is None: 
                                        if 'layerId' in webmap_data['applicationProperties']['editing']['locationTracking']['info']: 
                                            if webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] == currentID:
                                                webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] = opLayer['id']
                            if 'viewing' in webmap_data['applicationProperties'] and \
                               not webmap_data['applicationProperties']['viewing'] is None:                    
                                if 'search' in webmap_data['applicationProperties']['viewing'] and \
                                   not webmap_data['applicationProperties']['viewing']['search'] is None:
                                    if 'layers' in webmap_data['applicationProperties']['viewing']['search'] and \
                                       not webmap_data['applicationProperties']['viewing']['search']['layers'] is None: 
                    
                                        for k in range(len(webmap_data['applicationProperties']['viewing']['search']['layers'])):
                                            searchlayer =  webmap_data['applicationProperties']['viewing']['search']['layers'][k]                                  
                                            if searchlayer['id'] == currentID:
                                                searchlayer['id'] = opLayer['id']
                                                if 'fields' in searchlayer and \
                                                   not searchlayer['fields'] is None:                                       
                                                    for i in range(len(searchlayer['fields'])):
                    
                                                        searchlayer['fields'][i]['Name'] = str(searchlayer['fields'][i]['Name']).lower() 
                                                if 'field' in searchlayer and \
                                                   not searchlayer['field'] is None:                                       
                                                    searchlayer['field']['name'] = searchlayer['field']['name'].lower() 
                    
                                                webmap_data['applicationProperties']['viewing']['search']['layers'][k] = searchlayer
                        
                        if 'applicationProperties' in webmap_data:
                            webmap_data['applicationProperties'] = common.find_replace(webmap_data['applicationProperties'], currentID, opLayer['id'])
                                           
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
            
            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)
            
            content = admin.content        
            userInfo = content.users.user()
            userCommunity = admin.community
            
            if folderName is not None and folderName != "":               
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName    
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']


            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=itemType,searchorg=False)
            
            if items['total'] >= 1:
                itemId = items['results'][0]['id']            
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                            text=json.dumps(webmap_data))
                if 'error' in results:
                    return results
            else:
                try:
                    item = userInfo.addItem(itemParameters=itemParams,
                            overwrite=True,
                            url=None,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None,
                            text=json.dumps(webmap_data))
                    group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                    shareResults = userInfo.shareItems(items=item.id,
                                                       groups=','.join(group_ids),
                                                       everyone=everyone,
                                                       org=org)
                    updateParams = arcrest.manageorg.ItemParameter()
                    updateParams.title = name
                    updateResults = item.updateItem(itemParameters=updateParams)                    
                except Exception,e: 
                    print e
            if item is None:
                return "Item could not be added"

           
            resultMap['Results']['itemId'] = item.id
            resultMap['folderId'] = folderId
            resultMap['Name'] = name
            return resultMap

       
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishMap",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })

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
            itemId = None
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
            del itemId
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
                    item = admin.content.getItem(itemId=webmap)
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
                        print "%s webmap created" % itemInfo['MapInfo']['Name']
                    else:
                        print str(itemInfo['MapInfo']['Results'])
                else:
                    print "Map not created"

                return map_results
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishedCombinedWebMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishedCombinedWebMap",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "publishedCombinedWebMap",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })        
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
        resItm = None
        if self.securityhandler.is_portal:
            url = self.securityhandler.org_url
        else:
            url = 'http://www.arcgis.com'
        try:
            res = []
            if isinstance(fs_config, list):
                for fs in fs_config:
                    if fs.has_key('ReplaceTag'):

                        resItm = {"ReplaceTag":fs['ReplaceTag'] }
                    else:
                        resItm = {"ReplaceTag":"{FeatureService}" }

                    resItm['FSInfo'] = self._publishFSFromMXD(config=fs, url=url)
                    
                    if not resItm['FSInfo'] is None and 'url' in resItm['FSInfo']:
                        print "%s created" % resItm['FSInfo']['url']
                        res.append(resItm)
                    else:
                        print str(resItm['FSInfo'])
                
            else:
                if fs_config.has_key('ReplaceTag'):

                    resItm = {"ReplaceTag":fs_config['ReplaceTag'] }
                else:
                    resItm = {"ReplaceTag":"{FeatureService}" }

                resItm['FSInfo'] = self._publishFSFromMXD(config=fs_config, url=url)
              
                if 'url' in resItm['FSInfo']:
                    print "%s created" % resItm['FSInfo']['url']
                    res.append(resItm)
                else:
                    print str(resItm['FSInfo'])              
       
            return res
        except common.ArcRestHelperError,e:
            raise e
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishFsFromMXD",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                                "function": "publishFsFromMXD",
                                "line": line,
                                "filename":  filename,
                                "synerror": synerror,
                                                }
                                                )
                
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                            "function": "publishFsFromMXD",
                            "line": line,
                            "filename":  filename,
                            "synerror": synerror,
                                            }
                                            )

        finally:
            resItm = None
            fs = None

            del resItm
            del fs

            gc.collect()
    #----------------------------------------------------------------------
    def publishFeatureCollections(self,configs):
        """
            publishs a feature service from a mxd
            Inputs:
                feature_service_config: Json file with list of feature service publishing details
            Output:
                feature service item information

        """
        config = None
        res = None
        resItm = None
        try:
            res = []
            if isinstance(configs, list):
                for config in configs:
                    if config.has_key('ReplaceTag'):

                        resItm = {"ReplaceTag":config['ReplaceTag'] }
                    else:
                        resItm = {"ReplaceTag":"{FeatureService}" }

                    if 'Zip' in config:
                        resItm['FCInfo'] = self._publishFeatureCollection(config=config)
                

                    if not resItm['FCInfo'] is None and 'id' in resItm['FCInfo']:
                        print "%s feature collection created" % resItm['FCInfo']['id']
                        res.append(resItm)
                    else:
                        print str(resItm['FCInfo'])

           
            return res 
        
        except common.ArcRestHelperError,e:
            raise e
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishFeatureCollections",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishFeatureCollections",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
        
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "publishFeatureCollections",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })

        finally:
            resItm = None
            config = None

            del resItm
            del config

            gc.collect()
    
    #----------------------------------------------------------------------
    def _publishFSFromMXD(self,config,url='http://www.arcgis.com'):
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
        itemId = None
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
            dataFle = None
            if 'Mxd' in config:
                dataFile = config['Mxd']
            elif 'Zip' in config:
                dataFile = config['Zip']
            # Service settings
            service_name = config['Title']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated
            if config.has_key('EnableEditTracking'):
                print "enableEditTracking parameter has been deprecated, please add a definition section to the config"                
                enableEditTracking = config['EnableEditTracking']
            else:
                #print "Please add an EnableEditTracking parameter to your feature service section"
                enableEditTracking = False
            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            if 'Capabilities' in config:
                print "Capabilities parameter has been deprecated, please add a definition section to the config"
                
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
            service_name_safe = service_name_safe.replace(':','_')
            service_name_safe = service_name_safe.replace('-','_')

            if os.path.exists(path=dataFile) == False:
                raise ValueError("data file does not exit")
           
            extension = os.path.splitext(dataFile)[1]
            
            if (extension == ".mxd"):
                dataFileType = "serviceDefinition"
                searchType = "Service Definition"
                sd_Info = arcrest.common.servicedef.MXDtoFeatureServiceDef(mxd_path=dataFile,
                                                                     service_name=service_name_safe,
                                                                     tags=None,
                                                                     description=None,
                                                                     folder_name=None,
                                                                     capabilities=capabilities,
                                                                     maxRecordCount=maxRecordCount,
                                                                     server_type='MY_HOSTED_SERVICES',
                                                                     url=url)
                publishParameters = arcrest.manageorg.PublishSDParmaeters(tags=sd_Info['tags'],
                                                                          overwrite='true')                
            elif (extension == ".zip"):
                dataFileType = "Shapefile"
                searchType = "Shapefile"
                sd_Info = {'servicedef':dataFile,'tags':config['Tags']}
                description = ""
                if 'Description' in config:
                    description = config['Description']                 
                publishParameters = arcrest.manageorg.PublishShapefileParameter(name=service_name,
                                                                            layerInfo={'capabilities':capabilities},
                                                                            description=description)
                if 'hasStaticData' in definition:
                    publishParameters.hasStaticData = definition['hasStaticData']

            if sd_Info is None:
                print "Publishing SD or Zip not valid"
                raise common.ArcRestHelperError({
                    "function": "_publishFsFromMXD",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": "Publishing SD or Zip not valid"
                })                   

            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)


            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = service_name
            itemParams.thumbnail = thumbnail
            itemParams.type = searchType
            itemParams.overwrite = True

            content = admin.content

            userInfo = content.users.user()
            userCommunity = admin.community

            if folderName is not None and folderName != "":               
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName    
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']
            
            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=service_name, itemType=searchType,searchorg=False)

            if items['total'] >= 1:
                itemId = items['results'][0]['id']  
            
            defItem = None
            
            if not itemId is None:
                defItem = content.getItem(itemId).userItem
                resultSD = defItem.updateItem(itemParameters=itemParams,
                                            data=sd_Info['servicedef'])
                if 'error' in resultSD:
                    return resultSD

            else:
                try:
                    defItem = userInfo.addItem(itemParameters=itemParams,
                            filePath=sd_Info['servicedef'],
                            overwrite=True,
                            url=None,
                            text=None,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None)
                except Exception,e: 
                    print e
                if defItem is None:
                    return "Item could not be added "

 
            try:
                serviceItem = userInfo.publishItem(
                    fileType=dataFileType,
                    itemId=defItem.id,
                    publishParameters=publishParameters,
                    overwrite = True,
                    wait=True)
            except Exception, e:
                print "Overwrite failed"
                
                sea = arcrest.find.search(securityHandler=self._securityHandler)
                items = sea.findItem(title =service_name, itemType='Feature Service',searchorg=False)
              
                if items['total'] >= 1:
                    itemId = items['results'][0]['id']

                else:
                
                    sea = arcrest.find.search(securityHandler=self._securityHandler)
                    items = sea.findItem(title =service_name_safe, itemType='Feature Service',searchorg=False)

                    if items['total'] >= 1:
                        itemId = items['results'][0]['id']
                    
                if not itemId is None:
                    existingItem = admin.content.getItem(itemId = itemId).userItem        
                    if existingItem.url is not None:
                        adminFS = AdminFeatureService(url=existingItem.url, securityHandler=self._securityHandler)
                        cap = str(adminFS.capabilities)
                        existingDef = {}
                    
                        if 'Sync' in cap:
                            print "Disabling Sync"
                            capItems = cap.split(',')
                            if 'Sync' in capItems:
                                capItems.remove('Sync')
                
                            existingDef['capabilities'] = ','.join(capItems)
                            enableResults = adminFS.updateDefinition(json_dict=existingDef)
                    
                            if 'error' in enableResults:
                                delres = userInfo.deleteItems(items=existingItem.id)
                                if 'error' in delres:
                                    print delres
                                    return delres
                                print "Delete successful"    
                            else:
                                print "Sync Disabled"
                        else:
                            print "Attempting to delete"
                            delres = userInfo.deleteItems(items=existingItem.id)
                            if 'error' in delres:
                                print delres
                                return delres
                            print "Delete successful"                                    
                        adminFS = None
                        del adminFS                                  
                    else:
                        print "Attempting to delete"
                        delres = userInfo.deleteItems(items=existingItem.id)
                        if 'error' in delres:
                            print delres
                            return delres
                        print "Delete successful"                                
                else:
                    print "Item exist and cannot be found, probably owned by another user."
                    raise common.ArcRestHelperError({
                        "function": "_publishFsFromConfig",
                        "line": lineno(),
                        "filename":  'publishingtools.py',
                        "synerror": "Item exist and cannot be found, probably owned by another user."
                    }
                    )       

                try:
                    serviceItem = userInfo.publishItem(
                        fileType=dataFileType,
                        itemId=defItem.id,
                        overwrite = True,
                        publishParameters=publishParameters,
                        wait=True)
                except Exception, e:
           
                    print "Overwrite failed, deleting"
                    delres = userInfo.deleteItems(items=existingItem.id)  
                    if 'error' in delres:
                        print delres
                        return delres
                     
                    print "Delete successful"      
                    try:
                        serviceItem = userInfo.publishItem(
                            fileType=dataFileType,
                            itemId=defItem.id,
                            overwrite = True,
                            publishParameters=publishParameters,
                            wait=True)
                    except Exception, e:
                        return e
                    
            results = {
                "url": serviceItem.url,
                "folderId": folderId,
                "itemId": serviceItem.id,
                "convertCase": self._featureServiceFieldCase,
                "messages":""
            }            
            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=serviceItem.id,
                                    groups=','.join(group_ids),
                                    everyone=everyone,
                                    org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = service_name
            updateResults = serviceItem.updateItem(itemParameters=updateParams)
            adminFS = AdminFeatureService(url=serviceItem.url, securityHandler=self._securityHandler)

            if enableEditTracking == True or str(enableEditTracking).upper() == 'TRUE':
              
                json_dict = {'editorTrackingInfo':{}}
                json_dict['editorTrackingInfo']['allowOthersToDelete'] = True
                json_dict['editorTrackingInfo']['allowOthersToUpdate'] = True
                json_dict['editorTrackingInfo']['enableEditorTracking'] = True
                json_dict['editorTrackingInfo']['enableOwnershipAccessControl'] = False

                enableResults = adminFS.updateDefinition(json_dict=json_dict)
                if 'error' in enableResults:
                    results['messages'] += enableResults

                json_dict = {'editFieldsInfo':{}}

                json_dict['editFieldsInfo']['creationDateField'] = ""
                json_dict['editFieldsInfo']['creatorField'] = ""
                json_dict['editFieldsInfo']['editDateField'] = ""
                json_dict['editFieldsInfo']['editorField'] = ""
                    
                layers = adminFS.layers
                tables = adminFS.tables
                for layer in layers:
                    if layer.canModifyLayer is None or layer.canModifyLayer == True:
                        if layer.editFieldsInfo is None:
                            layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                            if 'error' in layUpdateResult:
                               
                                layUpdateResult['error']['layerid'] = layer.id
                                results['messages'] += layUpdateResult['error']
                if not tables is None:
                    for layer in tables:
                        if layer.canModifyLayer is None or layer.canModifyLayer == True:
                            if layer.editFieldsInfo is None:
                                layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                                if 'error' in layUpdateResult:
                                   
                                    layUpdateResult['error']['layerid'] = layer.id
                                    results['messages'] += layUpdateResult['error']                                        


            if definition is not None:
                enableResults = adminFS.updateDefinition(json_dict=definition)
                if 'error' in enableResults:
                    results['messages'] += enableResults
        
            return results
   
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishFsFromConfig",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishFsFromConfig",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
        
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishFsFromConfig",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
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
           
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemId = None
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
            
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemId
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
                            if 'ReplaceString' in replaceItem:
                                if mapDet is not None and replaceItem['ReplaceString'] == mapDet['ReplaceTag'] and \
                                   replaceItem['ReplaceType'] == 'Map':
    
                                    replaceItem['ItemID'] = mapDet['MapInfo']['Results']['itemId']
                                    replaceItem['ItemFolder'] = mapDet['MapInfo']['folderId']
                                    replaceItem['LayerInfo'] = mapDet['MapInfo']['Layers']
                                elif mapDet is not None and replaceItem['ReplaceType'] == 'Layer':
                                    repInfo = replaceItem['ReplaceString'].split("|")
                                    if len(repInfo) == 2:
                                        if repInfo[0] == mapDet['ReplaceTag']:
                                            for key,value in mapDet['MapInfo']['Layers'].iteritems():
                                                if value["Name"] == repInfo[1]:
                                                    replaceItem['ReplaceString'] = value["ID"]

                            if replaceItem.has_key('ItemID'):
                                if replaceItem.has_key('ItemFolder') == False:

                                    itemId = replaceItem['ItemID']
                                 
                                    itemInfo = admin.content.getItem(itemId=itemId)
                                   
                                    if itemInfo.owner == self._securityHandler.username and itemInfo.ownerFolder:
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
                    print "%s app created" % itemInfo['AppInfo']['Name']
                else:
                    print str(itemInfo['AppInfo']['Results'])
            else:
                print "App was not created"
            return itemInfo 
      
        except common.ArcRestHelperError, e:
            raise e                                               
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishAppLogic",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishAppLogic",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
        
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishAppLogic",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
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
       
        except (common.ArcRestHelperError), e:
            raise e        
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
        
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "publishApp",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })

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
        itemId = None
        group_ids = None
        shareResults = None
        updateParams = None
        url = None
        updateResults = None
        portal = None
        try:
            resultApp = {'Results':{}}
            name = ''
            tags = ''
            description = ''
            extent = ''

            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:

                return {"Results":{"error": "%s does not exist" % itemJson}  }
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            content = admin.content        
            userInfo = content.users.user()
            userCommunity = admin.community
    
            folderName = config['Folder']
            if folderName is not None and folderName != "":               
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName 
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']
            
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
                        elif replaceItem['ReplaceType'] == 'Folder':
                            if 'id' in  userInfo.currentFolder:
                                folderID = userInfo.currentFolder['id']
                            else:
                                folderID = None
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],folderID)
                        elif replaceItem['ReplaceType'] == 'Global':
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])

            else:
                print "%s does not exist." % itemJson
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
        
            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=itemType,searchorg=False)
            
            if items['total'] >= 1:
                itemId = items['results'][0]['id']  
                
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                            text=json.dumps(itemData))
 
                if 'error' in results:
                    return results
            else:
                try:
                    item = userInfo.addItem(
                            itemParameters=itemParams,
                            overwrite=True,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None,
                            text=json.dumps(itemData))

                    group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
                    shareResults = userInfo.shareItems(items=item.id,
                                                       groups=','.join(group_ids),
                                                       everyone=everyone,
                                                       org=org)
                    updateParams = arcrest.manageorg.ItemParameter()
                    updateParams.title = name
    
                    url = url.replace("{AppID}",item.id)
                    portalself = admin.portals.portalSelf
                    if portalself.urlKey is None or portalself.customBaseUrl is None:
                        parsedURL = urlparse(url=self._securityHandler.org_url, scheme='', allow_fragments=True)
                        url = url.replace("{OrgURL}",parsedURL.netloc + parsedURL.path)
                    else:
                        url = url.replace("{OrgURL}", portalself.urlKey + '.' +  portalself.customBaseUrl)
                    updateParams.url = url                    
                    updateResults = item.updateItem(itemParameters=updateParams)                    
                except Exception,e: 
                    print e                 
            resultApp['Results']['itemId'] = item.id
            resultApp['folderId'] = folderId
            resultApp['Name'] = name
            return resultApp

     
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishApp",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishApp",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })

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
            itemId = None
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
            del itemId
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
        itemId = None
        group_ids = None
        shareResults = None
        updateParams = None
        resultApp = None
        updateResults = None
        try:
            resultApp = {'Results':{}}

            tags = ''
            description = ''
            extent = ''


            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:
                return {"Results":{"error": "%s does not exist" % itemJson}  }

            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            content = admin.content        
            userInfo = content.users.user()
            userCommunity = admin.community
            folderName = config['Folder']
            if folderName is not None and folderName != "":               
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                    userInfo.refresh()
                userInfo.currentFolder = folderName 
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

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
                            item = admin.content.getItem(itemId=replaceItem['ItemID'])
                            response = item.itemData()

                            layerNamesID = {}
                            layerIDs =[]

                            tableNamesID = {}
                            tableIDs =[]

                            if 'operationalLayers' in response:
                                for opLayer in response['operationalLayers']:
                                    #if 'LayerInfo' in replaceItem:
                                        #for layers in replaceItem['LayerInfo']:                                    
                                    layerNamesID[opLayer['title']] = opLayer['id']
                                    layerIDs.append(opLayer['id'])
                            if 'tables' in response:
                                for opLayer in response['tables']:
                                    tableNamesID[opLayer['title']] = opLayer['id']
                                    tableIDs.append(opLayer['id'])

                            widgets = itemData['widgets']
                            dataSourceIDToFields = {}
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
                                                    if 'LayerInfo' in replaceItem:
                                                        if dataSource['layerId'] in replaceItem['LayerInfo']:
                                                            layerIDSwitch.append({"OrigID":dataSource['layerId'],
                                                                                  "NewID":replaceItem['LayerInfo'][dataSource['layerId']]['ID']})
                                                                                  #'FieldInfo':replaceItem['LayerInfo'][dataSource['layerId']]['FieldInfo']})
                                                            
                                                            #dataSourceIDToFields[dataSource['id']] = {'NewID': replaceItem['LayerInfo'][dataSource['layerId']]['ID'],
                                                                                                      #'FieldInfo': replaceItem['LayerInfo'][dataSource['layerId']]['FieldInfo']}
                                                            dataSource['layerId'] = replaceItem['LayerInfo'][dataSource['layerId']]['ID']
                                                    elif layerNamesID.has_key(dataSource['name']):
                                                        layerIDSwitch.append({"OrigID":dataSource['layerId'],"NewID":layerNamesID[dataSource['name']] })
                                                        dataSource['layerId'] = layerNamesID[dataSource['name']]
                                            for dataSource in widget['dataSources']:
         
                                                if dataSource.has_key('filter'):
                                                    if dataSource['parentDataSourceId'] in dataSourceIDToFields:
                                                        if 'whereClause' in dataSource['filter']:
                                                            whercla = str(dataSource['filter']['whereClause'])
                                                            if pyparsingInstall:
                                                                try:
                                                                    selectResults = select_parser.select_stmt.parseString("select * from xyzzy where " + whercla)
                                                                   
                                                                    whereElements = list(selectResults['where_expr'])
                                                                    for h in range(len(whereElements)):
                                                                        for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                            if whereElements[h] == field['PublishName']:
                                                                                whereElements[h] = field['ConvertName']
                                                                                #whercla = whercla.replace(
                                                                                    #old=field['PublishName'], 
                                                                                    #new=field['ConvertName'])   
                                                                    dataSource['filter']['whereClause'] = " ".join(whereElements)
                                                                except select_parser.ParseException, pe:
                                                                    for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                        if whercla.contains(field['PublishName']):
                                                                            whercla = whercla.replace(
                                                                                old=field['PublishName'], 
                                                                                new=field['ConvertName'])

                                                                                                                                  
                                                            else:
                                                                
                                                                for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                    if whercla.contains(field['PublishName']):
                                                                        whercla = whercla.replace(
                                                                                       old=field['PublishName'], 
                                                                                       new=field['ConvertName'])
                                                                    
                                                                               


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

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=itemType,searchorg=False)
        
            if items['total'] >= 1:
                itemId = items['results'][0]['id']                    
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                                       text=json.dumps(itemData))
                if 'error' in results:
                    return results
            else:
                try:

                    item = userInfo.addItem(
                        itemParameters=itemParams,    
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None,
                        text=json.dumps(itemData))
                except Exception,e: 
                    print e                 
             
            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=item.id,
                                               groups=','.join(group_ids),
                                               everyone=everyone,
                                               org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = name
        
            updateResults = item.updateItem(itemParameters=updateParams)
            resultApp['Results']['itemId'] = item.id
                  
            resultApp['folderId'] = folderId
            resultApp['Name'] = name
            return resultApp
            
        
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishDashboard",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishDashboard",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishDashboard",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
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
            itemId = None
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
            del itemId
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
            fst = featureservicetools.featureservicetools(securityinfo=self)


            if isinstance(efs_config, list):
                for ext_service in efs_config:
                    resItm={"DeleteDetails": None,"AddDetails":None}
                    fURL = ext_service['URL']

                    if 'DeleteInfo' in ext_service:
                        if str(ext_service['DeleteInfo']['Delete']).upper() == "TRUE":
                            resItm['DeleteDetails'] = fst.DeleteFeaturesFromFeatureLayer(url=fURL, sql=ext_service['DeleteInfo']['DeleteSQL'])
                            if not 'error' in resItm['DeleteDetails'] :
                                print "Delete Successful: %s" % fURL
                            else:
                                print  str(resItm['DeleteDetails'])

                    resItm['AddDetails'] = fst.AddFeaturesToFeatureLayer(url=fURL, pathToFeatureClass = ext_service['FeatureClass'])

                    fsRes.append(resItm)

                    if not 'error' in resItm['AddDetails']:
                        print "Add Successful: %s " % fURL
                    else:
                        print str(resItm['AddDetails'])

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
        
        except common.ArcRestHelperError,e:
            raise e
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "updateFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "updateFeatureService",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "updateFeatureService",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
        finally:
            fst = None
            fURL = None
            resItm= None

            del fst
            del fURL
            del resItm

            gc.collect()
    #----------------------------------------------------------------------
    def _publishFeatureCollection(self, config):
        try:
  
            # Service settings
            zipfile = config['Zip']  
            service_name = config['Title']
            if config.has_key('DateTimeFormat'):
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat
                
            description = ""
            if 'Description' in config:
                description = config['Description']                    
            
            tags = config['Tags']
            snippet = config['Summary']
            extent = config['Extent']
    
            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated
    
            folderName = config['Folder']
            thumbnail = config['Thumbnail']
    
            typeKeywords = config['typeKeywords']                
                
            datestring = datetime.datetime.now().strftime(loc_df)
            service_name = service_name.replace('{DATE}',datestring)
            service_name = service_name.replace('{Date}',datestring)
  
            service_name_safe = service_name.replace(' ','_')
            service_name_safe = service_name_safe.replace(':','_')
            service_name_safe = service_name_safe.replace('-','_')         
  
            if os.path.exists(path=zipfile) == False:
                raise ValueError("Zip does not exit")
  
            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)
            content = admin.content
            feature_content = content.FeatureContent

            publishParameters = arcrest.manageorg.GenerateParameter(
                name=service_name,maxRecordCount=4000
                )
            
                   
            fcResults = feature_content.generate(publishParameters=publishParameters,
                itemId=None,
                filePath=zipfile,
                fileType='shapefile')
            
            if not 'featureCollection' in fcResults:
                raise common.ArcRestHelperError({
                    "function": "_publishFeatureCollection",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": fcResults
                })
            if not 'layers' in fcResults['featureCollection']:
                raise common.ArcRestHelperError({
                    "function": "_publishFeatureCollection",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": fcResults
                })
            
            fcJson = {'visibility':True,
                      'showLegend':True,
                      'opacity':1}
            for layer in fcResults['featureCollection']['layers']:
                oidFldName = ''
                highOID = -1
                popInfo = {'title':'',
                           'description':None,
                           'showAttachments': False,
                           'mediaInfo': [],
                           'fieldInfos': []
                           }
                if 'layerDefinition' in layer:
                    extVal = extent.split(',')
                    layer['layerDefinition']['extent'] = {'type':'extent',
                                       'xmin':extVal[0],
                                       'ymin':extVal[1],
                                       'xmax':extVal[2],
                                       'ymax':extVal[3]
                                       }
                    layer['layerDefinition']['spatialReference'] = {'wkid':102100}
                    
                    if 'fields' in layer['layerDefinition']:
                        for field in layer['layerDefinition']['fields']:
                            fieldInfos = None
                            if field['type'] == 'esriFieldTypeOID':
                                oidFldName = field['name']
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':False,
                                    'tooltip':'',
                                    'visible':False,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }
                                              
                            elif field['type'] == 'esriFieldTypeInteger':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':{
                                        'places':0,
                                        'digitSeparator':True
                                    },
                                    'stringFieldOption':'textbox'
                                }    
                            elif field['type'] == 'esriFieldTypeDouble':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':{
                                        'places':2,
                                        'digitSeparator':True
                                        },
                                    'stringFieldOption':'textbox'
                                }                                            
                            elif field['type'] == 'esriFieldTypeString':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }                                      
                            else:
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }                                                                      
                            if fieldInfos is not None:
                                popInfo['fieldInfos'].append(fieldInfos)
                                
                if 'featureSet' in layer:
                    if 'features' in layer['featureSet']:
                        for feature in layer['featureSet']['features']:
                            if 'attributes' in feature:
                                if feature['attributes'][oidFldName] > highOID:
                                    highOID = feature[oidFldName]
                layer['nextObjectId'] = highOID + 1
                
            fcJson['layers'] = fcResults['featureCollection']['layers']
            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.type = "Feature Collection"
            itemParams.title = service_name
            itemParams.thumbnail = thumbnail            
            itemParams.overwrite = True
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.extent = extent
            itemParams.tags = tags
            itemParams.typeKeywords = ",".join(typeKeywords)
            
            userInfo = content.users.user()
            userCommunity = admin.community
            
  
            if folderName is not None and folderName != "":               
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']
            
            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=service_name, itemType='Feature Collection',searchorg=False)
            itemId = None
            if items['total'] >= 1:
                itemId = items['results'][0]['id']            
            if not itemId is None:
                item = content.getItem(itemId).userItem
                resultSD = item.updateItem(itemParameters=itemParams,
                                           text=fcJson)
  
            else:
  
                resultSD = userInfo.addItem(itemParameters=itemParams,
                                            overwrite=True,
                                            url=None,
                                            text= fcJson,
                                            relationshipType=None,
                                            originItemId=None,
                                            destinationItemId=None,
                                            serviceProxyParams=None,
                                            metadata=None)
  
  
  
            if 'error' in resultSD:
                if not itemId is None:
                    print "Attempting to delete"
                    delres=userInfo.deleteItems(items=itemId)
                    if 'error' in delres:
                        print delres
                        return delres
                    print "Delete successful"                                
                else:
                    print "Item exist and cannot be found, probably owned by another user."
                    raise common.ArcRestHelperError({
                        "function": "_publishFeatureCollection",
                        "line": lineno(),
                        "filename":  'publishingtools.py',
                        "synerror": "Item exist and cannot be found, probably owned by another user."
                    })       
  
                resultSD = userInfo.addItem(itemParameters=itemParams,
                                            overwrite=True,
                                            url=None,
                                            text=fcResults['featureCollection'],
                                            relationshipType=None,
                                            originItemId=None,
                                            destinationItemId=None,
                                            serviceProxyParams=None,
                                            metadata=None)       
                return resultSD
            else:
                return resultSD
  
  
  
      
        except common.ArcRestHelperError, e:
            raise e
           
        except Exception as e:
            if (arcpyFound):
                if isinstance(e,(arcpy.ExecuteError)):
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishFeatureCollection",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                        "arcpyError": arcpy.GetMessages(2),
                    })
                else:
                    line, filename, synerror = trace()
                    raise common.ArcRestHelperError({
                        "function": "_publishFeatureCollection",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                    })
    
            else:
                line, filename, synerror = trace()
                raise common.ArcRestHelperError({
                    "function": "_publishFeatureCollection",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                })
        finally:
  
           
            gc.collect()
