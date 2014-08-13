###############################
#  Sample showing various bulk#
#  update methods of adding   #
#  new features.              #
###############################

from arcrest.agol.layer import FeatureLayer
from arcrest.agol.common import Feature
if __name__ == "__main__":
    url = "<url>"
    username = "<username"
    password = "<password>"
    fc = r"<path to feature class" # must match projection on destionation feature layer, or you'll need to re-project your local data
    fl = FeatureLayer(url, username, password)
    fl.deleteFeatures(where="1=1")
    # Method 1). Use addFeatures()
    fl.addFeatures(fc)
    # Method 2). use applyEdits()
    fl.deleteFeatures(where="1=1")
    features = Feature.fc_to_features(fc)
    fl.applyEdits(addFeatures=features)
