"""
   This sample shows how to recursively walk into a parent directory, find all files matching a specific file extension
   and add them to your ArcGIS Online organization.
"""
import arcpy.AddMessage
import os
import arcrest
from arcresthelper import securityhandlerhelper

org_url = 'http://www.arcgis.com'
username = ''
password = ''

top_level_directory = r'D:\files'
file_extension = '.pdf'
file_tags = 'pdf'
file_type = 'PDF'

proxy_port = None
proxy_url = None


# create security dictionary object
securityinfo = dict(
    security_type='Portal', #LDAP, NTLM, OAuth, Portal, PKI
    username=username,
    password=password,
    org_url=org_url,
    proxy_url=proxy_url,
    proxy_port=proxy_port,
    referer_url=None,
    token_url=None,
    certificatefile=None,
    keyfile=None,
    client_id=None,
    secret_id=None
)

shh = securityhandlerhelper.securityhandlerhelper(securityinfo)

if shh.valid == False:
    print shh.message

else:
    admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
    content = admin.content
    userInfo = content.users.user()

    # walk into the top level directory
    for top_dir, dir_list, file_list in os.walk(top_level_directory):

        for this_file in file_list:

            # check to see if the file extension matches
            if os.path.splitext(this_file) == file_extension:

                # get the full file path
                file_path = os.path.join(top_dir, this_file)

                # create item parameter object instance
                itemParams = arcrest.manageorg.ItemParameter()

                # get the title from the file name
                itemParams.title = os.path.split(os.path.basename(file_path))[0]

                # set the file type, pretty boring
                itemParams.type = file_type

                # overwrite - if the item already exists, it will be overwritten
                itemParams.overwrite = True

                # set tags
                itemParams.tags = file_tags

                # set the snippet to simply be the file name with the extension
                itemParams.snippet = os.path.basename(file_path)

                # set the type keywords to the same thing as the tags for now
                itemParams.typeKeywords = file_tags

                # this is just the entire path to the file
                itemParams.filename = file_path

                # with the item parameters set up, now upload the file
                item = userInfo.addItem(
                    itemParameters=itemParams,
                    overwrite=True,
                    relationshipType=None,
                    originItemId=None,
                    destinationItemId=None,
                    serviceProxyParams=None,
                    metadata=None
                )

                # display success
                arcpy.AddMessage("{} successfully uploaded and ArcGIS Online item created.".format(item.title))

