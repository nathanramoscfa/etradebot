import unittest
import pandas as pd
import yahooquery as yq
from unittest.mock import patch, Mock
from unittest import mock
from api.api import DataAPI
import utils.mock_data as mock_data


class TestDataAPI(unittest.TestCase):

    def test_init_defaults(self):
        api = DataAPI(symbols=['AAPL'])
        self.assertEqual(api.symbols, ['AAPL'])
        self.assertEqual(api.api_source, 'yahoo')
        self.assertEqual(api.market_symbol, 'SPY')

    def test_init_with_params(self):
        api = DataAPI(symbols=['AAPL'], api_source='bloomberg', market_symbol='MSFT')
        self.assertEqual(api.symbols, ['AAPL US Equity'])
        self.assertEqual(api.api_source, 'bloomberg')
        self.assertEqual(api.market_symbol, 'MSFT US Equity')

    def test_process_symbols_for_yahoo(self):
        api = DataAPI(symbols=['AAPL US Equity'])
        processed_symbols = api.process_symbols(api.symbols, 'yahoo')
        self.assertEqual(processed_symbols, ['AAPL'])

    def test_process_symbols_for_bloomberg(self):
        api = DataAPI(symbols=['AAPL'], api_source='bloomberg')
        processed_symbols = api.process_symbols(api.symbols, 'bloomberg')
        self.assertEqual(processed_symbols, ['AAPL US Equity'])

    def test_invalid_api_source(self):
        with self.assertRaises(ValueError):
            DataAPI(symbols=['AAPL'], api_source='invalid')

    @patch.object(yq, 'Ticker', autospec=True)
    def mock_yq_Ticker(self, *args, **kwargs):
        return mock.MagicMock(history=mock.MagicMock(return_value=mock_data.get_mock_yahoo_price_history()))


if __name__ == '__main__':
    unittest.main()
