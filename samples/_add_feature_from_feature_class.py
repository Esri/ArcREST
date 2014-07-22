#
#   Adds rows from the feature class
#   to a hosted feature service
#

import arcrest
try:
    fc = r"<some feature class>"
    url = "<service URL>"
    username = "<username>"
    password = "<password>"

    fl = arcrest.agol.layer.FeatureLayer(url=url, username=username, password=password)

    features = arcrest.agol.common.Feature.fc_to_features(fc)
    print fl.addFeature(features=features)

except ValueError, e:
    print e
