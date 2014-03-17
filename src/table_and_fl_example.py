from agol import featureservice

if __name__ == "__main__":
    fs = featureservice.FeatureService(url="http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/SanFrancisco/311Incidents/FeatureServer")
    for table in fs.tables:
        print table.name

    
    