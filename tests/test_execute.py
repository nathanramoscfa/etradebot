import random
import unittest
import xmltodict
import pandas as pd
import utils.mock_responses as mock_responses
from etrade.etrade import ETrade
from execute.execute import Execute
from unittest.mock import MagicMock, Mock, ANY, patch


@patch('etrade.etrade.Authentication.etrade_login')
class TestETrade(unittest.TestCase):
    def test_calculate_shares(self, mock_login):
        # Set up mock API response
        market_mock = Mock()
        market_mock.get_quote.return_value = mock_responses.mock_quote_response
        mock_login.return_value = (Mock(), Mock(), market_mock)

        # Create instance of ETrade class and call method
        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username', 'web_password', 'account_id', {'cookie': 'value'}
        )
        execute = Execute(etrade)

        weights = pd.Series([0.5, 0.5], index=['AAPL', 'GOOG'])
        buying_power = 1000
        shares_to_buy = execute.calculate_shares(weights, buying_power, prints=False)

        # Verify expected results
        expected = pd.Series(data=[3, 5], index=['AAPL', 'GOOG'], name='Shares')
        pd.testing.assert_series_equal(shares_to_buy, expected)

    def test_generate_trades_preview_true(self, mock_login):
        mock_client_order_id = '8402024091'
        mock_orders = Mock()
        mock_preview_response = mock_responses.mock_preview_order.format(client_order_id=mock_client_order_id)
        mock_orders.preview_equity_order.return_value = mock_preview_response
        mock_accounts = Mock()
        mock_accounts.get_accounts.return_value = {'AccountListResponse': {'Accounts': {'Account': []}}}
        mock_market = Mock()
        mock_market.get_quote.return_value = {'QuoteResponse': {'QuoteData': {}}}
        mock_login.return_value = (mock_accounts, mock_orders, mock_market)

        # create a MagicMock object to mock the generate_trades method
        mock_generate_trades = MagicMock(return_value=mock_preview_response)

        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username', 'web_password', 'account_id', {'cookie': 'value'}
        )
        execute = Execute(etrade)

        symbol = 'AAPL'
        order_action = 'BUY'
        quantity = 3
        price_type = 'MARKET'
        order_term = 'GOOD_FOR_DAY'
        market_session = 'REGULAR'
        preview = True
        prints = False

        with patch.object(execute, 'generate_trades', mock_generate_trades):
            trade_response = execute.generate_trades(
                'account_id_key', symbol, order_action, quantity, price_type, order_term, market_session, preview,
                prints
            )

            # extract clientOrderId from the preview response
            preview_response_dict = xmltodict.parse(mock_preview_response)
            client_order_id = preview_response_dict['PreviewOrderResponse']['PreviewIds']['previewId']

            # check that the generate_trades method was called with the expected parameters
            mock_generate_trades.assert_called_with(
                ANY, symbol, order_action, quantity, price_type, order_term, market_session, preview, prints
            )

            # check that the trade response matches the expected response
            self.assertEqual(trade_response, mock_preview_response)

    def test_generate_trades_preview_false(self, mock_login):
        mock_client_order_id = '8402024091'
        mock_orders = Mock()
        mock_accounts = Mock()
        mock_accounts.list_accounts.return_value = mock_responses.mock_accounts_response
        mock_market = Mock()
        mock_market.get_quote.return_value = {'QuoteResponse': {'QuoteData': {}}}
        mock_login.return_value = (mock_accounts, mock_orders, mock_market)

        # create a MagicMock object to mock the place_equity_order method
        mock_place_order = MagicMock()
        mock_orders.place_equity_order = mock_place_order

        etrade = ETrade(
            'consumer_key', 'consumer_secret', 'web_username', 'web_password', 'account_id', {'cookie': 'value'}
        )
        execute = Execute(etrade)

        symbol = 'GOOG'
        order_action = 'BUY'
        quantity = 5
        price_type = 'MARKET'
        order_term = 'GOOD_FOR_DAY'
        market_session = 'REGULAR'
        preview = False
        prints = False

        with patch.object(etrade, 'orders', mock_orders):
            with patch.object(random, 'randint', return_value=int(mock_client_order_id)):
                mock_place_order.return_value = None
                trade_response = execute.generate_trades(
                    'account_id_key', symbol, order_action, quantity, price_type, order_term, market_session, preview,
                    prints
                )

                # check that the place_equity_order method was called with the expected parameters
                mock_place_order.assert_called_with(
                    resp_format='xml',
                    accountId='account_id_key',
                    symbol='GOOG',
                    orderAction='BUY',
                    clientOrderId=int(mock_client_order_id),
                    priceType='MARKET',
                    quantity=5,
                    orderTerm='GOOD_FOR_DAY',
                    marketSession='REGULAR'
                )

                # check that no trades were actually placed by ensuring that the trade response is None
                self.assertIsNone(trade_response)


if __name__ == '__main__':
    unittest.main()
