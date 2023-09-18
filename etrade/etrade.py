import xmltodict
import pandas as pd
from authentication.authentication import Authentication


class ETrade:
    """
    :description: ETrade class

    :param consumer_key: Consumer key
    :type consumer_key: str, required
    :param consumer_secret: Consumer secret
    :type consumer_secret: str, required
    :param web_username: Etrade web username
    :type web_username: str, required
    :param web_password: Etrade web password
    :type web_password: str, required
    :param account_id: Etrade account ID
    :type account_id: str, required
    :param etrade_cookie: Etrade cookie
    :type etrade_cookie: dict, required
    :param sandbox_key: Etrade sandbox consumer key
    :type sandbox_key: str, required
    :param sandbox_secret: Etrade sandbox consumer secret
    :type sandbox_secret: str, required
    :param dev: Run in sandbox mode, defaults to False
    :type dev: bool, optional
    :param headless: Run browser in headless mode, defaults to True
    :type headless: bool, optional
    :param browser: Browser to use, defaults to 'chrome' or use 'edge'
    :type browser: str, optional
    :param retries: Number of retries for failed requests, defaults to 3
    :type retries: int, optional
    :param sleep: Sleep time between retries, defaults to 30
    :type sleep: int, optional
    :EtradeRef: https://apisb.etrade.com/docs/api/authorization/request_token.html
    """

    def __init__(
            self, consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie,
            sandbox_key=None, sandbox_secret=None, dev=False, headless=True, browser='chrome', retries=3, sleep=30
    ):
        self.auth = Authentication(
            consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie,
            sandbox_key, sandbox_secret, dev, headless, browser, retries, sleep
        )
        self.accounts, self.orders, self.market = self.auth.etrade_login()
        self.dev = dev

    def get_account_list(self, prints=False):
        """
        :description: Get a list of all accounts

        :param prints: Print the accounts
        :type prints: bool
        :return: DataFrame of accounts
        :rtype: pandas.DataFrame
        """
        list_accounts = self.accounts.list_accounts(resp_format='json')
        list_accounts = pd.DataFrame(list_accounts['AccountListResponse']['Accounts']['Account']).set_index('accountId')

        if prints:
            print(list_accounts)

        return list_accounts

    def get_account_balance(self, account_id_key, prints=False):
        """
        :description: Get balance

        :param account_id_key: Account ID key
        :type account_id_key: str, required
        :param prints: Print balance response, defaults to False
        :type prints: bool, optional
        :return: Balance response
        :rtype: pandas.core.series.Series
        """
        balance_response = self.accounts.get_account_balance(account_id_key, resp_format='json')

        def flatten_dict(d):
            items = []
            for k, v in d.items():
                if isinstance(v, dict):
                    items.extend(flatten_dict(v).items())
                else:
                    items.append((k, v))
            return dict(items)

        flat_d = flatten_dict(balance_response)
        df = pd.DataFrame({'BalanceResponse': flat_d}).squeeze()
        df = pd.to_numeric(df, errors='ignore')

        if prints:
            print(df)

        return df

    def get_orders_list(self, account_id_key, prints=False):
        """
        :description: Get a list of all orders for a given account

        :param account_id_key: Account ID
        :type account_id_key: str
        :param prints: Print the orders
        :type prints: bool
        :return: DataFrame of orders
        :rtype: pandas.DataFrame
        """
        orders_data = self.orders.list_orders(account_id_key, resp_format='json')

        if 'OrdersResponse' not in orders_data or 'Order' not in orders_data['OrdersResponse']:
            raise ValueError('No orders found for account: {}'.format(account_id_key))

        orders_data = orders_data['OrdersResponse']['Order']

        orders_list = []
        for order in orders_data:
            order_detail = order['OrderDetail'][0]
            instrument = order_detail['Instrument'][0]
            order_dict = {
                'orderId': order['orderId'],
                'orderType': order['orderType'],
                'placedTime': order_detail['placedTime'],
                'executedTime': order_detail.get('executedTime', None),
                'orderValue': order_detail['orderValue'],
                'status': order_detail['status'],
                'symbolDescription': instrument['symbolDescription'],
                'orderAction': instrument['orderAction'],
                'orderedQuantity': instrument['orderedQuantity'],
                'filledQuantity': instrument['filledQuantity'],
                'estimatedCommission': instrument['estimatedCommission'],
                'estimatedFees': instrument['estimatedFees'],
                'symbol': instrument['Product']['symbol'],
                'securityType': instrument['Product']['securityType']
            }
            if (order_detail['status'] != 'CANCELLED') and (order_detail['status'] != 'OPEN'):
                order_dict['averageExecutionPrice'] = instrument['averageExecutionPrice']

            else:
                order_dict['averageExecutionPrice'] = None
            orders_list.append(order_dict)

        df = pd.DataFrame(orders_list).set_index('orderId')

        if prints:
            print(df)

        return df

    def get_market_quote(self, symbols, prints=False):
        """
        :description: Get market quote for a list of symbols

        :param symbols: List of symbols
        :type symbols: list
        :param prints: Print the quote
        :type prints: bool
        :return: DataFrame of quote
        :rtype: pandas.DataFrame
        """
        json_dict = self.market.get_quote(symbols, resp_format='json')
        quote_data = json_dict['QuoteResponse']['QuoteData']
        data = []
        headers = []
        for quote in quote_data:
            symbol = quote['Product']['symbol']
            headers.append(symbol)

            def extract_data(data_dict, parent_key=''):
                for key, value in data_dict.items():
                    field_name = f'{key}' if parent_key == '' else f'{parent_key}.{key}'
                    if isinstance(value, dict):
                        extract_data(value, field_name)
                    elif isinstance(value, list):
                        if isinstance(value[0], dict):
                            for item in value:
                                extract_data(item, field_name)
                    else:
                        data.append([field_name, value, symbol])

            extract_data(quote)

        df = pd.DataFrame(data, columns=['Field', 'Value', 'Symbol'])
        df = df.pivot(index='Field', columns='Symbol', values='Value')

        if prints:
            print(df)

        return df

    def get_buying_power(self, account_id_key, resp_format='json', prints=False):
        """
        :description: Extract buying power

        :param account_id_key: Account ID key
        :type account_id_key: str, required
        :param resp_format: Response format
        :type resp_format: str, optional
        :param prints: Print output, default is False
        :type prints: bool, optional
        :return: Buying power
        :rtype: float
        """
        balance_response = self.accounts.get_account_balance(account_id_key, resp_format=resp_format)
        buying_power = balance_response['BalanceResponse']['Computed']['RealTimeValues']['totalAccountValue']

        if prints:
            print('')
            print(f'Buying Power: ${buying_power:,.2f}')

        return float(buying_power)

    def get_portfolio_data(self, account_id_key, sort_by='totalGainPct', ascending=False):
        """
        :description: Get portfolio data

        :param account_id_key: Account ID key
        :type account_id_key: str
        :param sort_by: Sort by column
        :type sort_by: str
        :param ascending: Sort ascending
        :type ascending: bool
        :return: Portfolio data
        :rtype: pandas.DataFrame
        """
        try:
            account_portfolio = self.accounts.get_account_portfolio(account_id_key)
        except xmltodict.expat.ExpatError:
            return pd.DataFrame()

        fields = ['symbolDescription', 'positionType', 'quantity', 'costPerShare', 'marketValue', 'totalCost',
                  'daysGain', 'daysGainPct', 'totalGain', 'totalGainPct', 'pctOfPortfolio']
        portfolio_data = pd.DataFrame(account_portfolio['PortfolioResponse']['AccountPortfolio']['Position'])[fields]
        portfolio_data = portfolio_data.apply(pd.to_numeric, errors='ignore')
        portfolio_data = portfolio_data.sort_values(by=sort_by, ascending=ascending).set_index('symbolDescription')

        return portfolio_data

    @staticmethod
    def compute_portfolio_performance(portfolio_data):
        """
        :description: Compute portfolio performance

        :param portfolio_data: Portfolio data
        :type portfolio_data: pandas.DataFrame
        :return: Portfolio performance
        :rtype: pandas.Series
        """
        dollar_cols = ['marketValue', 'totalCost', 'daysGain', 'totalGain']
        percent_cols = ['daysGainPct', 'totalGainPct']

        # Remove dollar sign and convert to float
        for col in dollar_cols:
            portfolio_data[col] = portfolio_data[col].replace(r'[\$,]', '', regex=True).astype(float)

        # Convert percentage strings to float numbers
        portfolio_data[percent_cols] = portfolio_data[percent_cols].replace('%', '', regex=True).astype('float')

        # Compute sum for dollar_cols
        dollar_sum = portfolio_data[dollar_cols].sum()

        # Compute the performance metrics as defined
        portfolio_performance = dollar_sum.copy()
        portfolio_performance['daysGainPct'] = dollar_sum['daysGain'] / (
                    dollar_sum['totalCost'] - dollar_sum['daysGain'])
        portfolio_performance['totalGainPct'] = dollar_sum['totalGain'] / dollar_sum['totalCost']

        # Now convert to string format
        portfolio_performance[dollar_cols] = portfolio_performance[dollar_cols].apply(lambda x: '${:,.2f}'.format(x))
        for col in percent_cols:
            if col in portfolio_performance:
                portfolio_performance[col] = '{:.2f}%'.format(
                    portfolio_performance[col] * 100)  # multiplying by 100 to convert ratio to percentage

        return portfolio_performance

    @staticmethod
    def format_portfolio_data(portfolio_data):
        """
        :description: Format portfolio data

        :param portfolio_data: Portfolio data
        :type portfolio_data: pandas.DataFrame
        :return: Formatted portfolio data
        :rtype: pandas.DataFrame
        """
        # Copy the original dataframe to avoid altering it
        formatted_portfolio = portfolio_data.copy()

        # Define the columns to be formatted
        dollar_cols = ['costPerShare', 'marketValue', 'totalCost', 'daysGain', 'totalGain']
        percent_cols = ['daysGainPct', 'totalGainPct', 'pctOfPortfolio']

        # Apply formatting
        for col in dollar_cols:
            formatted_portfolio[col] = formatted_portfolio[col].apply(
                lambda x: '${:,.2f}'.format(x) if isinstance(x, float) else x)

        for col in percent_cols:
            formatted_portfolio[col] = formatted_portfolio[col].apply(
                lambda x: '{:.2f}%'.format(x) if isinstance(x, float) else x)

        return formatted_portfolio

    @staticmethod
    def get_current_portfolio(portfolio_data):
        """
        :description: Get current portfolio

        :param portfolio_data: Portfolio data
        :type portfolio_data: pandas.DataFrame
        :return: Current portfolio
        :rtype: pandas.DataFrame
        """

        current_portfolio = portfolio_data[[
            'pctOfPortfolio', 'quantity', 'positionType'
        ]]

        return current_portfolio
