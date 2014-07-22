from arcrest.agol import featureservice

if __name__ == "__main__":
    try:
        url = "http://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Urban_Areas/FeatureServer"
        fs = featureservice.FeatureService(url=url)
        for serviceLayer in fs.layers:
            print serviceLayer.name

    except ValueError, e:
        print e

