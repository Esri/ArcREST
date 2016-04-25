"""
   This sample shows to load assignments from csv
   Python 2.x/3.x
   ArcREST 3.5
"""

from __future__ import print_function
import arcrest
from arcrest.common.general import Feature
from arcresthelper import featureservicetools
from arcresthelper import common
from arcrest.packages import six
import csv
from datetime import datetime
from arcrest.agol import FeatureLayer

def UnicodeDictReader(utf8_data, **kwargs):
    if six.PY3 == True:
        csv_reader = csv.DictReader(utf8_data, **kwargs)
        for row in csv_reader:
            yield {key: value for key, value in row.items()}
    else:
        csv_reader = csv.DictReader(utf8_data, **kwargs)
        for row in csv_reader:
            yield {unicode(key, 'utf-8-sig'): unicode(value, 'utf-8-sig') for key, value in row.items()}
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
    try:
        proxy_port = None
        proxy_url = None
    
        securityinfo = {}
        securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
        securityinfo['username'] = ""#<UserName>
        securityinfo['password'] = ""#<Password>
        securityinfo['org_url'] = "http://www.arcgis.com"
        securityinfo['proxy_url'] = proxy_url
        securityinfo['proxy_port'] = proxy_port
        securityinfo['referer_url'] = None
        securityinfo['token_url'] = None
        securityinfo['certificatefile'] = None
        securityinfo['keyfile'] = None
        securityinfo['client_id'] = None
        securityinfo['secret_id'] = None
    
    
        workforceProjectID = '' #Workforce project number

        assignmentAreasID = '' #ID of service to get centroids from
        assignmentAreaLayerName = ''#layer in servuce
        assignmentAreaNameField = ''#field with name of id area
        
        csvPath = r".\dataToLookup.csv"#<Path with data>
        workerCol = 'worker'
        areaCol  = 'area'
        descriptionCol = "description"
        notesCol = "notes"
        supervisorCol = "supervisor"
         
        assignmentType = 2
        status = 1
        
        workerNameToID = {}
        dispatcherNameToID = {}
        areaNameToID = {}
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid == False:
            print (fst.message)
        else:
            portalAdmin = arcrest.manageorg.Administration(securityHandler=fst.securityhandler)
            #Get the assignment areas
            fs = fst.GetFeatureService(itemId=assignmentAreasID,returnURLOnly=False)
            if not fs is None:
                fs_url = fst.GetLayerFromFeatureService(fs=fs,layerName=assignmentAreaLayerName,returnURLOnly=True)
                if not fs_url is None:

                    fl = FeatureLayer(
                        url=fs_url,
                        securityHandler=fst.securityhandler,
                        proxy_port=proxy_port,
                        proxy_url=proxy_url,
                        initialize=True)                    
                    areaResults =  fl.query(**{'where':"1=1",'outSR':'102100','out_fields':assignmentAreaNameField,'returnGeometry':False,'returnCentroid':True})
                   
                    for area in areaResults:
                        arDict = area.asDictionary
                        areaNameToID[arDict['attributes'][assignmentAreaNameField]] = arDict['centroid']
                    
            #Get the workers
            item = portalAdmin.content.getItem(itemId=workforceProjectID)
            itemData = item.itemData()
            if 'workers' in itemData:
                fl = FeatureLayer(
                    url=itemData['workers']['url'],
                    securityHandler=fst.securityhandler,
                    proxy_port=proxy_port,
                    proxy_url=proxy_url,
                    initialize=True)
            
                workersResults = fl.query(where="1=1",out_fields='OBJECTID, NAME',returnGeometry=False)
                for worker in workersResults:
                    workerNameToID[worker.get_value('name')] = worker.get_value('OBJECTID')
            
            if 'dispatchers' in itemData:
                fl = FeatureLayer(
                    url=itemData['dispatchers']['url'],
                    securityHandler=fst.securityhandler,
                    proxy_port=proxy_port,
                    proxy_url=proxy_url,
                    initialize=True)
            
                dispatcherResults = fl.query(where="1=1",out_fields='OBJECTID, NAME',returnGeometry=False)
                for dispatcher in dispatcherResults:
                    dispatcherNameToID[dispatcher.get_value('name')] = dispatcher.get_value('OBJECTID')
                    
    
            if 'assignments' in itemData:
                features = []
                
                fl = FeatureLayer(
                    url=itemData['assignments']['url'],
                    securityHandler=fst.securityhandler,
                    proxy_port=proxy_port,
                    proxy_url=proxy_url,
                    initialize=True)
                print(fl.deleteFeatures(where="1=1"))
                with open(csvPath) as csvfile:
                    reader = UnicodeDictReader(csvfile)
                    for row in reader:
                        json_string={}
                        json_string['geometry'] = {}
                       
                        centroidInfo = areaNameToID[row[areaCol].strip()]
                        
                        json_string['geometry']['x'] = centroidInfo['x']
                        json_string['geometry']['y'] = centroidInfo['y']
                        json_string['attributes'] ={}
                        json_string['attributes']['workerId'] = workerNameToID[row[workerCol].strip()]
                        json_string['attributes']['description'] = row[descriptionCol]
                        json_string['attributes']['notes'] = row[notesCol]
                        json_string['attributes']['assignmentType'] = assignmentType
                        json_string['attributes']['status'] = status
                        json_string['attributes']['dispatcherId'] = dispatcherNameToID[row[supervisorCol].strip()]
                        
                         
                        features.append(Feature(json_string=json_string))
                    results = fl.addFeature(features=features)
    
                    if 'error' in results:
                        print ("Error in response from server:  %s" % results['error'])
    
                    else:
                        if results['addResults'] is not None:
                            featSucces = 0
                            for result in results['addResults']:
                                if 'success' in result:
                                    if result['success'] == False:
                                        if 'error' in result:
                                            print ("Error info: %s" % (result['error']))
                                    else:
                                        featSucces = featSucces + 1
    
                            print ("%s features added to %s" % (featSucces,fl.name))
                        else:
                            print ("0 features added to %s /n result info %s" % (fl.name,str(results)))             

    except (common.ArcRestHelperError) as e:
        print ("error in function: %s" % e[0]['function'])
        print ("error on line: %s" % e[0]['line'])
        print ("error in file name: %s" % e[0]['filename'])
        print ("with error message: %s" % e[0]['synerror'])
        if 'arcpyError' in e[0]:
            print ("with arcpy message: %s" % e[0]['arcpyError'])

    except:
        line, filename, synerror = trace()
        print ("error on line: %s" % line)
        print ("error in file name: %s" % filename)
        print ("with error message: %s" % synerror)
if __name__ == "__main__":
    main()