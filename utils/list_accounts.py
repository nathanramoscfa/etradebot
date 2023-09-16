import ast
import keyring
import pandas as pd
from etrade.etrade import ETrade


# Retrieve credentials from keyring
consumer_key = keyring.get_password("etrade", "consumer_key")
consumer_secret = keyring.get_password("etrade", "consumer_secret")
web_username = keyring.get_password("etrade", "web_username")
web_password = keyring.get_password("etrade", "web_password")
account_id = keyring.get_password("etrade", "account_id")
etrade_cookie = ast.literal_eval(keyring.get_password("etrade", "cookie"))

# Initialize the E-Trade object
etrade = ETrade(consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie)


def get_account_list():
    """
    :description: This API returns the account information for the current user. The information returned includes
        account type, mode, and details.

    :return: The account information for the current user.
    :rtype: pd.DataFrame
    """
    # Get the account list
    return etrade.get_account_list()
