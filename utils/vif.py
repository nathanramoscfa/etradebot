import warnings
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor


def vif_filter(prices, market_cap, threshold=50, prints=False, omit_method='market_cap'):
    """
    :description: Variance inflation factor filter to reduce multicollinearity

    :param prices: Prices
    :type prices: pandas.core.frame.DataFrame, required
    :param market_cap: Market capitalization or fund total net assets
    :type market_cap: pandas.core.series.Series, required
    :param threshold: Threshold, default is 50
    :type threshold: int, optional
    :param prints: Prints, default is False
    :type prints: bool, optional
    :param omit_method: Omitting method, default is 'market_cap'. Options are 'market_cap' or 'vif'. If
    'market_cap', the symbol with the highest market capitalization will be omitted. If 'vif', the symbol with
    the highest VIF will be omitted.
    :type omit_method: str, optional
    :return: VIF symbols
    :rtype: list
    """
    returns = prices[market_cap.index].pct_change().dropna()
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    df = pd.DataFrame(columns=["VIF Factor"])
    for _ in range(returns.shape[1]):
        try:
            df = pd.DataFrame(
                {"VIF Factor": [variance_inflation_factor(returns.values, i) for i in range(returns.shape[1])]}
            )
            df.index = returns.columns
            if df.max().iloc[0] > threshold:
                if omit_method == 'market_cap':
                    high_vif_tickers = df[df['VIF Factor'] > threshold].index
                    relevant_market_caps = market_cap[high_vif_tickers]
                    omit = relevant_market_caps.idxmin()
                elif omit_method == 'vif':
                    omit = df.idxmax()
                else:
                    raise ValueError("Please select a valid omitting method: 'market_cap' or 'vif'")
                returns = returns.drop(omit, axis=1)
        except ValueError:
            continue
    df.index.name = 'TICKER'
    vif = df.squeeze()
    vif_symbols = list(vif.index)
    if prints:
        print('\nVIF Tickers:')
        print(round(vif, 2).sort_values())

    return vif_symbols
