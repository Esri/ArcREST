"""
   This sample shows how to update the
   large thumbnail and thumbnails of an items
   defined in a csv
   CSV requires the following fields
    - itemid - ID of AGOL item
    - thumbnail(optional) - name of image in the image folder
    - largethumbnail(optional) - name of image in the image folder

   A folder with the images is also required

   Python 2.x
   ArcREST 3.0.1


"""
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.security import PortalTokenSecurityHandler

import sys, os, datetime
import csv
import arcresthelper
from arcresthelper import orgtools
from arcresthelper import common as Common

dateTimeFormat = '%Y-%m-%d %H:%M'

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
    username = "<username>"
    password = "<password>"
    url = "<portal or AGOL url>"

    configFiles =  'path to csv file, can be relative to script'
    imageFolder = 'path to image folder, can be relative to script'


    sciptPath = os.getcwd()
    try:
        print "###############Script Started#################"
        print datetime.datetime.now().strftime(dateTimeFormat)
        if os.path.exists(imageFolder) == False:
            imageFolder = os.path.join(sciptPath,imageFolder)
        elif os.path.isabs(imageFolder) == False:
            imageFolder = os.path.join(sciptPath,imageFolder)
        if os.path.exists(imageFolder) == False:
            print "Image folder %s could not be located" % imageFolderName
            return
        if os.path.isfile(configFiles) == False:
            print "csv file %s could not be located" % configFiles
            return


        agolSH = AGOLTokenSecurityHandler(username=username,
                                          password=password,org_url=url)

        print "Login with token: %s" % agolSH.token

        portalAdmin = arcrest.manageorg.Administration(securityHandler=agolSH)
        content = portalAdmin.content

        with open(configFiles, 'rb') as csvfile:

            for row in csv.DictReader(csvfile,dialect='excel'):
                if not 'itemid' in row:
                    print "itemID could not be found if table"
                    return

                itemid = row['itemid']
                item = content.getItem(itemid)
                itemParams = arcrest.manageorg.ItemParameter()

                if 'thumbnail' in row:
                    print "%s to be applied to thumbnail of %s" % (row['thumbnail'],itemid )
                    image = os.path.join(imageFolder,row['thumbnail'])
                    if os.path.isfile(image):
                        itemParams.thumbnail = image
                    else:
                        print "image %s could not be located" % row['thumbnail']

                if 'largethumbnail' in row:
                    print "%s to be applied to largethumbnail of %s" % (row['largethumbnail'],itemid )
                    largeimage = os.path.join(imageFolder,row['largethumbnail'])
                    if os.path.isfile(largeimage):
                        itemParams.largeThumbnail = largeimage
                    else:
                        print "image %s could not be located" % row['largethumbnail']

                print(item.userItem.updateItem(itemParameters=itemParams))

    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror

    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"

if __name__ == "__main__":
    main()