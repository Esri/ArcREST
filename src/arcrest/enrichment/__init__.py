"""
    The GeoEnrichment service provides the ability to get facts about a
    location or area. Using GeoEnrichment, you can get information about the
    people, places, and businesses in a specific area or within a certain
    distance or drive time from a location. More specifically, by submitting a
    point or polygon to the GeoEnrichment service, you can retrieve the
    demographics and other relevant characteristics associated with the
    surrounding area. You can also use the geoenrichment service to obtain
    additional geographic context (for example, the ZIP Code of a location) and
    geographic boundaries (for example, the geometry for a drive-time service
    area). Currently, the service is available for Canada, the United States,
    and a number of European countries. Other countries will be added in the
    near future.
    This service enables you to answer questions about locations that you can't
    answer with maps alone. For example: What kind of people live here? What do
    people like to do in this area? What are their habits and lifestyles? What
    kind of businesses are in this area?
    Site analysis is a popular application of this type of data enrichment. For
    example, the GeoEnrichment service can be leveraged to study the population
    that would be affected by the development of a new community center within
    their neighborhood. With the service, the proposed site can be submitted,
    and the demographics and other relevant characteristics associated with the
    area around the site will be returned.
"""
from __future__ import absolute_import
from ._geoenrichment import GeoEnrichment
__version__ = "3.5.8"