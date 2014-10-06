"""

    Simple sample that lists all layers in a given hosted feature service

"""
import arcrest

if __name__ == "__main__":
    url = "https://<url to spatial data store>/ArcGIS/rest/admin"
    username = "<user name>"
    password = "<password> "
    sh = arcrest.AGOLTokenSecurityHandler(username, password)
    agolServices = arcrest.hostedservice.Services(url, securityHandler=sh)
    for service in agolServices.services:
        for lyr in service.layers:
            print lyr.name, lyr._url