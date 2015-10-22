from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class Data(BaseAGSServer):
    """
       This resource provides information about the data holdings of the
       server. This information is used by ArcGIS for Desktop and other
       clients to validate data paths referenced by GIS services.
       You can register new data items with the server by using the
       Register Data Item operation. Use the Find Data Items operation to
       search through the hierarchy of data items.
       The Compute Ref Count operation counts and lists all references to a
       specific data item. This operation helps you determine if a
       particular data item can be safely deleted or refreshed.
    """
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - handles site security
        """
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
    #----------------------------------------------------------------------
    @property
    def datastoreConfiguration(self):
        """
           The data store configuration properties affect the behavior of
           the data holdings of the server. The properties include:
           blockDataCopy - When this property is false, or not set at all,
           copying data to the site when publishing services from a client
           application is allowed. This is the default behavior. When this
           property is true, the client application is not allowed to copy
           data to the site when publishing. Rather, the publisher is
           required to register data items through which the service being
           published can reference data. Values: true | false
        """
        params = {
            "f" : "json"
        }
        dURL = self._url + "/config"
        return self._do_get(url=dURL, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateDatastoreConfiguration(self, datastoreConfig={}):
        """
           This operation allows you to update the data store configuration
           You can use this to allow or block the automatic copying of data
           to the server at publish time
           Input:
              datastoreConfig - the JSON object containing the data
                                configuration
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "datastoreConfig" : datastoreConfig
        }
        url = self._url + "/config/update"
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def computeTotalRefCount(self, path):
        """
           Computes the total number of references to a given data item
           that exist on the server. You can use this operation to
           determine if a data resource can be safely deleted (or taken
           down for maintenance).
           Input:
              path - The complete hierarchical path to the item
           Output:
              JSON message as dictionary
        """
        cURL = self._url + "/computeTotalRefCount"
        params = {
            "f" : "json",
            "path" : path
        }
        return self._do_post(url=cURL,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def findDataItems(self, parentPath=None, ancestorPath=None,
                      type=None, id=None):
        """
           You can use this operation to search through the various data
           items registered in the server's data store.
           Inputs:
              parentPath - The path of the parent under which to find items
              ancestorPath - The path of the ancestor under which to find
                             items.
              type - A filter for the type of the items
              id - A filter to search by the ID of the item
           Output:
              dictionary
        """
        params = {
            "f" : "json",
        }
        if parentPath is not None:
            params['parentPath'] = parentPath
        if ancestorPath is not None:
            params['ancestorPath'] = ancestorPath
        if type is not None:
            params['type'] = type
        if id is not None:
            params['id'] = id
        fURL = self._url + "/findItems"
        return self._do_post(url=fURL, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def registerDataItem(self, item):
        """
           Registers a new data item with the server's data store.
           Input
              item - The JSON representing the data item.
                     See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r3000001s9000000
           Output:
              dictionary
        """
        params = {
            "item" : item,
            "f" : "json"
        }
        rURL = self._url + "/registerItem"
        return self._do_post(url=rURL, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def rootDataItems(self):
        """ This resource lists data items that are the root of all other
            data items in the data store.
        """
        url = self._url + "/items"
        params = {
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def validateAllDataItems(self):
        """ validates all the items in the datastore """
        params = {
        "f" : "json"}
        url = self._url + "/validateAllDataItems"
        return self._do_post(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def validateDataItem(self, item):
        """
           In order for a data item to be registered and used successfully
           within the server's data store, you need to make sure that the
           path (for file shares) or connection string (for databases) is
           accessible to every server node in the site. This can be done by
           invoking the Validate Data Item operation on the JSON object
           representing the data store.
           Validating a data item does not automatically register it for
           you. You need to explicitly register your data item by invoking
           the Register Data Item operation.
           Input:
              item - The JSON representing the data item.
           Output:
              dictionary
        """
        params = {
            "f" : "json",
            "item" : item
        }
        url = self._url + "/validateDataItem"
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def makePrimary(self, dataStoreName, machineName):
        """
        Promotes a standby machine to the primary Data Store machine. The
        existing primary machine is downgraded to a standby machine.

        """
        url = self._url + "/items/enterpriseDatabases/%s/machines/%s/makePrimary" % (dataStoreName, machineName)
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeDataStoreMachine(self, dataStoreItemName, machineName):
        """
        Removes a standby machine from the Data Store. This operation is
        not supported on the primary Data Store machine.

        Inputs:
           dataStoreItemName - name of the data store item
           machineName - name of the machine to remove
        """
        url = self._url + "/items/enterpriseDatabases/%s/machines/%s/remove" % (dataStoreItemName, machineName)
        params = {
            "f" : "json"
        }
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def startDataStoreMachine(self, dataStoreItemName, machineName):
        """
        Starts the database instance running on the Data Store machine.

        Inputs:
           dataStoreItemName - name of the item to start
           machineName - name of the machine to start on
        """
        url = self._url + "/items/enterpriseDatabases/%s/machines/%s/start" % (dataStoreItemName, machineName)
        params = {
            "f": "json"
        }
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def stopDataStoreMachine(self, dataStoreItemName, machineName):
        """
        Stop the database instance running on the Data Store machine.

        Inputs:
           dataStoreItemName - name of the item to stop
           machineName - name of the machine to stop on
        """
        url = self._url + "/items/enterpriseDatabases/%s/machines/%s/stop" % (dataStoreItemName, machineName)
        params = {
            "f": "json"
        }
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def unregisterDataItem(self, path):
        """
        Unregisters a data item that has been previously registered with
        the server's data store.

        Inputs:
           path - path to share folder

        Example:
           path = r"/fileShares/folder_share"
           print data.unregisterDataItem(path)
        """
        url = self._url + "/unregisterItem"
        params = {
            "f" : "json",
            "itempath" : path
        }
        return self._do_post(url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def validateDataStore(self, dataStoreName, machineName):
        """
        Checks the status of ArcGIS Data Store and provides a health check
        response.

        Inputs:
           dataStoreName - name of the datastore
           machineName - name of the machine
        """
        url = self._url + "/items/enterpriseDatabases/%s/machines/%s/validate" % (dataStoreName, machineName)
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
