import time
import random
import pandas as pd
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
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
                accountIdKey=account_id_key,
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
                accountIdKey=account_id_key,
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

    def execute_trade(self, account_id_key, ticker, order_action, quantity, preview, prints=False):
        """
        :description: Helper function to execute trades

        :param account_id_key: Account ID key
        :type account_id_key: str, required
        :param ticker: Ticker
        :type ticker: str, required
        :param order_action: Order action
        :type order_action: str, required
        :param quantity: Quantity
        :type quantity: int, required
        :param preview: Preview trades, default is True. If False, trades will be executed.
        :type preview: bool, optional
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Trade response
        :rtype: dict
        """
        return self.generate_trades(
            account_id_key, ticker, order_action, quantity, preview=preview, prints=prints
        )

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
        # Setup and validation
        accounts = self.etrade.get_account_list(prints=False)
        accounts = [a for a in accounts.accountIdKey if a == account_id_key]
        if not accounts:
            raise ValueError(f"Account with account_id_key '{account_id_key}' not found.")

        # Initialize trade order lists
        sell_orders = []
        short_sell_orders = []
        buy_orders = []
        buy_cover_orders = []

        # Process portfolio and new allocation to categorize trades
        for ticker in set(current_portfolio.index).union(new_allocation.index):
            try:
                current_qty = current_portfolio.quantity[ticker]
            except KeyError:
                current_portfolio = current_portfolio.copy()
                current_portfolio.loc[ticker] = [0, 0, 'NONE']  # Adding new row for the missing ticker
                current_qty = 0
            try:
                new_qty = new_allocation.loc[ticker]
            except KeyError:
                new_allocation = new_allocation.copy()
                new_allocation.loc[ticker] = 0
                new_qty = 0
            net_qty = new_qty - current_qty

            # CONDITION 1: If net_qty is less than 0, and current position is LONG, SELL and/or SELL_SHORT
            if net_qty < 0 and current_portfolio.positionType.loc[ticker] == 'LONG':
                if abs(net_qty) > current_qty:  # Sell all shares
                    sell_orders.append((ticker, -current_qty))
                    short_sell_orders.append((ticker, net_qty))
                else:
                    sell_orders.append((ticker, net_qty))

            # CONDITION 2: If net_qty is less than 0, and current position is SHORT, SHORT SELL
            elif net_qty < 0 and current_portfolio.positionType.loc[ticker] == 'SHORT':
                short_sell_orders.append((ticker, net_qty))

            # CONDITION 3: If net_qty is greater than 0, and current position is SHORT, BUY_TO_COVER and/or BUY
            elif net_qty > 0 and current_portfolio.positionType.loc[ticker] == 'SHORT':
                if net_qty > current_qty:
                    buy_cover_orders.append((ticker, current_qty))
                    buy_orders.append((ticker, net_qty))
                else:
                    buy_cover_orders.append((ticker, net_qty))

            # CONDITION 4: If net_qty is greater than 0, and current position is LONG, BUY
            elif net_qty > 0 and current_portfolio.positionType.loc[ticker] == 'LONG':
                buy_orders.append((ticker, net_qty))

            # CONDITION 5: If current position is NONE, BUY or SHORT SELL
            elif current_portfolio.positionType.loc[ticker] == 'NONE':
                if net_qty < 0:
                    short_sell_orders.append((ticker, net_qty))
                elif net_qty > 0:
                    buy_orders.append((ticker, net_qty))

            # CONDITION 6: If net_qty is 0, do nothing
            elif net_qty == 0:
                continue

            else:
                raise ValueError(f'INVALID TRADE LOGIC for {ticker}.')

        if prints:
            # Proposed Trades
            print('Proposed Trades...')
            print('---------------------')
            if sell_orders:
                for ticker, qty in sell_orders:
                    print(f'SELL {abs(qty)} shares of {ticker}')
            if short_sell_orders:
                for ticker, qty in short_sell_orders:
                    print(f'SELL_SHORT {abs(qty)} shares of {ticker}')
            if buy_orders:
                for ticker, qty in buy_orders:
                    print(f'BUY {abs(qty)} shares of {ticker}')
            if buy_cover_orders:
                for ticker, qty in buy_cover_orders:
                    print(f'BUY_TO_COVER {abs(qty)} shares of {ticker}')
            if not sell_orders and not short_sell_orders and not buy_orders and not buy_cover_orders:
                print('No trades to execute.')

            # Execute trades in the specified order
            print('\n')
            if preview:
                print('Previewing Trades...')
            else:
                print('Executing Trades...')
            print('---------------------')

        # Execute trades in the specified order
        trade_responses = {}
        qty = None
        ticker = None
        try:
            for ticker, qty in sell_orders:
                trade_responses[ticker] = self.execute_trade(
                    account_id_key, ticker, 'SELL', abs(qty), preview)
                if prints:
                    print('SELL {} shares of {}'.format(abs(qty), ticker))
            for ticker, qty in short_sell_orders:
                trade_responses[ticker] = self.execute_trade(
                    account_id_key, ticker, 'SELL_SHORT', abs(qty), preview)
                if prints:
                    print('SELL_SHORT {} shares of {}'.format(abs(qty), ticker))
            for ticker, qty in buy_orders:
                trade_responses[ticker] = self.execute_trade(
                    account_id_key, ticker, 'BUY', abs(qty), preview)
                if prints:
                    print('BUY {} shares of {}'.format(abs(qty), ticker))
            for ticker, qty in buy_cover_orders:
                trade_responses[ticker] = self.execute_trade(
                    account_id_key, ticker, 'BUY_TO_COVER', abs(qty), preview)
                if prints:
                    print('BUY_TO_COVER {} shares of {}'.format(abs(qty), ticker))
        except Exception as e:
            print('ERROR executing {} shares of {}.'.format(qty, ticker))
            print('\n')
            print(e)

        # Handling responses and finalizing
        trade_responses_dict = {}
        for key, value in trade_responses.items():
            if value:  # Check if there is a response to process
                xml_str = dicttoxml(value).decode()
                root = ET.fromstring(xml_str)
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

        try:
            df = pd.DataFrame.from_dict(trade_responses_dict, orient='index')
            df = df[['orderAction', 'priceType', 'quantity', 'orderTerm', 'marketSession']].apply(
                pd.to_numeric, errors='ignore'
            )
            df.index.name = 'symbol'
            return df
        except KeyError:
            print('No trades to execute.')
