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
def main():
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


    itemId = ""#<Item ID>
    csvPath = r".\dataToLoad.csv"#<Path with data>

    xCol = "x"
    yCol = "y"
    descriptionCol = "description"
    statusCol = "status"
    priorityCol = "priority"
    assignmentTypeCol = "assignmentType"
    workorderCol = "workOrderId"
    locationCol = "location"
    dateTimeFormat = "%m/%d/%Y %I:%M:%S %p"#1/28/2016 4:59:59 AM
    dueDateCol = "dueDate"
    notesCol = "notes"

    fl = None
    fls = None
    fs = None
    try:
        fst = featureservicetools.featureservicetools(securityinfo)
        if fst.valid == False:
            print (fst.message)
        else:
            fs = fst.GetFeatureService(itemId=itemId,returnURLOnly=False)
            if not fs is None:
                fls = fs.layers
                if len(fls) > 0 :
                    fl = fls[0]
            if fl is None:
                print ("Layer Not Found")
                return
            features = []
            with open(csvPath) as csvfile:
                reader = UnicodeDictReader(csvfile)
                for row in reader:
                    json_string={}
                    json_string['geometry'] = {}
                    if xCol not in row or yCol not in row:
                        print ("X or Y col not found")
                        return
                    json_string['geometry']['x'] = row[xCol]
                    json_string['geometry']['y'] = row[yCol]
                    json_string['attributes'] ={}
                    if descriptionCol is not None:
                        if descriptionCol in row:
                            json_string['attributes']['description'] = row[descriptionCol]
                        else:
                            json_string['attributes']['description'] = descriptionCol
                    if statusCol is not None:
                        if statusCol in row:
                            json_string['attributes']['status'] = row[statusCol]
                        else:
                            json_string['attributes']['status'] = statusCol
                    if notesCol is not None:
                        if notesCol in row:
                            json_string['attributes']['notes'] = row[notesCol]
                        else:
                            json_string['attributes']['notes'] = notesCol
                    if priorityCol is not None:
                        if priorityCol in row:
                            json_string['attributes']['priority'] = row[priorityCol]
                        else:
                            json_string['attributes']['priority'] = priorityCol
                    if assignmentTypeCol is not None:
                        if assignmentTypeCol in row:
                            json_string['attributes']['assignmentType'] = row[assignmentTypeCol]
                        else:
                            json_string['attributes']['assignmentType'] = assignmentTypeCol
                    if workorderCol is not None:
                        if workorderCol in row:
                            json_string['attributes']['workOrderId'] = row[workorderCol]
                        else:
                            json_string['attributes']['workOrderId'] = workorderCol
                    if locationCol is not None:
                        if locationCol in row:
                            json_string['attributes']['location'] = row[locationCol]
                        else:
                            json_string['attributes']['location'] = locationCol
                    if dueDateCol is not None:
                        if dueDateCol in row:
                            timeVal = datetime.strptime(row[dueDateCol], dateTimeFormat)
                        else:
                            timeVal = datetime.strptime(dueDateCol, dateTimeFormat)
                        json_string['attributes']['dueDate'] = common.local_time_to_online(dt=timeVal)

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

    except (common.ArcRestHelperError),e:
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