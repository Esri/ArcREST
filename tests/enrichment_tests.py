"""
   Testing for geoenrichment functions
"""
import tempfile
from arcrest.common.geometry import Polygon, Point
from arcrest import AGOLTokenSecurityHandler
from arcrest import GeoEnrichment
if __name__ == "__main__":
    username = ""
    password = ""
    sh = AGOLTokenSecurityHandler(username, password)
    g = GeoEnrichment(securityHanlder=sh)
    #print g.allowedCountryNames
    #print g.allowedThreeDigitNames
    #print g.allowedTwoDigitCountryCodes
    #print g.findCountryThreeDigitCode(g.allowedCountryNames[11])
    #print g.findCountryTwoDigitCode(g.allowedCountryNames[11])
    #print g.queryDataCollectionByName(g.allowedCountryNames[11])
    #print g.getVariables(sourceCountry='HKG')
    #print g.getVariables(sourceCountry='HKG', searchText="alias:2012 Population Per Mill")
    #print g.lookUpReportsByCountry(countryName="Panama")
    #print g.createReport(
    #    out_file_path=tempfile.gettempdir(),
    #    studyAreas=Point(coord=[-117.1956, 34.0572], wkid=4326))
    #print g.createReport(out_file_path=tempfile.gettempdir(),
                         #report="networth",
                         #studyAreas=Polygon(rings=[[[-117.185412,34.063170],
                                                    #[-122.81,37.81],
                                                    #[-117.200570,34.057196],
                                                    #[-117.185412,34.063170]]], wkid=4326)
                         #)
    #print g.createReport(out_file_path=tempfile.gettempdir(),
                   #studyAreas=[{"address":{"text":"380 New York St. Redlands, CA 92373"}}],
                   #studyAreasOptions={"areaType":"RingBuffer","bufferUnits":"esriMiles","bufferRadii":[1,2,3]})
    #print g.dataCollections(outFields=None, addDerivativeVariables=None)
    #print g.dataCollections(outFields=None, addDerivativeVariables=None, countryName="Canada")
    #print g.dataCollections(outFields=None, addDerivativeVariables=None, suppressNullValues=True)
    #print g.standardGeographyQuery(sourceCountry="CA",
                             #geographyIDs=["35"],
                             #geographyLayers=["CAN.PR"])
    print g.standardGeographyQuery(sourceCountry="US",
                                   geographyIDs=["92129", "92126"],
                                   geographyLayers=["US.ZIP5"],
                                   returnGeometry=True,
                                   returnCentroids=True)
    #print g.standardGeographyQuery(sourceCountry="CA",
                                   #geographyIDs=["35"],
                                   #geographyLayers=["CAN.PR"],
                                   #returnGeometry=True)
    print 'fin'
