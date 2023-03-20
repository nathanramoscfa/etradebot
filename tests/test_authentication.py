import unittest
from unittest.mock import patch
from selenium.common import NoSuchElementException
from authentication.authentication import Authentication


class TestAuthentication(unittest.TestCase):
    @patch('pyetrade.ETradeOAuth.get_verification_code')
    @patch('pyetrade.ETradeOAuth.get_access_token')
    def test_etrade_login_success(self, mock_get_access_token, mock_get_verification_code):
        # Set up test data
        consumer_key = 'test_consumer_key'
        consumer_secret = 'test_consumer_secret'
        web_username = 'test_web_username'
        web_password = 'test_web_password'
        account_id = 'test_account_id'
        etrade_cookie = {'test_cookie_key': 'test_cookie_value'}
        sandbox_key = 'test_sandbox_key'
        sandbox_secret = 'test_sandbox_secret'

        # Create an instance of the Authentication class
        auth = Authentication(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            web_username=web_username,
            web_password=web_password,
            account_id=account_id,
            etrade_cookie=etrade_cookie,
            sandbox_key=sandbox_key,
            sandbox_secret=sandbox_secret,
            dev=True,
            headless=True,
            browser='chrome',
            retries=3,
            sleep=30
        )

        # Set up mock responses
        mock_get_verification_code.return_value = 'test_verifier_code'
        mock_get_access_token.return_value = {
            'oauth_token': 'test_oauth_token',
            'oauth_token_secret': 'test_oauth_token_secret'
        }

        # Call the method being tested
        accounts, orders, market = auth.etrade_login()

        # Assert that the expected methods were called with the expected parameters
        mock_get_verification_code.assert_called_once_with(True, True, 'chrome')
        mock_get_access_token.assert_called_once_with('test_verifier_code')

        # Assert that the expected objects were returned
        self.assertIsNotNone(accounts)
        self.assertIsNotNone(orders)
        self.assertIsNotNone(market)

    @patch('pyetrade.ETradeOAuth.get_verification_code')
    def test_etrade_login_failure(self, mock_get_verification_code):
        # Set up test data
        consumer_key = 'test_consumer_key'
        consumer_secret = 'test_consumer_secret'
        web_username = 'test_web_username'
        web_password = 'test_web_password'
        account_id = 'test_account_id'
        etrade_cookie = {'test_cookie_key': 'test_cookie_value'}
        sandbox_key = 'test_sandbox_key'
        sandbox_secret = 'test_sandbox_secret'

        # Create an instance of the Authentication class
        auth = Authentication(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            web_username=web_username,
            web_password=web_password,
            account_id=account_id,
            etrade_cookie=etrade_cookie,
            sandbox_key=sandbox_key,
            sandbox_secret=sandbox_secret,
            dev=True,
            headless=True,
            browser='chrome',
            retries=3,
            sleep=0  # Set sleep to 0 to speed up the test
        )

        # Set up mock response to raise a NoSuchElementException
        mock_get_verification_code.side_effect = NoSuchElementException()

        # Call the method being tested
        with self.assertRaises(Exception):
            accounts, orders, market = auth.etrade_login()

        # Assert that the expected method was called twice with the expected parameters
        mock_get_verification_code.assert_has_calls([
            unittest.mock.call(True, True, 'chrome'),
            unittest.mock.call(True, True, 'edge')
        ])
