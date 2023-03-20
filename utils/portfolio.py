import pandas as pd


def format_portfolio_data(portfolio_data):
    """
    Format the portfolio data.

    :param portfolio_data: the portfolio_data as a pandas DataFrame.
    :type portfolio_data: pandas.DataFrame
    :return: the formatted portfolio data as a pandas DataFrame.
    :rtype: pandas.DataFrame
    """
    formatted_portfolio = portfolio_data.copy()
    formatted_portfolio['quantity'] = formatted_portfolio['quantity'].apply('{:,.0f}'.format)
    formatted_portfolio['costPerShare'] = formatted_portfolio['costPerShare'].apply('${:,.2f}'.format)
    formatted_portfolio['marketValue'] = formatted_portfolio['marketValue'].apply('${:,.2f}'.format)
    formatted_portfolio['totalCost'] = formatted_portfolio['totalCost'].apply('${:,.2f}'.format)
    formatted_portfolio['daysGain'] = formatted_portfolio['daysGain'].apply('${:,.2f}'.format)
    formatted_portfolio['daysGainPct'] = formatted_portfolio['daysGainPct'].apply('{:.2%}'.format)
    formatted_portfolio['totalGain'] = formatted_portfolio['totalGain'].apply('${:,.2f}'.format)
    formatted_portfolio['totalGainPct'] = formatted_portfolio['totalGainPct'].apply('{:.2%}'.format)
    formatted_portfolio['pctOfPortfolio'] = formatted_portfolio['pctOfPortfolio'].apply('{:.2%}'.format)

    return formatted_portfolio


def calculate_aggregate_portfolio(portfolio_data):
    """
    Calculate the aggregate portfolio.

    :param portfolio_data: the portfolio_data as a pandas DataFrame.
    :type portfolio_data: pandas.DataFrame
    :return: the aggregate portfolio as a pandas Series.
    :rtype: pandas.Series
    """
    aggregate_portfolio = portfolio_data[[
        'marketValue', 'totalCost', 'daysGain', 'daysGainPct', 'totalGain', 'totalGainPct',
        'pctOfPortfolio'
    ]].copy()

    aggregate_dollar = aggregate_portfolio[[
        'marketValue', 'totalCost', 'daysGain', 'totalGain'
    ]].sum().apply('${:,.2f}'.format)

    aggregate_percent = aggregate_portfolio[['daysGainPct', 'totalGainPct', 'pctOfPortfolio']].copy()
    aggregate_percent['daysGainPct'] = aggregate_portfolio['daysGain'] / aggregate_portfolio['totalCost'].sum()
    aggregate_percent['totalGainPct'] = aggregate_portfolio['totalGain'] / aggregate_portfolio['totalCost'].sum()
    aggregate_percent = aggregate_percent.drop('pctOfPortfolio', axis=1).sum().apply('{:.2%}'.format)

    return pd.concat([aggregate_dollar, aggregate_percent])


def calculate_groupby_portfolio(portfolio_data):
    """
    Calculate the groupby portfolio.

    :param portfolio_data: the portfolio_data as a pandas DataFrame.
    :type portfolio_data: pandas.DataFrame
    :return: the groupby portfolio as a pandas DataFrame.
    :rtype: pandas.DataFrame
    """
    groupby_portfolio = portfolio_data[
        ['positionType', 'marketValue', 'totalCost', 'daysGain', 'daysGainPct', 'totalGain', 'totalGainPct',
         'pctOfPortfolio']].copy()

    groupby_dollar = groupby_portfolio[
        ['positionType', 'marketValue', 'totalCost', 'daysGain', 'totalGain']].copy().groupby('positionType').sum()
    groupby_dollar = groupby_dollar.applymap('${:,.2f}'.format)

    groupby_percent = groupby_portfolio[['positionType', 'daysGainPct', 'totalGainPct', 'pctOfPortfolio']].copy()
    groupby_percent['daysGainPct'] = groupby_portfolio['daysGain'] / groupby_portfolio['totalCost'].sum()
    groupby_percent['totalGainPct'] = groupby_portfolio['totalGain'] / groupby_portfolio['totalCost'].sum()
    groupby_percent = groupby_percent.drop('pctOfPortfolio', axis=1).groupby('positionType').sum().applymap(
        '{:.2%}'.format)

    groupby_portfolio = pd.concat([groupby_dollar, groupby_percent], axis=1)

    return groupby_portfolio
