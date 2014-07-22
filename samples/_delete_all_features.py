#
#   Simple Delete All Example
#   Erases all features in a given feature layer
#
import arcrest

url = r"<service url>"
username = "<username>"
password = "<password>"

fl = arcrest.agol.layer.FeatureLayer(url=url,
                                username=username,
                                password=password)
print fl.deleteFeatures(where="1=1")
print 'all features removed'

