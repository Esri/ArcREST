"""
This module contains system level constants that will carry throughout the
project.
"""
########################################################################
__version__ = "3.5.5"
"""
VERIFY_SSL_CERTIFICATES is a system level setting that allows for the by-pass of
less secure sites where the SSL certificates may be expired or invalid.
True means all SSL certificates must be valid
False means it will ignore all SSL invalid certificates (insecure)
"""
VERIFY_SSL_CERTIFICATES = False
"""
USER_AGENT identify the browser and operating system to the web server.
"""
USER_AGENT = "ArcREST/%s" % __version__
"""
DEFAULTTOKENEXPIRATION - is the timeout of the token in minutes
Default is 100 as an integer.
"""
DEFAULT_TOKEN_EXPIRATION = 100