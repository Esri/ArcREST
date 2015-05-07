from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureLayer

if __name__ == "__main__":
    username = "<username>"
    password = "<password>"
    url = "<URL to Feature Layer>"
    proxy_port = None
    proxy_url = None
    
    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)
    
    fl = FeatureLayer(
        url=url,
        securityHandler=agolSH,
        proxy_port=proxy_port,
        proxy_url=proxy_url,
        initialize=True)

    print fl.query(where="1=1",out_fields='*',returnGeometry=False) 
   