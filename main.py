import ast
import keyring
from bot import Bot

# Retrieve credentials from keyring
consumer_key = keyring.get_password("etrade", "consumer_key")
consumer_secret = keyring.get_password("etrade", "consumer_secret")
sandbox_key = keyring.get_password("etrade", "sandbox_key")
sandbox_secret = keyring.get_password("etrade", "sandbox_secret")
web_username = keyring.get_password("etrade", "web_username")
web_password = keyring.get_password("etrade", "web_password")
account_id = keyring.get_password("etrade", "account_id")
etrade_cookie = ast.literal_eval(keyring.get_password("etrade", "cookie"))
account_id_key = keyring.get_password("etrade", "account_id_key")

# Define the strategy name
strategy_name = 'cape_strategy'


# Define the main function
def main():
    # Create a bot object with the retrieved credentials
    bot = Bot(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        web_username=web_username,
        web_password=web_password,
        account_id=account_id,
        etrade_cookie=etrade_cookie,
        strategy_name=strategy_name,
        sandbox_key=sandbox_key,
        sandbox_secret=sandbox_secret,
        account_id_key=account_id_key,
        dev=False,  # Set to False for production, True for sandbox
        headless=True,  # Set to False to show browser window, True to hide
        browser='chrome',  # Set to 'chrome' or 'edge'
        preview=False,  # Set to False to execute trades, True to preview
        prints=True,  # Set to True to print information to console
    )

    # Run the strategy
    bot.run()
    print('\nDone!')


if __name__ == '__main__':
    main()
