#
#   Simple Delete All Example
#   Erases all features in a given feature layer
#
import arcrest
if __name__ == "__main__":
    try:
        url = r"<service url>"
        username = "<username>"
        password = "<password>"

        fl = arcrest.agol.layer.FeatureLayer(url=url,
                                        username=username,
                                        password=password)
        print fl.deleteFeatures(where="1=1")
        print 'all features removed'

    except ValueError, e:
            print e