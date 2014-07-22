from arcrest.agol import featureservice

if __name__ == "__main__":
    try:
        username = ""
        password = ""
        url = ""
        fs = featureservice.FeatureService(url, username=username, password=password)
        print "You have %s replicas" % len(fs.replicas)
        for replica in fs.replicas:
            print "unregistering replica: %s with the name: %s" % (replica['replicaID'], replica['replicaName'])
            fs.unRegisterReplica(replica['replicaID'])
        print "You now have %s replicas" % fs.replicas

    except ValueError, e:
        print e

