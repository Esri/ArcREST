"""
   This sample shows assign credits to a list
   of users

"""
from __future__ import print_function
import arcrest

def main():
    username = ""
    password = ""
    proxy_url = ""
    proxy_port = ""
    org_url = ""
    sh = arcrest.AGOLTokenSecurityHandler(username=username,
                                          password=password,
                                          org_url=org_url,
                                          proxy_port=proxy_port,
                                          proxy_url=proxy_url)

    users = ["",""] # List of users
    credits = 2320 # number of credits to assign to users

    admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
    portalself = admin.portals.portalSelf
    return portalself.assignUserCredits(usernames=users,credits=credits)

if __name__ == "__main__":
    main()