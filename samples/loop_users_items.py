"""
   This sample shows how to loop through all users and their
   items

   Python 2/3
   ArcREST version 3.5.x
"""
from __future__ import print_function
import arcrest
from arcrest.security import AGOLTokenSecurityHandler
from datetime import datetime as dt
import numpy as np

datetimeformat = '%m/%d/%Y %H:%M:%S'
createUsage = True # to filter views by date

# Start & end times to aggregate between
start = dt(2015, 7, 1)
end = dt(2015, 9, 1)
# Change period to different value (1w, 1m, etc.) for larger date ranges.
params = {
            "period": "1d",
            "groupby": "name",
            "vars": "num",
            "etype": "svcusg",
            "stype": "portal",
         }

if __name__ == "__main__":
    username = ""#Username
    password = ""#password
    proxy_port = None
    proxy_url = None

    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)


    admin = arcrest.manageorg.Administration(securityHandler=agolSH)
    content = admin.content
    portal = admin.portals.portalSelf
    commUsers = portal.users(start=1, num=100)
    commUsers = commUsers['users']

    for commUser in commUsers:
        user = admin.content.users.user(commUser.username)
        for userItem in user.items:

            msg = "Item: {0}".format(userItem.id)
            msg = msg +  "\n\tName: {0}".format(userItem.name)
            msg = msg +  "\n\tTitle: {0}".format(userItem.title)
            msg = msg +  "\n\tType: {0}".format(userItem.type)
            msg = msg +  "\n\tOwned by: {0}".format(commUser.username)
            msg = msg +  "\n\tCreated on: {0}".format(arcrest.general.online_time_to_string(userItem.created,datetimeformat))
            msg = msg +  "\n\tLast modified on: {0}".format(arcrest.general.online_time_to_string(userItem.modified,datetimeformat))
            msg = msg +  "\n\tTotal Views: {0}".format(userItem.numViews)

            if createUsage:
                params['name'] = userItem.id
                usage = portal.usage(start, end, **params)
                views = 0

                if usage.get('error', None) is None:
                    for data in usage.get('data', []):
                        # Views per period are returned as a list of lists
                        # Import to numpy for easy summing
                        arr = np.array(data['num'], dtype=np.uint64)
                        views = arr.sum(0)[1] # Sum "2nd column"
                        # Alternatively, without numpy
                        # views = sum(map(int, zip(*data['num'])[1]))
                else:
                    print(usage['error'])

                msg = msg +  "\n\tTimestamped Views: {0}".format(views)

            msg = msg +  "\n----------------------------------------------------------"
            print (msg)

