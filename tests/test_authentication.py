import unittest
from unittest.mock import patch, MagicMock
from authentication.authentication import Authentication


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.consumer_key = 'test_consumer_key'
        self.consumer_secret = 'test_consumer_secret'
        self.web_username = 'test_username'
        self.web_password = 'test_password'
        self.account_id = 'test_account_id'
        self.etrade_cookie = {'cookie_key': 'cookie_value'}
        self.sandbox_key = 'test_sandbox_key'
        self.sandbox_secret = 'test_sandbox_secret'
        self.dev = True
        self.headless = True
        self.browser = 'chrome'
        self.retries = 3
        self.sleep = 30

        self.auth = Authentication(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            web_username=self.web_username,
            web_password=self.web_password,
            account_id=self.account_id,
            etrade_cookie=self.etrade_cookie,
            sandbox_key=self.sandbox_key,
            sandbox_secret=self.sandbox_secret,
            dev=self.dev,
            headless=self.headless,
            browser=self.browser,
            retries=self.retries,
            sleep=self.sleep
        )

    @patch('pyetrade.ETradeOAuth')
    def test_get_oauth(self, mock_oauth):
        mock_oauth_instance = MagicMock()
        mock_oauth.return_value = mock_oauth_instance

        oauth = self.auth.get_oauth()

        mock_oauth.assert_called_once_with(
            self.sandbox_key,
            self.sandbox_secret,
            self.web_username,
            self.web_password,
            self.etrade_cookie
        )
        self.assertEqual(oauth, mock_oauth_instance)

    @patch('pyetrade.ETradeOAuth')
    def test_get_access_tokens(self, mock_oauth_class):
        # Create a mock instance of ETradeOAuth
        mock_oauth_instance = MagicMock()
        mock_oauth_class.return_value = mock_oauth_instance

        # Set up the expected return value from get_access_token
        expected_tokens = {'token_key': 'token_value'}
        mock_oauth_instance.get_access_token.return_value = expected_tokens

        # Test data
        verifier_code = 'test_verifier_code'

        # Call the static method
        actual_tokens = Authentication.get_access_tokens(mock_oauth_instance, verifier_code)

        # Assertions to validate behavior
        mock_oauth_instance.get_access_token.assert_called_once_with(verifier_code)
        self.assertEqual(actual_tokens, expected_tokens)

    @patch('pyetrade.ETradeAccounts')
    def test_get_accounts_api(self, mock_accounts_api):
        mock_accounts_api_instance = MagicMock()
        mock_accounts_api.return_value = mock_accounts_api_instance

        # Mock tokens
        tokens = {'oauth_token': 'test_oauth_token', 'oauth_token_secret': 'test_oauth_token_secret'}

        accounts_api = self.auth.get_accounts_api(tokens)

        # Assertions to validate correct instantiation of ETradeAccounts
        mock_accounts_api.assert_called_once_with(
            self.sandbox_key,
            self.sandbox_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )
        self.assertEqual(accounts_api, mock_accounts_api_instance)

    @patch('pyetrade.ETradeOrder')
    def test_get_orders_api(self, mock_orders_api):
        mock_orders_api_instance = MagicMock()
        mock_orders_api.return_value = mock_orders_api_instance

        # Mock tokens
        tokens = {'oauth_token': 'test_oauth_token', 'oauth_token_secret': 'test_oauth_token_secret'}

        orders_api = self.auth.get_orders_api(tokens)

        # Assertions to validate correct instantiation of ETradeOrder
        mock_orders_api.assert_called_once_with(
            self.sandbox_key,
            self.sandbox_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )
        self.assertEqual(orders_api, mock_orders_api_instance)

    @patch('pyetrade.ETradeMarket')
    def test_get_market_api(self, mock_market_api):
        mock_market_api_instance = MagicMock()
        mock_market_api.return_value = mock_market_api_instance

        # Mock tokens
        tokens = {'oauth_token': 'test_oauth_token', 'oauth_token_secret': 'test_oauth_token_secret'}

        market_api = self.auth.get_market_api(tokens)

        # Assertions to validate correct instantiation of ETradeMarket
        mock_market_api.assert_called_once_with(
            self.sandbox_key,
            self.sandbox_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )
        self.assertEqual(market_api, mock_market_api_instance)


if __name__ == '__main__':
    unittest.main()
