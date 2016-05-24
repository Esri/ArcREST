from __future__ import absolute_import
from ._geoprocessing import GPJob, GPService, GPTask
from ._gpobjects import GPBoolean, GPDataFile, GPDate
from ._gpobjects import GPDouble, GPFeatureRecordSetLayer, GPLinearUnit
from ._gpobjects import GPLong, GPMultiValue, GPRasterData
from ._gpobjects import GPRasterDataLayer, GPRecordSet, GPString

__version__ = "5.0.0"

__all__ = ['GPJob', 'GPService', 'GPTask',
           'GPBoolean', 'GPDataFile', 'GPDate',
           'GPDouble', 'GPFeatureRecordSetLayer', 'GPLinearUnit',
           'GPLong', 'GPMultiValue', 'GPRasterData',
           'GPRasterDataLayer', 'GPRecordSet', 'GPString']
