"""
Contains constants to determine if an item type has a file or not to help
tasks related to moving, updating or managing one's content on Portal or
ArcGIS Online.
"""
from __future__ import absolute_import
from __future__ import print_function
URL_BASED_ITEM_TYPES = ('Feature Service', 'Map Service',
                        'Image Service', 'Web Mapping Application','WMS','WMTS', 'Geodata Service',
                        'Globe Service','Geometry Service', 'Geocoding Service',
                        'Network Analysis Service', 'Geoprocessing Service','Mobile Application')

TEXT_BASED_ITEM_TYPES = ('Web Map', 'Feature Service', 'Map Service',
                         'Image Service', 'Feature Collection', 'Feature Collection Template',
                         'Web Mapping Application', 'Mobile Application', 'Symbol Set', 'Color Set',
                         'Windows Viewer Configuration')

FILE_BASED_ITEM_TYPES = ('Code Attachment', 'Shapefile', 'CSV',
                         'Service Definition', 'Map Document', 'Map Package', 'Tile Package',
                         'Explorer Map', 'Globe Document', 'Scene Document', 'Published Map',
                         'Map Template', 'Windows Mobile Package', 'Layer', 'Layer Package',
                         'Explorer Layer', 'Geoprocessing Package', 'Geoprocessing Sample',
                         'Locator Package', 'Workflow Manager Package', 'Code Sample',
                         'Desktop Application Template', 'Desktop Add In', 'Explorer Add In',
                         'CityEngine Web Scene', 'Windows Viewer Add In')

RELATIONSHIP_TYPES = ('Map2Service', 'WMA2Code',
                      'Map2FeatureCollection', 'MobileApp2Code', 'Service2Data',
                      'Service2Service')

RELATIONSHIP_DIRECTIONS = ('forward', 'reverse')

URL_ITEM_FILTER = ' OR '.join(['type:"%s"' % t for t in URL_BASED_ITEM_TYPES]) \
    + ' -type:"Web Map" -type:"Map Package"'

WEB_ITEM_FILTER = '((type:"service" -type:"globe" -type:"geodata") OR ' \
    + 'type:"KML" OR type:"WMS" OR type:"Web Map" OR ' \
    + 'type:"web mapping application" OR (type:"feature collection" ' \
    + '-type:"Feature Collection Template") OR ' \
    + 'type:"mobile application")'
WEBMAP_ITEM_FILTER = 'type:"Web Map" -type:"Web Mapping Application"'
EXCLUDE_BASEMAP_FILTER = ' -tags:basemap'
