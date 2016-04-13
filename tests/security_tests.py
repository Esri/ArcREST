# coding: utf-8
import unittest

from arcrest.security import OAuthSecurityHandler


class OAuthSecurityHandlerTests(unittest.TestCase):
    def test_get_token_with_invalid_client_id_should_not_return_valid_as_true(self):
        client_id = "invalid_client_id"
        secret_id = "invalid_secret"
        org_url = "https://www.arcgis.com"

        oauth_handler = OAuthSecurityHandler(client_id, secret_id, org_url)
        # Call .token to trigger token generation call
        self.assertIsNone(oauth_handler.token)
        self.assertNotEqual(True, oauth_handler.valid)

    def test_get_token_with_invalid_secret_id_should_not_return_valid_as_true(self):
        client_id = "IXlkCQ0nfEAKbZAP"
        secret_id = "invalid_secret"
        org_url = "https://www.arcgis.com"

        oauth_handler = OAuthSecurityHandler(client_id, secret_id, org_url)
        # Call .token to trigger token generation call
        self.assertIsNone(oauth_handler.token)
        self.assertNotEqual(True, oauth_handler.valid)
