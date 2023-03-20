import pandas as pd


def get_equity_etf_data(path, min_long_return=0.15, max_short_return=0.0):
    """
    :description: Get equity ETF data and filter ETFs by expected return

    :param path: Path to file
    :type path: str, required
    :param min_long_return: Minimum required long return, default is 0.15
    :type min_long_return: float, optional
    :param max_short_return: Maximum tolerable short return, default is 0.0
    :type max_short_return: float, optional
    :return: Selected equity ETFs
    :rtype: pd.DataFrame
    """
    equity_etf_csv = pd.read_csv(
        r'{}'.format(path)
    )

    selected_equity_etfs = equity_etf_csv[
        (equity_etf_csv['FWD_RETURN_FORECAST'] >= min_long_return) |
        (equity_etf_csv['FWD_RETURN_FORECAST'] <= max_short_return)
        ]

    return selected_equity_etfs


def get_common_stock_data(path, min_long_return=0.15, max_short_return=0.0):
    """
    :description: Get common stock data and filter stocks by expected return

    :param path: Path to file
    :type path: str, required
    :param min_long_return: Minimum required long return, default is 0.15
    :type min_long_return: float, optional
    :param max_short_return: Maximum tolerable short return, default is 0.0
    :type max_short_return: float, optional
    :return: Selected common stocks
    :rtype: pd.DataFrame
    """
    equity_etf_csv = pd.read_csv(
        r'{}'.format(path)
    )

    selected_common_stocks = equity_etf_csv[
        (equity_etf_csv['FWD_RETURN_FORECAST'] >= min_long_return) |
        (equity_etf_csv['FWD_RETURN_FORECAST'] <= max_short_return)
        ]

    return selected_common_stocks


def investor_views_confidences(selected_etfs_stocks, vif_symbols, prints=False):
    """
    :description: Investor views and confidences

    :param selected_etfs_stocks: Selected equity ETFs
    :type selected_etfs_stocks: pandas.core.frame.DataFrame, required
    :param vif_symbols: Variance inflation factor symbols
    :type vif_symbols: list, required
    :param prints: Prints, default is False
    :type prints: bool, optional
    :return: Investor views and confidences
    :rtype: tuple of pd.core.series.Series
    """
    investor_views = {}
    for symbol in vif_symbols:
        investor_views[symbol] = selected_etfs_stocks.set_index('TICKER').loc[symbol]['FWD_RETURN_FORECAST']
    investor_views_df = pd.DataFrame.from_dict(investor_views, orient='index', columns=['Investor Views']).squeeze()
    investor_views_df.index.name = 'TICKER'
    if prints:
        print('Investor Views:')
        print(
            (100 * investor_views_df).sort_values(ascending=False).apply(lambda x: '{:,.2f}%'.format(round(x, 2)))
        )

    confidences = selected_etfs_stocks[['TICKER', 'RSQUARED']].set_index('TICKER').loc[vif_symbols].squeeze()
    confidences.name = 'Confidences'
    if prints:
        print('\nView Confidences:')
        print((100 * confidences).sort_values(ascending=False).apply(lambda x: '{:,.2f}%'.format(round(x, 2))))

    return investor_views, confidences
