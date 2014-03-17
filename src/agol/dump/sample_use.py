import services

if __name__ == "__main__":
    url = "http://services2.arcgis.com/PWJUSsdoJDp7SgLj/arcgis/rest/services/Triangle/FeatureServer/0"
    s = services.FeatureService(url, "AndrewSolutions", "fujiFUJI1")

    print s.fields
    print s.count
    s.username = ""
    s.password = ""
    s.url = "http://services.arcgis.com/iTQUx5ZpNUh47Geb/arcgis/rest/services/CensusDivisions2010/FeatureServer/4"
    print s.url
    print s.count
    print s.fields

    print 'fin'
