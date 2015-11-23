"""

   This sample shows how to copy a feature service
"""
import arcrest
import tempfile
import os
import uuid
import json
from arcresthelper import securityhandlerhelper
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

def main():
    proxy_port = None
    proxy_url = None    
    
    securityinfoSource = {}
    securityinfoSource['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfoSource['username'] = ""
    securityinfoSource['password'] = ""
    securityinfoSource['org_url'] = "http://www.arcgis.com"
    securityinfoSource['proxy_url'] = proxy_url
    securityinfoSource['proxy_port'] = proxy_port
    securityinfoSource['referer_url'] = None
    securityinfoSource['token_url'] = None
    securityinfoSource['certificatefile'] = None
    securityinfoSource['keyfile'] = None
    securityinfoSource['client_id'] = None
    securityinfoSource['secret_id'] = None   
    
    securityinfoTarget = {}
    securityinfoTarget['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfoTarget['username'] = ""
    securityinfoTarget['password'] = ""
    securityinfoTarget['org_url'] = "http://www.arcgis.com"
    securityinfoTarget['proxy_url'] = proxy_url
    securityinfoTarget['proxy_port'] = proxy_port
    securityinfoTarget['referer_url'] = None
    securityinfoTarget['token_url'] = None
    securityinfoTarget['certificatefile'] = None
    securityinfoTarget['keyfile'] = None
    securityinfoTarget['client_id'] = None
    securityinfoTarget['secret_id'] = None   

  
    itemId = ""#Item ID of item to copy    
    new_service_name = "" #name of new item
    try:      
        
        shhSource = securityhandlerhelper.securityhandlerhelper(securityinfoSource)
        shhTarget = securityhandlerhelper.securityhandlerhelper(securityinfoTarget)
        if shhSource.valid == False or shhTarget.valid == False:
            print shhSource.message + " "  + shhTarget.message
        else:        
          
            adminSource = arcrest.manageorg.Administration(securityHandler=shhSource.securityhandler)
            adminTarget = arcrest.manageorg.Administration(securityHandler=shhTarget.securityhandler)
            portalSource = adminSource.portals.portalSelf
            portalTarget = adminTarget.portals.portalSelf
            res = portalTarget.isServiceNameAvailable(name=new_service_name,
                                       serviceType='Feature Service')
            if 'available' in res:
                if res['available'] == False:
                    print "Pick a new name" 
                    return
            else:
                print "Pick a new name" 
                return
                
            itemSource = adminSource.content.getItem(itemId)
            
            fs = arcrest.agol.FeatureService(url=itemSource.url, securityHandler=shhSource.securityhandler, 
                                       initialize=True, 
                                       proxy_url=None, 
                                       proxy_port=None)   
          
            wkid = None
            wkt = None
            if 'wkid' in fs.initialExtent['spatialReference']:
                wkid = fs.initialExtent['spatialReference']['wkid']
            else:
                wkt = fs.initialExtent['spatialReference']['wkt']
            if fs.xssPreventionInfo is not None:
                xssPreventionEnabled = fs.xssPreventionInfo['xssPreventionEnabled']
                xssPreventionRule = fs.xssPreventionInfo['xssPreventionRule']
                xssInputRule = fs.xssPreventionInfo['xssInputRule']
            else:
                xssPreventionEnabled = None
                xssPreventionRule = None
                xssInputRule = None            
            
            #Edit tracking needs to be turned off when item is created    
            enableEditorTracking = False
            enableOwnershipAccessControl = False
            allowOthersToUpdate = False
            allowOthersToDelete = False

            if fs.syncCapabilities is not None:     
                supportsAsync = fs.syncCapabilities['supportsAsync']
                supportsRegisteringExistingData = fs.syncCapabilities['supportsRegisteringExistingData']
                supportsSyncDirectionControl = fs.syncCapabilities['supportsSyncDirectionControl']
                supportsPerLayerSync = fs.syncCapabilities['supportsPerLayerSync']
                supportsPerReplicaSync = fs.syncCapabilities['supportsPerReplicaSync']
                supportsRollbackOnFailure = fs.syncCapabilities['supportsRollbackOnFailure']
            else:
                supportsAsync = None 
                supportsRegisteringExistingData = None 
                supportsSyncDirectionControl = None 
                supportsPerLayerSync = None 
                supportsPerReplicaSync = None 
                supportsRollbackOnFailure = None

            createSerParams = arcrest.manageorg.CreateServiceParameters(
                        name=new_service_name, 
                        spatialReference=arcrest.geometry.SpatialReference(wkid=wkid, wkt=wkt), 
                        serviceDescription=fs.serviceDescription, 
                        hasStaticData=fs.hasStaticData, 
                        maxRecordCount=fs.maxRecordCount, 
                        supportedQueryFormats=fs.supportedQueryFormats, 
                        capabilities=fs.capabilities, 
                        description=fs.description, 
                        copyrightText=fs.copyrightText,
                        initialExtent=arcrest.geometry.Envelope(
                                                               xmin=fs.initialExtent['xmin'], 
                                                               ymin=fs.initialExtent['ymin'], 
                                                               xmax=fs.initialExtent['xmax'], 
                                                               ymax=fs.initialExtent['ymax'], 
                                                               wkid=wkid,
                                                               wkt=wkt), 
                        allowGeometryUpdates=fs.allowGeometryUpdates, 
                        units=fs.units, 
                        xssPreventionEnabled=xssPreventionEnabled, 
                        xssPreventionRule=xssPreventionRule, 
                        xssInputRule=xssInputRule,
                        currentVersion=fs.currentVersion,
                            enableEditorTracking = enableEditorTracking,
                            enableOwnershipAccessControl = enableOwnershipAccessControl,
                            allowOthersToUpdate = allowOthersToUpdate,
                            allowOthersToDelete = allowOthersToDelete,
                            supportsAsync = supportsAsync,
                            supportsRegisteringExistingData = supportsRegisteringExistingData,
                            supportsSyncDirectionControl = supportsSyncDirectionControl,
                            supportsPerLayerSync = supportsPerLayerSync,
                            supportsPerReplicaSync = supportsPerReplicaSync,
                            supportsRollbackOnFailure = supportsRollbackOnFailure,  
                            hasVersionedData = fs.hasVersionedData,
                            supportsDisconnectedEditing = fs.supportsDisconnectedEditing,
                            size =fs.size,
                            syncEnabled =fs.syncEnabled                                                                                              
            )
            userTarget = adminTarget.content.users.user()
            
            newServiceResult = userTarget.createService(createServiceParameter=createSerParams)
            print newServiceResult
            item = adminTarget.content.getItem(itemId=newServiceResult['itemId']).userItem
          
                 
            params = arcrest.manageorg.ItemParameter()
            params.title = new_service_name
            params.licenseInfo = itemSource.licenseInfo
            params.description = itemSource.description
            params.snippet = itemSource.snippet
            params.tags = itemSource.tags
            params.accessInformation = itemSource.accessInformation
            params.extent = itemSource.extent
            params.spatialReference = itemSource.spatialReference
            
            tempDir =  tempfile.gettempdir()
            filename = new_service_name #"%s" % uuid.uuid4().get_hex()
            tempFile = itemSource.saveThumbnail(fileName = filename, filePath= tempDir)
            params.thumbnail =  tempFile
            
            updateItemResults = item.updateItem(itemParameters=params,
                                                clearEmptyFields=True,
                                                data=None,
                                                metadata=None,
                                                text=None)
            
            print updateItemResults
                    
            if itemSource.protected:
                print item.protect()
            
            adminNewFS = arcrest.hostedservice.AdminFeatureService(url=newServiceResult['encodedServiceURL'], securityHandler=shhTarget.securityhandler)
            adminExistFS = fs.administration
            jsdic = {}
            exJson = adminExistFS.json
            jsdic['layers'] = exJson['layers']
            if 'tables' in exJson:
                jsdic['tables'] = exJson['tables']
            else:
                jsdic['tables'] = []
            for k in jsdic['layers']:
                k['spatialReference'] = {}
                if wkt is not None:
                    
                    k['spatialReference']['wkt'] = wkt
                if wkid is not None:
                                        
                    k['spatialReference']['wkid'] = wkid                    
                if 'adminLayerInfo' in k:
                    if 'tableName' in k['adminLayerInfo']:
                        k['adminLayerInfo'].pop('tableName',None)
            for k in jsdic['tables']:
                if 'adminLayerInfo' in k:
                    if 'tableName' in k['adminLayerInfo']:
                        k['adminLayerInfo'].pop('tableName',None)            
            res=adminNewFS.addToDefinition(json_dict=jsdic)
            print res
            
            
        if fs.editorTrackingInfo is not None:
      
            json_dict = {'editorTrackingInfo':{}}
            json_dict['editorTrackingInfo']['enableEditorTracking'] = fs.editorTrackingInfo['enableEditorTracking']          
            json_dict['editorTrackingInfo']['allowOthersToDelete'] = fs.editorTrackingInfo['allowOthersToDelete']
            json_dict['editorTrackingInfo']['allowOthersToUpdate'] =  fs.editorTrackingInfo['allowOthersToUpdate']
            json_dict['editorTrackingInfo']['enableOwnershipAccessControl'] = fs.editorTrackingInfo['enableOwnershipAccessControl']
            res = adminNewFS.updateDefinition(json_dict=json_dict)
            print res   
     
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        
if __name__ == "__main__":
    main()