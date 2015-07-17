"""
   This sample shows how to copy a feature service

"""
import arcrest
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
    
    securityInfo = {}
    securityInfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityInfo['username'] = ""
    securityInfo['password'] = ""
    securityInfo['org_url'] = ""
    securityInfo['proxy_url'] = proxy_url
    securityInfo['proxy_port'] = proxy_port
    securityInfo['referer_url'] = None
    securityInfo['token_url'] = None
    securityInfo['certificatefile'] = None
    securityInfo['keyfile'] = None
    securityInfo['client_id'] = None
    securityInfo['secret_id'] = None   
    
   
    itemId = "1c2d57215d1241e3a17041a353ebf222"    
    new_service_name = "l21d12dd"
    try:      
        
        shh = securityhandlerhelper.securityhandlerhelper(securityInfo)
        if shh.valid == False:
            print shh.message
        else:        
          
            portalAdmin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            portal = portalAdmin.portals(portalId='self')
            res = portal.checkServiceName(name=new_service_name,
                                       serviceType='Feature Service')
            if 'available' in res:
                if res['available'] == False:
                    print "Pick a new name" 
                    return
            else:
                print "Pick a new name" 
                return
            content = portalAdmin.content
            
                
            item = content.item(itemId)
            fs = arcrest.agol.FeatureService(url=item.url, securityHandler=shh.securityhandler, 
                                       initialize=True, 
                                       proxy_url=None, 
                                       proxy_port=None)   
            
            uc = content.usercontent(username=shh.securityhandler.username)
            
            createSerParams = arcrest.manageorg.parameters.CreateServiceParameters(
                                                                                  name=new_service_name, 
                                                                                  spatialReference=arcrest.geometry.SpatialReference(wkid=fs.spatialReference['wkid']), 
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
                                                                                                                         wkid=fs.initialExtent['spatialReference']['wkid']), 
                                                                                  allowGeometryUpdates=fs.allowGeometryUpdates, 
                                                                                  units=fs.units, 
                                                                                  xssPreventionEnabled=fs.xssPreventionInfo['xssPreventionEnabled'], 
                                                                                  xssPreventionRule=fs.xssPreventionInfo['xssPreventionRule'], 
                                                                                  xssInputRule=fs.xssPreventionInfo['xssInputRule'],
                                                                                  currentVersion=fs.currentVersion,
                                                                                      enableEditorTracking = fs.editorTrackingInfo['enableEditorTracking'],
                                                                                      enableOwnershipAccessControl = fs.editorTrackingInfo['enableOwnershipAccessControl'],
                                                                                      allowOthersToUpdate = fs.editorTrackingInfo['allowOthersToUpdate'],
                                                                                      allowOthersToDelete = fs.editorTrackingInfo['allowOthersToDelete'],
                                                                                      supportsAsync = fs.syncCapabilities['supportsAsync'],
                                                                                      supportsRegisteringExistingData = fs.syncCapabilities['supportsRegisteringExistingData'],
                                                                                      supportsSyncDirectionControl = fs.syncCapabilities['supportsSyncDirectionControl'],
                                                                                      supportsPerLayerSync = fs.syncCapabilities['supportsPerLayerSync'],
                                                                                      supportsPerReplicaSync = fs.syncCapabilities['supportsPerReplicaSync'],
                                                                                      supportsRollbackOnFailure = fs.syncCapabilities['supportsRollbackOnFailure'],  
                                                                                      hasVersionedData = fs.hasVersionedData,
                                                                                      supportsDisconnectedEditing = fs.supportsDisconnectedEditing,
                                                                                      size =fs.size,
                                                                                      syncEnabled =fs.syncEnabled                                                                                              
            )
            newServiceResult = uc.createService(createServiceParameter=createSerParams)
            print newServiceResult
           
            uc = content.usercontent()           
            params = item.itemParameters
            params.title = new_service_name
            updateItemResults = uc.updateItem(itemId=newServiceResult['itemId'],
                   updateItemParameters=params,
                   folderId=None,
                   clearEmptyFields=True,
                   filePath=None,
                   url=None,
                   text=None)
            
            print updateItemResults
            
            #new_item = content.item(newServiceResult['itemId'])
             
            adminNewFS = arcrest.hostedservice.AdminFeatureService(url=newServiceResult['encodedServiceURL'], securityHandler=shh.securityhandler)
            adminExistFS = fs.administration
            jsdic = {}
            exJson = adminExistFS.json
            jsdic['layers'] = exJson['layers']
            if 'tables' in exJson:
                jsdic['tables'] = exJson['tables']
            else:
                jsdic['tables'] = []
            for k in jsdic['layers']:
                if 'adminLayerInfo' in k:
                    if 'tableName' in k['adminLayerInfo']:
                        k['adminLayerInfo'].pop('tableName',None)
            for k in jsdic['tables']:
                if 'adminLayerInfo' in k:
                    if 'tableName' in k['adminLayerInfo']:
                        k['adminLayerInfo'].pop('tableName',None)            
            res=adminNewFS.addToDefinition(json_dict=jsdic)
            print res
            
    except:
        line, filename, synerror = trace()
        print("error on line: %s" % line)
        print("error in file name: %s" % filename)
        print("with error message: %s" % synerror)
        
if __name__ == "__main__":
    main()