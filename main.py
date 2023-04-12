import os
import sys
import ast
import pytz
import keyring
import logging
import pandas_market_calendars as mcal

from bot import Bot
from datetime import datetime, time


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


def is_market_open():
    now = datetime.now(pytz.timezone('US/Eastern'))
    market_open = time(hour=9, minute=30)
    market_close = time(hour=16, minute=0)
    nyse = mcal.get_calendar('NYSE')

    if market_open <= now.time() <= market_close and now.weekday() < 5:
        current_date = now.date()
        schedule = nyse.schedule(start_date=current_date, end_date=current_date)
        if schedule.empty:
            return False, "The market is closed today due to a holiday."
        else:
            return True, None
    else:
        return False, "The market is closed now. It's outside trading hours or it's a weekend."


# Define the main function
def main(preview_mode=True, strategy_name='example_strategy'):
    # Set up logging
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = datetime.now().strftime('bot_log_%Y%m%d_%H%M%S.txt')
    log_path = os.path.join(log_dir, log_file)
    logging.basicConfig(filename=log_path, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

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
        preview=preview_mode,  # Set to False to execute trades, True to preview
        prints=True,  # Set to True to print information to console
    )

    # Run the strategy and log the output
    market_open, reason = is_market_open()
    if bot.preview or (not bot.preview and market_open):
        logging.info('Starting bot...')
        bot.run()
        logging.info('Bot run complete.')
        print('\nBot run complete.')
    elif not bot.preview and not market_open:
        logging.info(f"Bot not running because: {reason}")
        print(f"\nBot not running because: {reason}")


if __name__ == '__main__':
    main(
        sys.argv[1].lower() == 'true' if len(sys.argv) > 1 else True,
        sys.argv[2] if len(sys.argv) > 2 else 'example_strategy'
    )
