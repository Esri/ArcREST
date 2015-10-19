import agol
import ags
from security import *
from common import *
import _abstract
import web
import manageorg
import manageags
import manageportal
import hostedservice
#import webmap
from geometryservice import *
from enrichment import GeoEnrichment
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
__version__ = "3.0.0"