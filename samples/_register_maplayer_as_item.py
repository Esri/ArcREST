
"""
   Updating a feature layer, OBJECTID must
   be included in the features.

"""
import json

from arcrest.agol import admin

if __name__ == "__main__":
    try:
        agol = admin.AGOL(username='',password='')
        inparams = {"url":"http://IPADDRESS/arcgis/rest/services/Sanitary_Sewer_Infrastructure/Sanitary_Sewer_Network/MapServer/6"}

        res = agol.addItem(name="SampleMapLayer",
                     tags="Test",
                     description="Test",
                     snippet="test",
                     data=None,
                     extent="-88.1799,41.7718,-88.1353,41.7823",
                     item_type="Feature Service",
                     folder=None,
                     inparams=inparams,
                     typeKeywords=["Data", "Service", "Feature Service", "ArcGIS Server", "Feature Access"]
                    )

        print res
    except ValueError, e:
        print e