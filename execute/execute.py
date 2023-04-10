import time
import random
import pandas as pd
import xml.etree.ElementTree as ET
from pypfopt import DiscreteAllocation


class Execute:
    """
    :description: Execute trades

    :param etrade: Etrade API object
    :type etrade: pyetrade.ETradeAccounts, required
    """
    def __init__(
            self, etrade
    ):
        """
        :description: Initialize class

        :return: None
        :rtype: None
        """
        self.etrade = etrade

    def calculate_shares(
            self, weights, buying_power, reinvest=True, prints=False
    ):
        """
        :description: Calculate shares to buy or sell

        :param weights: Weights of new portfolio
        :type weights: pandas.core.series.Series, required
        :param buying_power: Buying power
        :type buying_power: float, required
        :param reinvest: Reinvest cash from short position, default is True
        :type reinvest: bool, optional
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Shares to buy or sell
        :rtype: dict
        """
        quote_col_name = 'All.lastTrade'
        output_decimals = 2

        symbols = list(weights.index)
        current_prices = pd.to_numeric(
            self.etrade.get_market_quote(symbols, prints=False).loc[quote_col_name], errors='coerce'
        )
        short_weight = -weights[weights < 0].sum()
        da = DiscreteAllocation(
            weights=dict(weights),
            latest_prices=current_prices,
            total_portfolio_value=buying_power,
            short_ratio=short_weight
        )
        allocation, leftover = da.greedy_portfolio(reinvest)
        allocation = pd.DataFrame.from_dict(allocation, orient='index', columns=['Shares']).squeeze()
        trade_values = (allocation * current_prices).sort_values(ascending=False)
        trade_values.name = 'Trade Amounts'
        total_trade_value = trade_values.sum()
        shares_to_buy = allocation.to_dict()
        shares_to_buy = pd.DataFrame.from_dict(shares_to_buy, orient='index', columns=['Shares']).squeeze()

        if prints:
            print('')
            print('Trade Instructions:')
            print(trade_values.apply(lambda x: '${:,.{}f}'.format(round(x, output_decimals), output_decimals)))
            print(f"\nPosition Value: ${total_trade_value:,.2f}")
            print(f"Leftover: ${leftover:,.2f}\n")
            print(allocation.apply(lambda x: "{:,}".format(x)))

        return shares_to_buy

    def generate_trades(
            self, account_id_key, symbol, order_action, quantity, price_type='MARKET', order_term='GOOD_FOR_DAY',
            market_session='REGULAR', preview=True, prints=False
    ):
        """
        :description: Generate trades. If preview is True, trades will be previewed. If False, trades will be executed.

        :param account_id_key: Account ID key
        :type account_id_key: str, required
        :param symbol: Ticker
        :type symbol: str, required
        :param order_action: Order action
        :type order_action: str, required
        :param quantity: Quantity
        :type quantity: int, required
        :param price_type: Price type, default is 'MARKET'.
        :type price_type: str, optional
        :param order_term: Order term, default is 'GOOD_FOR_DAY'
        :type order_term: str, optional
        :param market_session: Market session, default is 'REGULAR'
        :type market_session: str, optional
        :param preview: Preview trades, default is True. If False, trades will be executed.
        :type preview: bool, optional
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Trade response
        :rtype: dict
        """
        trade_response = None
        if preview:
            trade_response = self.etrade.orders.preview_equity_order(
                resp_format="xml",
                accountId=account_id_key,
                symbol=symbol,
                orderAction=order_action,
                clientOrderId=random.randint(1000000000, 9999999999),
                priceType=price_type,
                quantity=abs(quantity),
                orderTerm=order_term,
                marketSession=market_session
            )
        elif not preview:
            trade_response = self.etrade.orders.place_equity_order(
                resp_format="xml",
                accountId=account_id_key,
                symbol=symbol,
                orderAction=order_action,
                clientOrderId=random.randint(1000000000, 9999999999),
                priceType=price_type,
                quantity=abs(quantity),
                orderTerm=order_term,
                marketSession=market_session
            )
        if prints:
            print(trade_response)

        return trade_response

    def execute_trades(self, current_portfolio, new_allocation, account_id_key, preview=True, prints=False):
        """
        :description: Execute trades

        :param current_portfolio: Current portfolio
        :type current_portfolio: pandas.core.frame.DataFrame, required
        :param new_allocation: New allocation
        :type new_allocation: pandas.core.series.Series, required
        :param account_id_key: Account ID key
        :type account_id_key: str, required
        :param preview: Preview trades, default is True. If False, trades will be executed.
        :type preview: bool, optional
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Trade responses
        :rtype: dict
        """
        # Filter out any empty accounts
        accounts = self.etrade.get_account_list(prints=False)
        accounts = [a for a in accounts.accountIdKey if a == account_id_key]
        if not accounts:
            raise ValueError(f"Account with account_id_key '{account_id_key}' not found.")

        # Get current shares
        current_shares = current_portfolio.copy().quantity

        # Keep track of trade responses
        trade_responses = {}

        # Loop over current portfolio
        for ticker in current_portfolio.index:
            # Liquidates current positions that are not included in the new portfolio
            if ticker not in new_allocation.index:
                if current_portfolio.loc[ticker, 'positionType'] == 'LONG':
                    current_shares.loc[ticker] = 0
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL',
                            quantity=current_portfolio.loc[ticker, 'quantity']
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL',
                            quantity=current_portfolio.loc[ticker, 'quantity'], preview=False
                        )
                    if prints:
                        print('SELL {} shares of {}'.format(current_portfolio.loc[ticker, 'quantity'], ticker))
                elif current_portfolio.loc[ticker, 'positionType'] == 'SHORT':
                    current_shares.loc[ticker] = 0
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY_TO_COVER',
                            quantity=current_portfolio.loc[ticker, 'quantity']
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY_TO_COVER',
                            quantity=current_portfolio.loc[ticker, 'quantity'], preview=False
                        )
                    if prints:
                        print('BUY_TO_COVER {} shares of {}'.format(current_portfolio.loc[ticker, 'quantity'], ticker))

            # Handles instances if current position flips from long to short and vice-versa
            if ticker in new_allocation.index:
                if (current_portfolio.loc[ticker, 'positionType'] == 'LONG') & (new_allocation.loc[ticker] < 0):
                    current_shares.loc[ticker] = current_shares.loc[ticker] - current_portfolio.loc[ticker, 'quantity']
                    current_shares.loc[ticker] = current_shares.loc[ticker] - new_allocation.loc[ticker]
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL',
                            quantity=current_portfolio.loc[ticker, 'quantity']
                        )
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL_SHORT',
                            quantity=current_portfolio.loc[ticker, 'quantity']
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL',
                            quantity=new_allocation.loc[ticker], preview=False
                        )
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL_SHORT',
                            quantity=new_allocation.loc[ticker], preview=False
                        )
                    if prints:
                        print('SELL {} shares of {}'.format(current_portfolio.loc[ticker, 'quantity'], ticker))
                        print('SELL_SHORT {} shares of {}'.format(new_allocation.loc[ticker], ticker))
                elif (current_portfolio.loc[ticker, 'positionType'] == 'SHORT') & (new_allocation.loc[ticker] > 0):
                    current_shares.loc[ticker] = current_shares.loc[ticker] + current_portfolio.loc[ticker, 'quantity']
                    current_shares.loc[ticker] = current_shares.loc[ticker] + new_allocation.loc[ticker]
                    if prints:
                        print('BUY_TO_COVER {} shares of {}'.format(current_portfolio.loc[ticker, 'quantity'], ticker))
                        print('BUY {} shares of {}'.format(new_allocation.loc[ticker], ticker))
        time.sleep(5)

        # Logic for new portfolio
        for ticker in new_allocation.index:
            if new_allocation.loc[ticker] > 0:
                try:
                    net_quantity = new_allocation.loc[ticker] - current_shares.loc[ticker]
                except KeyError:
                    net_quantity = new_allocation.loc[ticker]
                if net_quantity > 0:
                    try:
                        current_shares.loc[ticker] = current_shares.loc[ticker] + net_quantity
                    except KeyError:
                        current_shares[ticker] = net_quantity
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY', quantity=net_quantity
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY', quantity=net_quantity, preview=False
                        )
                    if prints:
                        print('BUY {} shares of {}'.format(net_quantity, ticker))
                elif net_quantity < 0:
                    try:
                        current_shares.loc[ticker] = current_shares.loc[ticker] - net_quantity
                    except KeyError:
                        current_shares.loc[ticker] = net_quantity
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL', quantity=net_quantity
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL', quantity=net_quantity, preview=False
                        )
                    if prints:
                        print('SELL {} shares of {}'.format(net_quantity, ticker))

            elif new_allocation.loc[ticker] < 0:
                try:
                    net_quantity = new_allocation.loc[ticker] - current_shares.loc[ticker]
                except KeyError:
                    net_quantity = new_allocation.loc[ticker]
                if net_quantity < 0:
                    try:
                        current_shares.loc[ticker] = current_shares.loc[ticker] + net_quantity
                    except KeyError:
                        current_shares.loc[ticker] = net_quantity
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL_SHORT', quantity=net_quantity
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='SELL_SHORT', quantity=net_quantity, preview=False
                        )
                    if prints:
                        print('SELL_SHORT {} shares of {}'.format(net_quantity, ticker))
                elif net_quantity > 0:
                    try:
                        current_shares.loc[ticker] = current_shares.loc[ticker] - net_quantity
                    except KeyError:
                        current_shares.loc[ticker] = net_quantity
                    if preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY_TO_COVER', quantity=net_quantity
                        )
                    elif not preview:
                        trade_responses[ticker] = self.generate_trades(
                            account_id_key, ticker, order_action='BUY_TO_COVER', quantity=net_quantity, preview=False
                        )
                    if prints:
                        print('BUY_TO_COVER {} shares of {}'.format(net_quantity, ticker))
        time.sleep(5)

        trade_responses_dict = {}
        for key, value in trade_responses.items():
            root = ET.fromstring(value)
            data_dict = {}
            for element in root.iter():
                if element.tag == root.tag:
                    continue
                if len(list(element)) == 0:
                    data_dict[element.tag] = element.text
                else:
                    sub_dict = {}
                    for sub_element in element:
                        sub_dict[sub_element.tag] = sub_element.text
                    data_dict[element.tag] = sub_dict
            trade_responses_dict[key] = data_dict

        df = pd.DataFrame.from_dict(trade_responses_dict, orient='index')
        df = df[['orderAction', 'priceType', 'quantity', 'orderTerm', 'marketSession']].apply(
            pd.to_numeric, errors='ignore'
        )
        df.index.name = 'symbol'

        return df
