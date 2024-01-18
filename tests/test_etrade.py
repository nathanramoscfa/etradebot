import unittest
import pandas as pd
import utils.mock_responses as mock_responses
from etrade.etrade import ETrade
from unittest.mock import patch, Mock


@patch('etrade.etrade.Authentication.etrade_login')
class TestETrade(unittest.TestCase):
    def test_get_account_list(self, mock_login):
        # Set up mock API response
        mock_login.return_value = (Mock(), Mock(), Mock())
        mock_login.return_value[0].list_accounts.return_value = mock_responses.mock_accounts_response

        # Create instance of ETrade class and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', {'cookie': 'value'}
        )
        accounts = etrade.get_account_list()

        # Check that the method returns the expected result
        expected_result = pd.DataFrame(
            mock_responses.mock_accounts_response['AccountListResponse']['Accounts']['Account']
        )
        expected_result.set_index('accountId', inplace=True)
        pd.testing.assert_frame_equal(accounts, expected_result)

    def test_get_account_balance(self, mock_login):
        # Set up mock API response
        mock_login.return_value = (Mock(), Mock(), Mock())
        mock_login.return_value[0].get_account_balance.return_value = mock_responses.mock_balance_response

        # Create instance of ETrade class and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', {'cookie': 'value'}
        )
        balance = etrade.get_account_balance('58315636')

        # Check that the method returns the expected result
        def flatten_dict(d):
            items = []
            for k, v in d.items():
                if isinstance(v, dict):
                    items.extend(flatten_dict(v).items())
                else:
                    items.append((k, v))
            return dict(items)

        flat_d = flatten_dict(mock_responses.mock_balance_response)
        expected_result = pd.DataFrame({'BalanceResponse': flat_d}).squeeze()
        expected_result = pd.to_numeric(expected_result, errors='ignore')
        pd.testing.assert_series_equal(balance, expected_result)

    def test_get_orders_list(self, mock_login):
        mock_orders = Mock()
        mock_orders.list_orders.return_value = mock_responses.mock_orders_list_response
        mock_accounts = Mock()
        mock_accounts.get_accounts.return_value = {'AccountListResponse': {'Accounts': {'Account': []}}}
        mock_market = Mock()
        mock_market.get_quote.return_value = {'QuoteResponse': {'QuoteData': {}}}
        mock_login.return_value = (mock_accounts, mock_orders, mock_market)

        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', {'cookie': 'value'}
        )

        with patch.object(etrade, 'orders', mock_orders):
            actual_df = etrade.get_orders_list('test_account')

        self.assertIsInstance(actual_df, pd.DataFrame)

    def test_get_market_quote(self, mock_login):
        # Set up mock API response
        market_mock = Mock()
        market_mock.get_quote.return_value = mock_responses.mock_quote_response
        mock_login.return_value = (Mock(), Mock(), market_mock)

        # Create instance of ETrade class and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', {'cookie': 'value'}
        )
        market = etrade.get_market_quote(symbols=['AAPL', 'GOOG'])

        # Assert that the returned value is a pandas dataframe
        self.assertIsInstance(market, pd.DataFrame)

        # Assert that the dataframe has the expected columns
        self.assertCountEqual(market.columns, ['AAPL', 'GOOG'])

    def test_get_buying_power(self, mock_login):
        # Set up mock API response
        mock_accounts = Mock()
        mock_accounts.get_account_balance.return_value = mock_responses.mock_balance_response
        mock_login.return_value = (mock_accounts, Mock(), Mock())

        # Create instance of ETrade class and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', {'cookie': 'value'}
        )
        buying_power = etrade.get_buying_power(account_id_key='12345', prints=False)

        # Check return value and mock API call
        assert isinstance(buying_power, float)
        mock_login.assert_called_once()

    def test_get_portfolio_data(self, mock_login):
        # Set up mock response
        mock_account = Mock()
        mock_account.get_account_portfolio.return_value = mock_responses.mock_get_portfolio_data
        mock_login.return_value = (mock_account, Mock(), Mock())

        # Create ETrade object and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username',
            'web_password', 'account_id', 'etrade_cookie'
        )
        portfolio_data = etrade.get_portfolio_data('account_id')

        # Verify expected results
        expected = ['positionType', 'quantity', 'costPerShare', 'marketValue', 'totalCost', 'daysGain', 'daysGainPct',
                    'totalGain', 'totalGainPct', 'pctOfPortfolio']
        self.assertEqual(portfolio_data.columns.tolist(), expected)
        self.assertEqual(portfolio_data.index.tolist(), ['FYX', 'VIOG'])
        self.assertEqual(portfolio_data.loc['FYX', 'quantity'], 11)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'costPerShare'], 86.9)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'marketValue'], 947.8171)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'totalCost'], 955.8999)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'daysGain'], 11.3871)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'daysGainPct'], 1.216)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'totalGain'], -8.0828)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'totalGainPct'], -0.8455)
        self.assertAlmostEqual(portfolio_data.loc['FYX', 'pctOfPortfolio'], 9.4585)
        self.assertEqual(portfolio_data.loc['VIOG', 'quantity'], 16)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'costPerShare'], 200.4115)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'marketValue'], 3176.5599)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'totalCost'], 3206.5849)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'daysGain'], 19.4704)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'daysGainPct'], 0.6167)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'totalGain'], -30.0249)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'totalGainPct'], -0.9363)
        self.assertAlmostEqual(portfolio_data.loc['VIOG', 'pctOfPortfolio'], 31.6997)


if __name__ == '__main__':
    unittest.main()
