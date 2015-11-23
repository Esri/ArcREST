from __future__ import absolute_import
import six
if six.PY2:
    from .security import LDAPSecurityHandler, NTLMSecurityHandler, OAuthSecurityHandler, AGOLTokenSecurityHandler,\
         AGSTokenSecurityHandler, ArcGISTokenSecurityHandler, PKISecurityHandler, PortalServerSecurityHandler, \
         PortalTokenSecurityHandler
elif six.PY3:
    from .security3 import LDAPSecurityHandler, NTLMSecurityHandler, OAuthSecurityHandler, AGOLTokenSecurityHandler,\
         AGSTokenSecurityHandler, ArcGISTokenSecurityHandler, PKISecurityHandler, PortalServerSecurityHandler, \
         PortalTokenSecurityHandler

__version__ = "3.5.0"