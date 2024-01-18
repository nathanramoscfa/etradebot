# import unittest
# from utils import mock_responses
# import pandas as pd
# import numpy as np
# from unittest import mock
# from model.model import Model
#
#
# class TestModel(unittest.TestCase):
#
#     def setUp(self):
#         self.symbols = ['AAPL', 'GOOG', 'AMZN']
#         self.model = Model(self.symbols)
#
#     def test_process_symbols_yahoo(self):
#         processed_symbols = self.model.process_symbols(self.symbols, api_source='yahoo')
#         expected_symbols = ['AAPL', 'GOOG', 'AMZN']
#         self.assertListEqual(processed_symbols, expected_symbols)
#
#     def test_process_symbols_bloomberg(self):
#         processed_symbols = self.model.process_symbols(self.symbols, api_source='bloomberg')
#         expected_symbols = ['AAPL US Equity', 'GOOG US Equity', 'AMZN US Equity']
#         self.assertListEqual(processed_symbols, expected_symbols)
#
#     def test_invalid_api_source(self):
#         with self.assertRaises(ValueError):
#             Model(self.symbols)
#
#     def test_get_historical_prices_yahoo(self):
#         with mock.patch('model.model.Model.get_historical_prices') as mock_history:
#             # Set up mock API response
#             index = ['2022-01-01', '2022-01-02']
#             columns = ['AAPL', 'GOOG']
#             data = np.array([[100.0, 200.0], [300.0, 400.0]])
#             prices = pd.DataFrame(data=data, index=index, columns=columns)
#             mock_history.return_value = prices
#
#             # Create a Model object and call get_historical_prices
#             model = Model(['AAPL', 'GOOG'])
#             result = model.get_historical_prices()
#
#             # Convert the index of the result dataframe to a DatetimeIndex with the same frequency as the
#             # expected_prices dataframe
#             result.index = pd.date_range(start='2022-01-01', periods=result.shape[0], freq='D')
#
#             # Check that the result is equal to the expected DataFrame
#             expected_index = pd.date_range(start='2022-01-01', periods=2)
#             expected_data = np.array([[100.0, 200.0], [300.0, 400.0]])
#             expected_prices = pd.DataFrame(data=expected_data, index=expected_index, columns=['AAPL', 'GOOG'])
#             pd.testing.assert_frame_equal(result, expected_prices)
#
#     def test_get_historical_prices_bloomberg(self):
#         with mock.patch('model.model.Model.get_historical_prices') as mock_history:
#             # Set up mock API response
#             index = ['2022-01-01', '2022-01-02']
#             columns = ['AAPL US Equity', 'GOOG US Equity']
#             data = np.array([[100.0, 200.0], [300.0, 400.0]])
#             prices = pd.DataFrame(data=data, index=index, columns=columns)
#             mock_history.return_value = prices
#
#             # Create a Model object and call get_historical_prices
#             model = Model(['AAPL', 'GOOG'])
#             result = model.get_historical_prices()
#
#             # Convert the index of the result dataframe to a DatetimeIndex with the same frequency as the
#             # expected_prices dataframe
#             result.index = pd.date_range(start='2022-01-01', periods=result.shape[0], freq='D')
#
#             # Check that the result is equal to the expected DataFrame
#             expected_index = pd.date_range(start='2022-01-01', periods=2)
#             expected_data = np.array([[100.0, 200.0], [300.0, 400.0]])
#             expected_prices = pd.DataFrame(data=expected_data, index=expected_index,
#                                            columns=['AAPL US Equity', 'GOOG US Equity'])
#             pd.testing.assert_frame_equal(result, expected_prices)
#
#     def test_get_risk_free_rate_yahoo(self):
#         with mock.patch('model.model.yq.Ticker') as mock_ticker:
#             # Set up mock API response
#             mock_ticker().price.__getitem__.return_value = {'regularMarketPrice': 1.23}
#
#             # Create a Model object and call get_risk_free_rate
#             model = Model(['AAPL'])
#             result = model.get_risk_free_rate()
#
#             # Check that the result is equal to the expected value
#             self.assertEqual(result, 0.0123)
#
#     @mock.patch('tia.bbg.datamgr.BbgDataManager')
#     def test_get_risk_free_rate_bloomberg(self, mock_bbg):
#         mock_mgr = mock_bbg.return_value
#         mock_mgr['USGG10YR Index'].PX_LAST = 4.0
#
#         model = Model(symbols=['AAPL'])
#         result = model.get_risk_free_rate()
#
#         self.assertEqual(result, 0.04)
#
#     @mock.patch('model.model.yq.Ticker')
#     def test_get_market_caps_yahoo(self, mock_ticker):
#         model = Model(['QQQ', 'VIOG', 'PSCD', 'SPSM', 'FYX'])
#         for symbol, summary_detail in mock_responses.mock_summary_detail.items():
#             mock_yq_symbol = mock.MagicMock()
#             mock_yq_symbol.summary_detail = {symbol: summary_detail}
#             mock_ticker.return_value = mock_yq_symbol
#             break  # Just use the first item for now
#         actual_market_caps = model.get_market_caps()
#         expected_market_caps = pd.Series([mock_responses.mock_market_caps['QQQ'] / 1_000_000], index=['QQQ'])
#         if not isinstance(actual_market_caps, pd.Series):
#             actual_market_caps = pd.Series([actual_market_caps], index=[model.symbols[0]])
#         pd.testing.assert_series_equal(actual_market_caps, expected_market_caps)
#
#     def test_get_market_caps_bloomberg(self):
#         with mock.patch('model.model.dm.BbgDataManager') as MockDataManager:
#             MockCUR_MKT_CAP = mock.MagicMock()
#             MockCUR_MKT_CAP.to_dict.return_value = {'AAPL': 1000000000, 'MSFT': 2000000000}
#
#             MockDataManager.return_value.__getitem__.return_value = mock.MagicMock(CUR_MKT_CAP=MockCUR_MKT_CAP)
#
#             m = Model(symbols=['AAPL US Equity', 'MSFT US Equity'])
#             market_cap = m.get_market_caps()
#             expected = pd.Series({'AAPL': 1000.0, 'MSFT': 2000.0})
#             pd.testing.assert_series_equal(market_cap, expected)
#
#     def test_vif_filter(self):
#         vif_symbols = Model.vif_filter(mock_responses.mock_prices, mock_responses.mock_market_caps, threshold=100)
#         self.assertEqual(set(vif_symbols), {'VIOG', 'PSCD', 'SPSM', 'FYX'})
#
#         vif_symbols = Model.vif_filter(mock_responses.mock_prices, mock_responses.mock_market_caps, threshold=25)
#         self.assertEqual(set(vif_symbols), {'VIOG', 'PSCD', 'SPSM'})
#
#         vif_symbols = Model.vif_filter(mock_responses.mock_prices, mock_responses.mock_market_caps, threshold=1)
#         self.assertEqual(set(vif_symbols), {'PSCD', 'SPSM'})
#
#     def test_calculate_covariance_matrix(self):
#         covariance_matrix = Model.calculate_covariance_matrix(
#             mock_responses.mock_prices, mock_responses.mock_prices.columns
#         )
#         self.assertIsInstance(covariance_matrix, pd.DataFrame)
#         self.assertEqual(covariance_matrix.shape, (5, 5))
#
#
# if __name__ == '__main__':
#     unittest.main()
