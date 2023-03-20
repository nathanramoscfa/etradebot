import random
import pandas as pd


def create_fake_balances(num_fake_accounts=4):
    """
    :description: Create fake balances for testing purposes

    :param num_fake_accounts: Number of fake accounts, default is 4
    :type num_fake_accounts: int, optional
    :return: Fake balances
    :rtype: pandas.core.frame.DataFrame
    """
    account_id = [random.randint(10000000, 99999999) for i in range(num_fake_accounts)]
    total_account_value = [round(random.randint(100000, 1000000), 2) for i in range(num_fake_accounts)]
    cash_balance = [round(random.uniform(0, 10000), 2) for i in range(num_fake_accounts)]
    data = {
        "accountId": account_id,
        "totalAccountValue": total_account_value,
        "cashBalance": cash_balance
    }
    df = pd.DataFrame(data).set_index('accountId')

    return df


def create_fake_portfolio(buying_power, prints=False):
    """
    :description: Create fake portfolio for testing purposes
    :param buying_power: Buying power
    :type buying_power: float, required
    :param prints: Prints, default is False
    :type prints: bool, optional
    :return: Fake portfolio
    """
    tickers = ['SPY', 'AGG', 'PSCD', 'QQQ', 'SPSM', 'OIH']
    weights = [0.80, 0.40, 0.10, -0.10, -0.10, -0.10]
    prices = pd.Series(data=[round(random.uniform(10, 100), 2) for i in range(len(tickers))], index=tickers)
    quantity = [x * buying_power for x in weights] / prices
    df = pd.DataFrame(data={
        'symbolDescription': tickers,
        'positionType': ['LONG' if value > 0 else 'SHORT' for value in quantity],
        'quantity': quantity.astype(int),
        'costPerShare': [round(random.uniform(50, 200), 2) for i in range(len(quantity))]
    }).set_index('symbolDescription')
    df['marketValue'] = round(df['quantity'] * prices, 2)
    df['totalCost'] = round(df['quantity'] * df['costPerShare'], 2)
    df['totalGain'] = round(df['marketValue'] - df['totalCost'], 2)
    df['totalGainPct'] = round(df['totalGain'] / df['totalCost'], 2)
    df['pctOfPortfolio'] = weights

    if prints:
        print(df)

    return df
