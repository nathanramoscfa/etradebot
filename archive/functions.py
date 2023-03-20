import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor


def vif_filter(prices, market_caps, threshold=100, prints=False):
    """
    :description: Variance inflation factor filter to reduce multicollinearity

    :param prices: Prices
    :type prices: pandas.core.frame.DataFrame, required
    :param market_caps: Market caps
    :type market_caps: pandas.core.series.Series, required
    :param threshold: Threshold, default is 50
    :type threshold: int, optional
    :param prints: Prints, default is False
    :type prints: bool, optional
    :return: VIF symbols
    :rtype: list
    """
    returns = prices[market_caps.index].pct_change().dropna()
    vif_factors = pd.Series([variance_inflation_factor(returns.values, i) for i in range(returns.shape[1])],
                            index=returns.columns)
    vif_symbols = list(vif_factors[vif_factors <= threshold].index)

    if prints:
        print('VIF Tickers:')
        print(round(vif_factors.sort_values(), 2))

    return vif_symbols
