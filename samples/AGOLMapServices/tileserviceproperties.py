"""
   This sample will show the user the properties of a
   hosted map service (tiled service) on AGOL.
"""
import arcrest

if __name__ == "__main__":
    url = "https://<tile site>/arcgis/rest/admin"
    username = "<agol username>"
    password = "<agol password>"

    sh = arcrest.AGOLTokenSecurityHandler(username, password)
    agolServices = arcrest.hostedservice.Services(url, securityHandler=sh)
    for service in agolServices.services:
        if isinstance(service, arcrest.hostedservice.AdminMapService):
            print service.id
            print service.urlService
            print service.name