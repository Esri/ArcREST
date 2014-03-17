from agol import common

if __name__ == "__main__":
    #  Converts a feature class or table to a Feature Object. You can then
    #  use the Feature object to perform update or other operations 
    #  requiring a Feature object as an input.  This method is static so it
    #  does not require the Feature object to be created.  Just refer to 
    #  the common.Feature.fc_to_features(<dataset>)
    rows = common.Feature.fc_to_features(r"c:\temp\census\Data\NJ Tract.xls\'DE Tract$'")
    for row in rows:
        print row.asDictionary
        break
    features = common.Feature.fc_to_features(r"c:\temp\census\Data\sample.gdb\NYCounties")
    for feature in features:
        print feature.asDictionary
        break
    
    