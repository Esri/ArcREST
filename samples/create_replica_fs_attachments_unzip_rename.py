"""
  This sample shows how to create a replica from a large FS with attachments.
  Download a zip file, unzip zip file, and rename output file gdb
  ArcREST version 3.5.x
  Python 2/3
"""
from __future__ import print_function
from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureService
from arcrest.common.filters import LayerDefinitionFilter
import os, zipfile

if __name__ == "__main__":
    username = "agol_username"
    password = "agol_password"
    url = "http://services1.arcgis.com/***/rest/services/yourservice/FeatureServer"
    proxy_port = None
    proxy_url = None
    agolSH = AGOLTokenSecurityHandler(username=username, password=password)
    repName = 'MyHostedFeatureLayerName' #Name of replica and unzipped file gdb
    filelocation = 'C:\\Temp'

    fs = FeatureService(url=url,
                        securityHandler=agolSH,
                        proxy_port=proxy_port,
                        proxy_url=proxy_url,
                        initialize=True)

    result = fs.createReplica(replicaName=repName,
                              layers=[0,1,2,3,4,5,6,7,8],
                              async=True,
                              returnAttachments=True,
                              returnAttachmentsDatabyURL=True,
                              attachmentsSyncDirection='bidirectional',
                              wait=True,
                              dataFormat="filegdb",
                              out_path=filelocation)

    dzipfile = '{0}'.format(result)
    parentdirectory = os.path.dirname(os.path.abspath(dzipfile))
    newzip = zipfile.ZipFile(result)
    newzip.extractall(parentdirectory)
    z = zipfile.ZipFile(result, 'r')
    dirs = list(set([os.path.dirname(x) for x in z.namelist()]))
    extractedfgdb = '{0}'.format(os.path.join(parentdirectory,str(dirs[0])))
    renamefgdb = '{0}\\{1}.gdb'.format(parentdirectory,repName) # Use repName or change to your choice of string value
    os.rename(extractedfgdb,renamefgdb)
