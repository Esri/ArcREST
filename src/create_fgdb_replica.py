"""
   Returns a replicated fgdb from AGOL
   attachments are included in the fgdb
"""
from agol import featureservice

if __name__ == "__main__":
    username = ""
    password = ""
    url = ""
    fs = featureservice.FeatureService(url, username=username, password=password)
    print fs.createReplica(replicaName="test_replica", 
                           layers="0", 
                           returnAttachments=True,
                           returnAsFeatureClass=True, 
                           out_path=r"c:\temp\replicas")
    