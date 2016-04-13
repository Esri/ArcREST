from __future__ import absolute_import
from __future__ import print_function
from .._base import BaseServer
import json
from .parameters import ClusterProtocol
########################################################################
class Clusters(BaseServer):
    """
    This resource is a collection of all the clusters created within your
    site. The Create Cluster operation lets you define a new cluster
    configuration.

    Inputs:
       url - server cluster url
       connection - SiteConnection class
       initialize - boolean, false means so not load data, true means load
                    the class' information as creation.
    """
    _con = None
    _json_dict = None
    _json = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 connection,
                 initialize=False):
        """Constructor"""

        self._con = connection
        self._url = url
        if url.lower().endswith("/clusters"):
            self._url = url
        else:
            self._url = url + "/clusters"
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        if connection:
            json_dict = self._con.get(path_or_url=self._url,
                                      params=params)
        else:
            json_dict = self._con.get(path_or_url=self._url,
                                      params=params)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                setattr(self, k, json_dict[k])
            del k
            del v
    #----------------------------------------------------------------------
    def createCluster(self, clusterName, machineNames="", tcpClusterPort=""):
        """
        Creating a new cluster involves defining a clustering protocol that
        will be shared by all server machines participating in the cluster.
        All server machines that are added to the cluster must be
        registered with the site. The clustering protocol and the initial
        list of server machines are optional. In this case, the server
        picks the default clustering protocol and selects the port numbers
        such that they do not conflict with other configured ports on the
        server machine. Once a cluster has been created you can add more
        machines (to increase the compute power) or remove them (to reduce
        the compute power) dynamically.

        Inputs:
           clusterName - The name of the cluster. This must be a unique
                         name within a site
           machineNames - An optional comma-separated list of server
                          machines to be added to this cluster.
           tcpClusterPort - A TCP port number that will be used by all the
                            server machines to communicate with each other
                            when using the TCP clustering protocol. This is
                            the default clustering protocol. If this
                            parameter is missing, a suitable default will
                            be used.
        """
        url = self._url + "/create"
        params = {
            "f" : "json",
            "clusterName" : clusterName,
            "machineNames" : machineNames,
            "tcpClusterPort" : tcpClusterPort
        }
        return self._con.post(url=url,
                             postdata=params)
    #----------------------------------------------------------------------
    def getAvailableMachines(self):
        """
        This operation lists all the server machines that don't participate
        in any cluster and are available to be added to a cluster.
        The list would be empty if all registered server machines already
        participate in some cluster.
        """
        url = self._url + "/getAvailableMachines"
        params = {
            "f" : "json"
        }
        return self._con.get(path_or_url=url,
                            params=params)
########################################################################
class Cluster(BaseServer):
    """
    A Cluster is a group of server machines that host a collection of GIS
    services. Grouping server machines into a cluster allows you to treat
    them as a single unit to which you can publish GIS services.A cluster
    with more than one server machine provides a level of fault tolerance
    to the services. At the same time, having more than one machine
    increases the computing power of your cluster, hence increasing the
    overall throughput.
    A cluster is dynamic with respect to the list of server machines. New
    server machines can be added to increase computing power without
    affecting the already running GIS services. You can also remove
    machines from a cluster and re-assign them to another cluster.
    """
    _con = None
    _json_dict = None
    _json = None
    _proxy_url = None
    _proxy_port = None
    _url = None
    _securityHandler = None
    _clusterName = None
    _clusterProtocol = None
    _configuredState = None
    _machineNames = None
    _configurationState = None
    _clusters = None
    #----------------------------------------------------------------------
    def __init__(self, url, connection,
                 initialize=False):
        """Constructor"""
        self._con = connection
        self._url = url
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        if connection:
            json_dict = connection.get(path_or_url=self._url, params=params)
        else:
            json_dict = self._con.get(path_or_url=self._url,
                                      params=params)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                setattr(self, k,v)
            del k, v
    @property
    def clusters(self):
        """returns the cluster object for each server"""
        if self._clusters is None:
            self.__init()
            Cs = []
            for c in self._clusters:
                url = self._url + "/%s" % c['clusterName']
                Cs.append(Cluster(url=url,
                                  connection=self._con,
                                  initialize=True))
            self._clusters = Cs
        return self._clusters
    #----------------------------------------------------------------------
    def refresh(self):
        """refreshes the object's properties"""
        self.__init()
    #----------------------------------------------------------------------
    @property
    def clusterName(self):
        """returns the cluster name"""
        if self._clusterName is None:
            self.__init()
        return self._clusterName
    #----------------------------------------------------------------------
    @property
    def clusterProtocol(self):
        """returns the cluster's protocol parameters"""
        if self._clusterProtocol is None:
            self.__init()
        return self._clusterProtocol
    #----------------------------------------------------------------------
    @property
    def configuredState(self):
        """returns the current state of the cluster"""
        if self._configurationState is None:
            self.__init()
        return self._configuredState
    #----------------------------------------------------------------------
    @property
    def machineNames(self):
        """returns a list of machines in cluster"""
        if self._machineNames is None:
            self.__init()
        return self._machineNames
    #----------------------------------------------------------------------
    def start(self):
        """
        Starts the cluster.  Starting a cluster involves starting all the
        server machines within the cluster and the GIS services that are
        deployed to the cluster. This operation attempts to start all the
        server machines. If one or more of them cannot be reached, this
        operation reports an error.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/start"
        return self._con.post(url=url,
                              postdata=params)
    #----------------------------------------------------------------------
    def stop(self):
        """
        Stops a cluster. This also stops all the GIS services that are
        hosted on the cluster. This operation attempts to stop all the
        server machines within the cluster. If one or more machines cannot
        be reached, then this operation reports an error.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/stop"
        return self._con.post(url=url,
                             postdata=params)
    #----------------------------------------------------------------------
    def delete(self):
        """
        Deletes the cluster configuration. All the server machines in the
        cluster will be stopped and returned to the pool of registered
        machines. The GIS services that were deployed on the cluster are
        also stopped. Deleting a cluster does not delete your GIS services.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/delete"
        return self._con.post(url=url,
                             postdata=params)
    #----------------------------------------------------------------------
    def servicesInCluster(self):
        """
        This resource lists all the services that are currently deployed to
        the cluster (of machines). A service deployed to a cluster runs on
        every server machine that is participating in the cluster.

        This resource was added at ArcGIS 10.1 Service Pack 1.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/services"
        return self._con.post(url=url,
                             postdata=params)
    #----------------------------------------------------------------------
    def machinesInCluster(self):
        """
        This resource lists all the server machines that are currently
        participating in the cluster. Each server machine listing is
        accompanied by its status indicating whether the server machine is
        running or stopped.
        The list of server machines participating in a cluster is dynamic
        as machines can be added or removed.
        """
        url = self._url + "/machines"
        params = {
            "f" : "json"
        }
        return self._con.get(path_or_url=url,
                            params=params)
    #----------------------------------------------------------------------
    def addMachinesToCluster(self, machineNames):
        """
        Adds new server machines to the cluster. The server machines need
        to be registered with the site prior to this operation. When a
        server machine is added to the cluster, it pulls all the GIS
        services that were deployed to cluster and prepares to run them.

        Inputs:
           machineNames - A comma-separated list of machine names. The
           machines must be registered prior to completing this operation.
        """
        url = self._url + "/machines/add"
        params = {
            "f" : "json",
            "machineNames" : machineNames
        }
        return self._con.post(url=url,
                             postdata=params)
    #----------------------------------------------------------------------
    def removeMachinesFromCluster(self,
                                  machineNames):
        """
        Removes server machines from the cluster. The server machines are
        returned back to the pool of registered server machines.

        Inputs:
           machineNames - A comma-separated list of machine names. The
           machines must be registered prior to completing this operation.
        """
        url = self._url + "/machines/remove"
        params = {
            "f" : "json",
            "machineNames" : machineNames
        }
        return self._con.post(url=url,
                              postdata=params)
    #----------------------------------------------------------------------
    def editProtocol(self, clusterProtocolObj):
        """
        Updates the Cluster Protocol. This will cause the cluster to be
        restarted with updated protocol configuration.
        """
        if isinstance(clusterProtocolObj, ClusterProtocol):
            value = str(clusterProtocolObj.value['tcpClusterPort'])
        elif isinstance(clusterProtocolObj, dict):
            value = json.dumps(clusterProtocolObj)
        else:
            raise AttributeError("Invalid Input, must be a ClusterProtocal Object")
        url = self._url + "/editProtocol"
        params = {
            "f" : "json",
            "tcpClusterPort" : value
        }
        return self._con.post(url=url,
                              postdata=params)