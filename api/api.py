import pandas as pd
import yahooquery as yq
from tqdm import tqdm
from datetime import datetime, timedelta


class DataAPI(object):
    """
    :description: Class for data api management.

    :param symbols: List of symbols
    :type symbols: list
    :param num_years: Number of years to look back, default is 100
    :type num_years: int, optional
    :param period: Period, default is 'None'. Choices include: '1d', '5d', '7d', '60d', '1mo', '3mo', '6mo', '1y', '2y',
                                                               '5y', '10y', 'ytd', 'max'
    :type period: str, optional
    :param api_source: API source, default is yahoo, other option is bloomberg
    :type api_source: str, optional
    :param market_symbol: Market symbol, default is SPY
    :type market_symbol: str, optional
    :param start_date: Start date, default is None
    :type start_date: str, optional
    :param end_date: End date, default is None
    :type end_date: str, optional
    """
    def __init__(
            self,
            symbols,
            num_years=100,
            period=None,
            api_source='yahoo',
            market_symbol='SPY',
            start_date=None,
            end_date=None
    ):
        self.symbols = symbols
        self.num_years = num_years
        self.period = period
        self.api_source = api_source
        self.market_symbol = market_symbol
        self.start_date = start_date
        self.end_date = end_date

        if self.api_source == 'bloomberg':
            try:
                import tia.bbg.datamgr as dm
                self.mgr = dm.BbgDataManager()
            except ImportError:
                raise ImportError("Please install Bloomberg Python API to use Bloomberg as the data source.")
        elif self.api_source not in ['yahoo']:
            raise ValueError(f"Invalid API source: {self.api_source}")

        self.symbols = self.process_symbols(self.symbols, self.api_source)
        self.market_symbol = self.process_symbols([self.market_symbol], self.api_source)[0]

        if self.start_date is None:
            self.start_date = (datetime.today() - timedelta(days=int(365.25 * self.num_years))).strftime('%m-%d-%Y')
        if self.end_date is None:
            self.end_date = datetime.today().strftime('%m-%d-%Y')

    @staticmethod
    def process_symbols(symbols, api_source):
        """
        :description: Process symbols based on the API source.
                      Bloomberg symbols usually end with ' US Equity',
                      whereas Yahoo symbols do not.

        :param symbols: List of symbols
        :type symbols: list
        :param api_source: API source, either 'yahoo' or 'bloomberg'
        :type api_source: str
        :return: Processed symbols
        """
        # Check for a valid API source
        if api_source not in ['yahoo', 'bloomberg']:
            raise ValueError(f"Invalid API source: {api_source}")

        # Append ' US Equity' for Bloomberg symbols, if not already present
        if api_source == 'bloomberg':
            symbols = [
                symbol if symbol.endswith(' US Equity') else symbol + ' US Equity'
                for symbol in symbols
            ]

        # Remove ' US Equity' for Yahoo symbols, if present
        elif api_source == 'yahoo':
            symbols = [
                symbol[:-len(' US Equity')] if symbol.endswith(' US Equity') else symbol
                for symbol in symbols
            ]

        return symbols

    def check_valid_api_source(self):
        """
        :description: Check for a valid API source.

        :return: None
        """
        if self.api_source not in ['yahoo', 'bloomberg']:
            raise ValueError(f"Invalid API source: {self.api_source}")

    def get_yahoo_prices(self):
        """
        :description: Get historical prices from Yahoo Finance

        :return: Historical prices
        :rtype: pandas.DataFrame
        """
        if self.period is None:
            start_date_obj = datetime.strptime(self.start_date, '%m-%d-%Y')
            end_date_obj = datetime.strptime(self.end_date, '%m-%d-%Y')
            start_date_formatted = datetime.strftime(start_date_obj, '%Y-%m-%d')
            end_date_formatted = datetime.strftime(end_date_obj, '%Y-%m-%d')
            try:
                prices = yq.Ticker(self.symbols).history(
                    start=start_date_formatted, end=end_date_formatted
                )['adjclose']
            except OverflowError:
                prices = yq.Ticker(self.symbols).history(period='max')['adjclose']
        else:
            prices = yq.Ticker(self.symbols).history(self.period)['adjclose']
        prices = prices.unstack(level='symbol').dropna()
        prices.index = pd.to_datetime(prices.index).date
        return prices

    def get_bloomberg_prices(self):
        """
        :description: Get historical prices from Bloomberg

        :return: Historical prices
        :rtype: pandas.DataFrame
        """
        prices = self.mgr[self.symbols].get_historical('PX_LAST', start=self.start_date, end=self.end_date).dropna()
        prices.columns = [col.replace(' US Equity', '') for col in prices.columns]
        return prices

    def get_historical_prices(self):
        """
        :description: Get historical prices

        :return: Historical prices
        :rtype: pandas.DataFrame
        """
        self.check_valid_api_source()

        if self.api_source == 'yahoo':
            return self.get_yahoo_prices()
        elif self.api_source == 'bloomberg':
            return self.get_bloomberg_prices()

    @staticmethod
    def get_yahoo_risk_free_rate(symbol, percent=100, decimals=4):
        """
        :description: Get risk-free rate from Yahoo Finance

        :param symbol: Ticker, default is None
        :type symbol: str, optional
        :param percent: Percent, default is 100
        :param decimals: Decimals, default is 4
        :return: Risk free rate
        :rtype: float
        """
        if symbol is None:
            risk_free_rate = round(
                yq.Ticker('^TNX').price['^TNX']['regularMarketPrice'] / percent, decimals)
        else:
            ticker = yq.Ticker(symbol)
            risk_free_rate = round(ticker.price[symbol]['regularMarketPrice'] / percent, decimals)
        return risk_free_rate

    def get_bloomberg_risk_free_rate(self, symbol='USGG10YR Index', percent=100, decimals=4):
        """
        :description: Get risk-free rate from Bloomberg

        :param symbol: Ticker, default is 'USGG10YR Index'
        :type symbol: str, optional
        :param percent: Percent, default is 100
        :type percent: int, optional
        :param decimals: Decimals, default is 4
        :type decimals: int, optional
        :return: Risk free rate
        :rtype: float
        """
        if symbol is None:
            risk_free_rate = round(self.mgr['USGG10YR Index'].PX_LAST / percent, decimals)
        else:
            risk_free_rate = round(self.mgr[symbol].PX_LAST / percent, decimals)
        return risk_free_rate

    def get_risk_free_rate(self, prints=False, symbol=None):
        """
        :description: Calculate risk-free rate

        :param prints: Prints, default is False
        :type prints: bool, optional
        :param symbol: Ticker, default is None
        :type symbol: str, optional
        :return: Risk free rate
        :rtype: float
        """
        # Constants
        percent = 100
        decimals = 4

        self.check_valid_api_source()

        if self.api_source == 'yahoo':
            risk_free_rate = self.get_yahoo_risk_free_rate(symbol, percent, decimals)
        elif self.api_source == 'bloomberg':
            risk_free_rate = self.get_bloomberg_risk_free_rate(symbol, percent, decimals)

        if prints:
            print('------------------------------------')
            print(f"Risk Free Rate: {round(risk_free_rate * percent, decimals)}%")

        return risk_free_rate

    @staticmethod
    def get_yahoo_market_caps(symbols):
        """
        :description: Get market caps from Yahoo Finance

        :param symbols: Symbols
        :type symbols: list
        :return: Market caps
        :rtype: dict
        """
        market_cap_dict = {}
        symbol = None
        yq_tickers = [yq.Ticker(symbol) for symbol in symbols]
        for yq_symbol in tqdm(yq_tickers):
            try:
                summary_detail = yq_symbol.summary_detail
                symbol = list(summary_detail.keys())[0]
                if summary_detail is not None:
                    market_cap_dict[symbol] = summary_detail[symbol]['totalAssets']
                else:
                    raise ValueError(f"No summary detail found for symbol: {symbol}")
            except (KeyError, ValueError):
                price = yq_symbol.price
                if price is not None:
                    market_cap_dict[symbol] = price[symbol]['marketCap']
                else:
                    raise ValueError(f"No market cap found for symbol: {symbol}")
        return market_cap_dict

    def get_bloomberg_market_caps(self, symbols):
        """
        :description: Get market caps from Bloomberg

        :param symbols: Symbols
        :type symbols: list
        :return: Market caps
        :rtype: dict
        """
        market_caps = self.mgr[symbols].CUR_MKT_CAP
        market_caps.index = [s.replace(' US Equity', '') for s in market_caps.index]
        return market_caps.to_dict()

    def get_market_caps(self, prints=False):
        """
        :description: Calculate market caps

        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Market caps
        :rtype: pandas.Series
        """
        self.check_valid_api_source()

        processed_symbols = self.process_symbols(self.symbols, self.api_source)

        if self.api_source == 'yahoo':
            market_cap_dict = self.get_yahoo_market_caps(processed_symbols, prints)
        elif self.api_source == 'bloomberg':
            market_cap_dict = self.get_bloomberg_market_caps(processed_symbols)

        try:
            market_caps = pd.DataFrame.from_dict(
                market_cap_dict, orient='columns'
            ).squeeze() / 1_000_000
        except ValueError:
            market_caps = pd.Series(market_cap_dict) / 1_000_000

        if not isinstance(market_caps, pd.Series):
            market_caps = pd.Series([market_caps], index=[self.symbols[0]])

        market_caps.index = [s.replace(' US Equity', '') if isinstance(s, str) else s for s in market_caps.index]

        if prints:
            print('\nMarket Cap ($Millions):')
            print(market_caps.sort_values(ascending=False).apply(lambda x: f'${x:,.2f}'))

        return market_caps.squeeze()

    def get_yahoo_market_prices(self, prices, symbols):
        """
        :description: Get market prices from Yahoo Finance

        :param prices: Prices
        :type prices: pandas.core.frame.DataFrame
        :param symbols: Symbols
        :type symbols: list
        :return: Market name, market prices
        :rtype: tuple
        """
        market_name = yq.Ticker(self.market_symbol).price[self.market_symbol]['longName']
        market_prices = yq.Ticker(self.market_symbol).history(
            start=prices[symbols].index[0].strftime('%Y-%m-%d'),
            end=prices[symbols].index[-1].strftime('%Y-%m-%d')
        )['adjclose']
        market_prices = market_prices.unstack(level='symbol').dropna().squeeze().round(2)
        market_prices.index = pd.to_datetime(market_prices.index).date
        market_prices.name = market_name
        return market_name, market_prices

    def get_bloomberg_market_prices(self, prices, symbols):
        """
        :description: Get market prices from Bloomberg

        :param prices: Prices
        :type prices: pandas.DataFrame
        :param symbols: Symbols
        :type symbols: list
        :return: Market name, market prices
        :rtype: tuple
        """
        market_name = self.mgr[self.market_symbol].LONG_COMP_NAME
        market_prices = self.mgr[self.market_symbol].get_historical(
            'PX_LAST',
            start=prices[symbols].index[0],
            end=prices[symbols].index[-1]
        ).squeeze().round(2)
        market_prices.name = market_name
        return market_name, market_prices

    def get_market_prices(self, prices, symbols, prints=False):
        """
        :description: Calculate market values

        :param prices: Prices
        :type prices: pandas.core.frame.DataFrame, required
        :param symbols: Symbols
        :type symbols: list, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Market symbol, market name, market values
        :rtype: tuple
        """
        self.check_valid_api_source()

        if self.api_source == 'yahoo':
            market_name, market_prices = self.get_yahoo_market_prices(prices, symbols)
        elif self.api_source == 'bloomberg':
            market_name, market_prices = self.get_bloomberg_market_prices(prices, symbols)

        if prints:
            print('\nMarket Symbol:', self.market_symbol)
            print('Market Name:', market_name)
            print('Market Prices:')
            print(market_prices.apply(lambda x: '${:,.2f}'.format(round(x, 2))))

        return self.market_symbol, market_name, market_prices
