"""
   This sample shows how to copy a feature service
   Python 2
   ArcREST 3.0.1
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

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfo['username'] = ""
    securityinfo['password'] = ""
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None


    itemId = "f13d20825b12491295084129a21e7a42"
    new_service_name = "NewService0"
    try:

        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if shh.valid == False:
            print shh.message
        else:

            admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            portal = admin.portals.portalSelf
            res = portal.isServiceNameAvailable(name=new_service_name,
                                       serviceType='Feature Service')
            if 'available' in res:
                if res['available'] == False:
                    print "Pick a new name"
                    return
            else:
                print "Pick a new name"
                return

            item = admin.content.getItem(itemId)
            fs = arcrest.agol.FeatureService(url=item.url, securityHandler=shh.securityhandler,
                                       initialize=True,
                                       proxy_url=None,
                                       proxy_port=None)

            wkid = None
            wkt = None
            if 'wkid' in fs.initialExtent['spatialReference']:
                wkid = fs.initialExtent['spatialReference']['wkid']
            else:
                wkt = fs.initialExtent['spatialReference']['wkt']
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
            user = admin.content.users.user()

            newServiceResult = user.createService(createServiceParameter=createSerParams)
            print newServiceResult
            item = admin.content.getItem(itemId=newServiceResult['itemId']).userItem

            params = arcrest.manageorg.ItemParameter()
            params.title = new_service_name
            updateItemResults = item.updateItem(itemParameters=params,
                                                clearEmptyFields=True,
                                                data=None,
                                                metadata=None,
                                                text=None)

            print updateItemResults

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
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

if __name__ == "__main__":
    main()