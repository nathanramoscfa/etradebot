import pandas as pd
import numpy as np
import cvxpy as cp
from matplotlib import pyplot as plt
from tqdm import tqdm
from pypfopt import risk_models, black_litterman, efficient_frontier


class Model(object):
    """
    :description: Class for the portfolio modeling.

    :param symbols: List of symbols
    :type symbols: list, required
    :param historical_prices: Historical prices
    :type historical_prices: pandas.core.frame.DataFrame, required
    :param bounds: Bounds for long and short weights, default is (0.0, 1.0)
    :type bounds: tuple, optional
    :param min_weight: Minimum weight, default is 0.0
    :type min_weight: float, optional
    :param margin_rate: Margin rate, default is 0.0
    :type margin_rate: float, optional
    :param long_weight: Long weight, default is 1.0
    :type long_weight: float, optional
    :param short_weight: Short weight, default is 0.0
    :type short_weight: float, optional
    :param frequency: Frequency, default is 252
    :type frequency: int, optional
    :param optimization_method: Method, default is 'mean_variance'. Options are 'mean_variance', 'semivariance',
        'cvar', 'cdar'
    :type optimization_method: str, optional
    :param risk_method: Risk model, default is 'sample_cov'. Options are 'sample_cov', 'semicovariance', 'exp_cov',
        'ledoit_wolf', 'ledoit_wolf_constant_variance', ledoit_wolf_single_factor, ledoit_wolf_constant_correlation,
        'oracle_approximating'
    :type risk_method: str, optional
    :param semivariance_benchmark: The return threshold to distinguish "downside" and "upside". Default is 0
    :type semivariance_benchmark: int, optional
    :param beta: Confidence level (e.g., expected loss on the worst (1-beta) days). Default is 0.95
    :type beta: float, optional
    """
    def __init__(
            self,
            symbols,
            historical_prices,
            bounds=(0.0, 1.0),
            min_weight=0.0,
            margin_rate=0.0,
            long_weight=1.0,
            short_weight=0.0,
            frequency=252,
            optimization_method='mean_variance',
            risk_method='sample_cov',
            semivariance_benchmark=0,
            beta=0.95
    ):
        self.symbols = symbols
        self.bounds = bounds
        self.min_weight = min_weight
        self.margin_rate = margin_rate
        self.long_weight = long_weight
        self.short_weight = short_weight
        self.frequency = frequency
        self.optimization_method = optimization_method
        self.risk_method = risk_method
        self.semivariance_benchmark = semivariance_benchmark
        self.historical_prices = historical_prices
        self.returns = historical_prices.pct_change().dropna()
        self.beta = beta

    @staticmethod
    def calculate_covariance_matrix(prices, symbols, risk_method='sample_cov', prints=False):
        """
        :description: Calculate covariance matrix

        :param prices: Prices
        :type prices: pandas.core.frame.DataFrame, required
        :param symbols: Symbols
        :type symbols: list, required
        :param risk_method: Risk method
        :type risk_method: str, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Covariance matrix
        :rtype: pandas.core.frame.DataFrame
        """
        covariance_matrix = risk_models.risk_matrix(prices[symbols], risk_method)
        covariance_matrix = risk_models.fix_nonpositive_semidefinite(covariance_matrix)
        if prints:
            print('\nCovariance Matrix:')
            print(round(covariance_matrix, 4))

        return covariance_matrix

    def market_implied_risk_aversion(self, market_prices, risk_free_rate, prints=False):
        """
        :description: Market implied risk aversion

        :param market_prices: Market prices
        :type market_prices: pandas.core.series.Series, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Market implied risk aversion
        :rtype: float
        """
        if not isinstance(market_prices, (pd.Series, pd.DataFrame)):
            raise TypeError("Please format market_prices as a pd.Series")
        returns = market_prices.pct_change().dropna()
        average_return = returns.mean() * self.frequency
        variance = returns.var() * self.frequency
        delta = round((average_return - risk_free_rate) / variance, 2)
        if prints:
            print('\nMarket Implied Risk Aversion:')
            print('Delta: {}'.format(delta))

        return delta

    def calculate_black_litterman(
            self, covariance_matrix, market_prices, risk_free_rate, market_caps, symbols, investor_views,
            confidences, prints=False
    ):
        """
        :description: Calculate Black-Litterman

        :param covariance_matrix: Covariance matrix
        :type covariance_matrix: pandas.core.frame.DataFrame, required
        :param market_prices: Market prices
        :type market_prices: pandas.core.series.Series, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param market_caps: Market capitalization
        :type market_caps: pandas.core.series.Series, required
        :param symbols: Symbols
        :type symbols: list, required
        :param investor_views: Investor views
        :type investor_views: dict, required
        :param confidences: Confidences
        :type confidences: pandas.core.series.Series, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: posterior covariance matrix, posterior expected returns
        :rtype: tuple
        """
        delta = self.market_implied_risk_aversion(market_prices, risk_free_rate, prints=prints)

        prior_returns = black_litterman.market_implied_prior_returns(
            market_caps.loc[symbols],
            delta,
            covariance_matrix,
            risk_free_rate
        )
        if prints:
            print('\nPrior Expected Returns:')
            print((100 * prior_returns).sort_values(ascending=False).apply(lambda x: '{:,.2f}%'.format(round(x, 4))))

        bl = black_litterman.BlackLittermanModel(
            covariance_matrix,
            pi='market',
            absolute_views=investor_views,
            risk_aversion=delta,
            market_caps=market_caps.loc[symbols],
            risk_free_rate=risk_free_rate,
            omega='idzorek',
            view_confidences=list(confidences)
        )

        posterior_covariance_matrix = bl.bl_cov()
        posterior_expected_returns = bl.bl_returns()

        investor_views = pd.Series(investor_views)
        min_values = pd.concat([prior_returns, investor_views], axis=1).min(axis=1)
        max_values = pd.concat([prior_returns, investor_views], axis=1).max(axis=1)
        posterior_expected_returns = posterior_expected_returns.clip(lower=min_values, upper=max_values)

        if prints:
            print('\nPosterior Expected Returns:')
            print((100 * posterior_expected_returns).sort_values(ascending=False).apply(lambda x: '{:,.2f}%'.format(
                round(x, 4))))

        return posterior_covariance_matrix, posterior_expected_returns

    def process_ef_output(self, ef, risk_free_rate, portfolio_name=None):
        """
        :description: Process efficient frontier output

        :param ef: Efficient frontier object
        :type ef: pypfopt.efficient_frontier.EfficientFrontier, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param portfolio_name: Portfolio name, default is None
        :type portfolio_name: str, optional
        :return: volatility, weights, results, print_results
        :rtype: tuple
        """
        weights = ef.clean_weights(self.min_weight)
        weights = pd.DataFrame.from_dict(weights, orient='index', columns=[portfolio_name]).round(4)
        weights = weights.squeeze().fillna(0)
        weights = weights[weights != 0].sort_values(ascending=False)
        performance = pd.DataFrame(ef.portfolio_performance(risk_free_rate=risk_free_rate)).round(4)
        margin_weight = -weights[weights < 0].sum().squeeze()
        portfolio_return = performance.loc[0].squeeze()
        performance.iloc[0, 0] = round((portfolio_return - self.margin_rate * margin_weight), 4)
        results = performance.rename(
            index={0: 'Expected_Return', 1: 'Expected Volatility', 2: 'Sharpe_Ratio'}
        ).squeeze()
        results.name = 'Results'

        # Separate DataFrame for formatted results
        print_results = results.copy()
        formatted_performance = print_results.iloc[:2].apply(lambda x: '{:.2%}'.format(x))
        print_results = pd.concat([formatted_performance, print_results.iloc[2:]])

        volatility = results.loc['Expected Volatility'].squeeze()

        return volatility, weights, results, print_results

    @staticmethod
    def print_results(weights, print_results):
        """
        :description: Print results

        :param weights: Portfolio weights
        :type weights: pandas.core.frame.DataFrame, required
        :param print_results: Print results
        :type print_results: pandas.core.series.Series, required
        :return: None
        """
        print('\nWeights:')
        print(weights.apply(lambda x: '{:.2%}'.format(x)))
        print('\nResults:')
        print(print_results)
        print('\nLong/Short Ratio:')
        print('Portfolio weights sum: {}%'.format(round(weights.sum().squeeze() * 100, 2)))
        print('Long weights sum: {}%'.format(round(weights[weights > 0].sum().squeeze() * 100, 2)))
        print('Short weights sum: {}%'.format(round(weights[weights < 0].sum().squeeze() * 100, 2)))

    def minimum_risk_portfolio(
            self, posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, prints=False
    ):
        """
        :description: Minimum risk portfolio

        :param posterior_expected_returns: Posterior expected returns
        :type posterior_expected_returns: pandas.core.series.Series, required
        :param posterior_covariance_matrix: Posterior covariance matrix
        :type posterior_covariance_matrix: pandas.core.frame.DataFrame, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Minimum risk portfolio volatility, asset weights, and portfolio results
        :rtype: tuple
        """
        if self.optimization_method == 'mean_variance':
            ef = efficient_frontier.EfficientFrontier(
                posterior_expected_returns,
                posterior_covariance_matrix,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.min_volatility()
        elif self.optimization_method == 'semivariance':
            ef = efficient_frontier.EfficientSemivariance(
                posterior_expected_returns,
                self.frequency,
                self.semivariance_benchmark,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.min_semivariance()
        elif self.optimization_method == 'cvar':
            ef = efficient_frontier.EfficientCVaR(
                posterior_expected_returns,
                self.returns,
                self.beta,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.min_cvar()
        elif self.optimization_method == 'cdar':
            ef = efficient_frontier.EfficientCDaR(
                posterior_expected_returns,
                self.returns,
                self.beta,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.min_cdar()
        else:
            raise ValueError(
                "Please select a valid optimization method: 'mean_variance', 'semivariance', 'cvar', or 'cdar'"
            )

        volatility, weights, results, print_results = self.process_ef_output(
            ef, risk_free_rate, 'Minimum Risk Portfolio'
        )

        if prints:
            print('Minimum Risk Portfolio:')
            print('Minimum Volatility: {}%'.format(round(volatility * 100, 2)))
            self.print_results(weights, print_results)

        return volatility, weights, results

    def maximum_risk_portfolio(
            self, posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, prints=False
    ):
        """
        :description: Maximum risk portfolio

        :param posterior_expected_returns: Posterior expected returns
        :type posterior_expected_returns: pandas.core.series.Series, required
        :param posterior_covariance_matrix: Posterior covariance matrix
        :type posterior_covariance_matrix: pandas.core.frame.DataFrame, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Maximum risk portfolio volatility, asset weights, and portfolio results
        :rtype: tuple
        """
        if self.optimization_method == 'mean_variance':
            ef = efficient_frontier.EfficientFrontier(
                posterior_expected_returns,
                posterior_covariance_matrix,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.efficient_risk(1.0)
        elif self.optimization_method == 'semivariance':
            ef = efficient_frontier.EfficientSemivariance(
                posterior_expected_returns,
                self.returns,
                self.frequency,
                self.semivariance_benchmark,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.efficient_risk(1.0)
        elif self.optimization_method == 'cvar':
            ef = efficient_frontier.EfficientCVaR(
                posterior_expected_returns,
                self.returns,
                self.beta,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.efficient_risk(1.0)
        elif self.optimization_method == 'cdar':
            ef = efficient_frontier.EfficientCDaR(
                posterior_expected_returns,
                self.returns,
                self.beta,
                self.bounds
            )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.efficient_risk(1.0)
        else:
            raise ValueError(
                "Please select a valid optimization method: 'mean_variance', 'semivariance', 'cvar', or 'cdar'"
            )

        volatility, weights, results, print_results = self.process_ef_output(
            ef, risk_free_rate, 'Maximum Risk Portfolio'
        )

        if prints:
            print('Maximum Risk Portfolio:')
            print('Maximum Volatility: {}%'.format(round(volatility * 100, 2)))
            self.print_results(weights, print_results)

        return volatility, weights, results

    def maximum_sharpe_portfolio(
            self, posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, prints=False
    ):
        """
        :description: Maximum Sharpe ratio portfolio

        :param posterior_expected_returns: Posterior expected returns
        :type posterior_expected_returns: pandas.core.series.Series, required
        :param posterior_covariance_matrix: Posterior covariance matrix
        :type posterior_covariance_matrix: pandas.core.frame.DataFrame, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Maximum Sharpe portfolio asset weights, and portfolio results
        :rtype: tuple
        """
        ef = efficient_frontier.EfficientFrontier(
            posterior_expected_returns,
            posterior_covariance_matrix,
            self.bounds
        )
        ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
        ef.max_sharpe(risk_free_rate=risk_free_rate)

        volatility, weights, results, print_results = self.process_ef_output(
            ef, risk_free_rate, 'Maximum Sharpe Portfolio'
        )

        if prints:
            print('')
            print('Maximum Sharpe Portfolio:')
            print('Sharpe Ratio: {}'.format(results.loc['Sharpe_Ratio']))
            self.print_results(weights, print_results)

        return weights, results

    def efficient_frontier_portfolios(
            self, posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, prints=False
    ):
        """
        :description: Efficient frontier portfolios

        :param posterior_expected_returns: Posterior expected returns
        :type posterior_expected_returns: pandas.core.series.Series, required
        :param posterior_covariance_matrix: Posterior covariance matrix
        :type posterior_covariance_matrix: pandas.core.frame.DataFrame, required
        :param risk_free_rate: Risk free rate
        :type risk_free_rate: float, required
        :param prints: Prints, default is False
        :type prints: bool, optional
        :return: Efficient frontier portfolios, and portfolio results
        :rtype: tuple
        """
        min_risk = self.minimum_risk_portfolio(
            posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, self.optimization_method)[0]
        max_risk = self.maximum_risk_portfolio(
            posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, self.optimization_method)[0]

        portfolios = pd.DataFrame()
        results = pd.DataFrame()
        counter = 1
        for risk in tqdm(np.linspace(min_risk + .001, max_risk - .001, 20).round(4)):
            if self.optimization_method == 'mean_variance':
                ef = efficient_frontier.EfficientFrontier(
                    posterior_expected_returns, posterior_covariance_matrix, self.bounds, self.optimization_method
                )
            elif self.optimization_method == 'semivariance':
                ef = efficient_frontier.EfficientSemivariance(
                    posterior_expected_returns,
                    self.returns,
                    self.frequency,
                    self.semivariance_benchmark,
                    self.bounds
                )
            elif self.optimization_method == 'cvar':
                ef = efficient_frontier.EfficientCVaR(
                    posterior_expected_returns,
                    self.returns,
                    self.beta,
                    self.bounds
                )
            elif self.optimization_method == 'cdar':
                ef = efficient_frontier.EfficientCDaR(
                    posterior_expected_returns,
                    self.returns,
                    self.beta,
                    self.bounds
                )
            else:
                raise ValueError(
                    "Please select a valid optimization method: 'mean_variance', 'semivariance', 'cvar', or 'cdar'"
                )
            ef.add_constraint(lambda w: cp.norm(w, 1) <= self.long_weight + self.short_weight)
            ef.efficient_risk(risk)

            weights = ef.clean_weights(self.min_weight)
            weights = pd.DataFrame.from_dict(weights, orient='index', columns=[counter]).round(4)
            weights.index.name = 'TICKER'
            weights = weights.fillna(0)

            performance = pd.DataFrame(
                ef.portfolio_performance(risk_free_rate=risk_free_rate),
                columns=[counter],
                index=['Expected_Return', 'Expected Volatility', 'Sharpe_Ratio']
            ).round(4)

            margin_weight = -weights[weights < 0].sum().squeeze()
            exp_return = performance.loc['Expected_Return'].squeeze()
            performance.loc['Expected_Return'] = round(
                (exp_return + (margin_weight * exp_return) - (margin_weight * exp_return * self.margin_rate)) / (
                        1 + margin_weight), 4)
            portfolios = pd.concat([portfolios, weights], axis=1).round(4)
            results = pd.concat([results, performance], axis=1)
            results.name = 'Results'
            counter += 1

        if prints:
            print('Portfolios:')
            print(portfolios.applymap('{:,.2%}'.format))

            print('Results:')
            print_results = results.copy()
            print_results.iloc[:2] = print_results.iloc[:2].applymap('{:,.2%}'.format)
            print(print_results)

        return portfolios, results

    @staticmethod
    def calculate_symbol_vols(covariance_matrix):
        """
        :description: Calculate symbol volatilities

        :param covariance_matrix: Covariance matrix
        :type covariance_matrix: pandas.core.frame.DataFrame, required
        :return: Ticker volatilities
        :rtype: pandas.core.series.Series
        """
        # The diagonal elements of the covariance matrix represent the variance of each ticker
        # Standard deviation is the square root of the variance
        variances = covariance_matrix.values.diagonal()
        std_dev = pd.Series(variances ** 0.5, index=covariance_matrix.columns)
        return std_dev.round(4)

    @staticmethod
    def plot_efficient_frontier(expected_returns, results, covariance_matrix, figsize=(12, 6)):
        """
        :description: Plot efficient frontier

        :param expected_returns: Expected returns
        :type expected_returns: pandas.core.series.Series, required
        :param results: Results
        :type results: pandas.core.frame.DataFrame, required
        :param covariance_matrix: Covariance matrix
        :type covariance_matrix: pandas.core.frame.DataFrame, required
        :param figsize: Figure size, default is (12, 6)
        :type figsize: tuple, optional
        :return: Plot
        :rtype: matplotlib.pyplot.figure
        """
        portfolio_volatilities = list(results.iloc[1:2, :].squeeze())
        returns = list(results.iloc[:1, :].squeeze())
        sharpe_ratios = list(results.iloc[2:3, :].squeeze())
        max_sharpe_ratio_index = sharpe_ratios.index(max(sharpe_ratios))
        min_volatility_index = portfolio_volatilities.index(min(portfolio_volatilities))
        plt.figure(figsize=figsize)
        plt.plot(portfolio_volatilities, returns, c='black', label='Constrained Efficient Frontier')
        plt.scatter(portfolio_volatilities[max_sharpe_ratio_index],
                    returns[max_sharpe_ratio_index],
                    marker='*',
                    color='g',
                    s=400,
                    label='Maximum Sharpe Ratio')
        plt.scatter(portfolio_volatilities[min_volatility_index],
                    returns[min_volatility_index],
                    marker='*',
                    color='r',
                    s=400,
                    label='Minimum Volatility')
        plt.scatter(np.sqrt(np.diag(covariance_matrix)),
                    expected_returns,
                    marker='.',
                    color='black',
                    s=100,
                    label='Individual Assets')
        plt.title('Efficient Frontier with Individual Assets')
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.legend()
        plt.show()
