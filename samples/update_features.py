"""
   Update a feature service

   Python 2.x
   ArcREST 3.0.1
"""
from arcresthelper import securityhandlerhelper
from arcrest.agol import FeatureLayer
from arcrest.common.filters import LayerDefinitionFilter
import datetime
from datetime import timedelta
from arcrest.common.general import local_time_to_online,online_time_to_string

if __name__ == "__main__":
    url = ''# URL to Service
    sql = ''# where clause

    dt = local_time_to_online(datetime.datetime.now())

    fieldInfo =[
                {
                    'FieldName':'NAME',
                    'ValueToSet':'test'
                }
               ]

    proxy_port = None
    proxy_url = None

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = "" #User Name
    securityinfo['password'] = "" #password
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None

    shh = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
    if shh.valid == False:
        print shh.message
    else:
        fl= FeatureLayer(
            url=url,
            securityHandler=shh.securityhandler,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            initialize=True)

        out_fields = ['objectid']
        for fld in fieldInfo:
            out_fields.append(fld['FieldName'])

        resFeats = fl.query(where=sql,
                            out_fields=",".join(out_fields))
        for feat in resFeats:

            for fld in fieldInfo:
                feat.set_value(fld["FieldName"],fld['ValueToSet'])

        print fl.updateFeature(features=resFeats)