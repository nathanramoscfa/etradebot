####################################################################################
# DISCLAIMER:                                                                      #
# The following strategy is for demonstration purposes only and is not intended    #
# to be used as an actual trading strategy. This strategy is only for testing      #
# purposes. DO NOT use this example strategy with real money. Invest at your       #
# own risk.                                                                        #
####################################################################################


from pypfopt import expected_returns
from model.model import Model
from api.api import DataAPI


def strategy(prints=False):
    """
    Example strategy.

    :param prints: Print the strategy
    :type prints: bool
    :return: Strategy percentage weights for each position
    :rtype: pd.Series
    """

    # Define ETFs and their tickers
    etfs = {
        'SPY': 'U.S. Large Cap Equities',
        'IWM': 'U.S. Small Cap Equities',
        'EFA': 'International Equities',
        'EEM': 'Emerging Market Equities',
        'AGG': 'U.S. Aggregate Bonds',
        'LQD': 'Corporate Bonds',
        'HYG': 'High Yield Bonds',
        'TLT': 'Treasury Bonds',
        'TIP': 'Inflation-Protected Bonds',
        'VNQ': 'Real Estate Investment Trusts (REITs)'
    }

    # Get the list of symbols
    symbols = list(etfs.keys())

    # Instantiate the API
    api = DataAPI(
        symbols=symbols
    )

    # Instantiate the model
    model = Model(symbols=symbols, bounds=(0.0, 0.3), min_weight=0.05, margin_rate=0.132, long_weight=1.0,
                  short_weight=0.0, frequency=252)

    # Get historical prices
    historical_prices = api.get_historical_prices()

    # Calculate expected returns using the mean historical returns
    mu = expected_returns.mean_historical_return(historical_prices)

    # Calculate the sample covariance matrix
    sigma = model.calculate_covariance_matrix(historical_prices, symbols)

    # Get the risk-free rate
    risk_free_rate = api.get_risk_free_rate(prints=prints)

    # Calculate the maximum Sharpe ratio portfolio
    max_sharpe_weights, max_sharpe_results = model.maximum_sharpe_portfolio(
        mu, sigma, risk_free_rate, prints
    )

    return max_sharpe_weights
