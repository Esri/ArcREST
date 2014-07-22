"""
   Returns a replicated fgdb from AGOL
   attachments are included in the fgdb
"""
from arcrest.agol import featureservice
if __name__ == "__main__":
    try:

        username = ""
        password = ""
        url = ""
        print 'test'
        fs = featureservice.FeatureService(url, username=username, password=password)
        print fs.createReplica(replicaName="test_replica",
                           layers="0",
                           returnAttachments=True,
                           outputFormat="filegdb",
                           out_path=r"c:\temp")

    except ValueError, e:
        print e
