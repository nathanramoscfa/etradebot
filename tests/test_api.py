import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from api.api import DataAPI


class TestDataAPI(unittest.TestCase):

    def setUp(self):
        if hasattr(self, 'bloomberg_test'):
            self.symbols = ['AAPL US Equity', 'MSFT US Equity']
            self.api_source = 'bloomberg'
        else:
            self.symbols = ['AAPL', 'MSFT']
            self.api_source = 'yahoo'
        self.start_date = '01-01-2020'
        self.end_date = '12-31-2020'
        self.data_api = DataAPI(
            symbols=self.symbols, start_date=self.start_date, end_date=self.end_date, api_source=self.api_source
        )

    def test_init_with_yahoo_source(self):
        symbols = ['AAPL', 'MSFT']
        data_api = DataAPI(symbols, api_source='yahoo')

        self.assertEqual(data_api.symbols, symbols)
        self.assertEqual(data_api.api_source, 'yahoo')

    @patch('tia.bbg.datamgr.BbgDataManager')
    def test_init_with_bloomberg_source(self, mock_bbg):
        symbols = ['AAPL', 'MSFT']
        data_api = DataAPI(symbols, api_source='bloomberg')

        mock_bbg.assert_called_once()

    def test_init_with_invalid_source(self):
        symbols = ['AAPL', 'MSFT']
        with self.assertRaises(ValueError):
            DataAPI(symbols, api_source='invalid_source')

    def test_process_symbols_yahoo(self):
        symbols = ['AAPL', 'MSFT US Equity']
        processed_symbols = DataAPI.process_symbols(symbols, 'yahoo')

        self.assertEqual(processed_symbols, ['AAPL', 'MSFT'])

    def test_process_symbols_bloomberg(self):
        symbols = ['AAPL', 'MSFT']
        processed_symbols = DataAPI.process_symbols(symbols, 'bloomberg')

        self.assertEqual(processed_symbols, ['AAPL US Equity', 'MSFT US Equity'])

    def test_process_symbols_invalid_source(self):
        symbols = ['AAPL', 'MSFT']
        with self.assertRaises(ValueError):
            DataAPI.process_symbols(symbols, 'invalid_source')

    def test_check_valid_api_source_with_valid_sources(self):
        valid_sources = ['yahoo', 'bloomberg']
        for source in valid_sources:
            with self.subTest(api_source=source):
                data_api = DataAPI(['AAPL'], api_source=source)
                try:
                    data_api.check_valid_api_source()
                except ValueError:
                    self.fail(f"check_valid_api_source() raised ValueError unexpectedly with '{source}'")

    def test_check_valid_api_source_with_invalid_source(self):
        with self.assertRaises(ValueError) as cm:
            DataAPI(['AAPL'], api_source='invalid_source')
        self.assertEqual(str(cm.exception), "Invalid API source: invalid_source")

    @patch('yahooquery.Ticker')
    def test_get_yahoo_prices(self, mock_ticker):
        # Mock the DataFrame returned by yahooquery
        mock_prices_data = pd.DataFrame({
            'adjclose': [100, 200, 150, 250],
            'symbol': ['AAPL', 'AAPL', 'MSFT', 'MSFT'],
            'date': pd.date_range(start='01-01-2020', periods=4)
        }).set_index(['date', 'symbol'])

        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        mock_ticker_instance.history.return_value = {'adjclose': mock_prices_data}

        prices = self.data_api.get_yahoo_prices()

        # Assertions
        mock_ticker.assert_called_once_with(self.symbols)
        mock_ticker_instance.history.assert_called_once()
        self.assertIsInstance(prices, pd.DataFrame)
        self.assertEqual(len(prices.columns), len(self.symbols))  # Check if columns match the symbols


if __name__ == '__main__':
    unittest.main()
