from strategies.strategy import Strategy
from etrade.etrade import ETrade
from execute.execute import Execute


class Bot:
    """
    :description: This class is the main strategy class that will be used to run the strategy.

    :param consumer_key: Your E-Trade API consumer key
    :type consumer_key: str, required
    :param consumer_secret: Your E-Trade API consumer secret
    :type consumer_secret: str, required
    :param web_username: Your E-Trade web username
    :type web_username: str, required
    :param web_password: Your E-Trade web password
    :type web_password: str, required
    :param account_id: Your E-Trade account ID
    :type account_id: str, required
    :param etrade_cookie: Your E-Trade cookie
    :type etrade_cookie: str, required
    :param account_id_key: Your E-Trade account ID key
    :type account_id_key: str, required
    :param strategy_name: The name of the strategy to run
    :type strategy_name: str, required
    :param sandbox_key: Your E-Trade sandbox API key, defaults to None
    :type sandbox_key: str, optional
    :param sandbox_secret: Your E-Trade sandbox API secret, defaults to None
    :type sandbox_secret: str, optional
    :param dev: Whether to use the E-Trade sandbox, defaults to True
    :type dev: bool, optional
    :param headless: Whether to run the browser in headless mode, defaults to True
    :type headless: bool, optional
    :param browser: The browser to use, defaults to 'chrome'
    :type browser: str, optional
    :param preview: Whether to preview the order, defaults to True
    :type preview: bool, optional
    :param prints: Whether to print the order, defaults to True
    :type prints: bool, optional
    """
    def __init__(
            self, consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie,
            account_id_key, strategy_name, sandbox_key=None, sandbox_secret=None, dev=True, headless=True,
            browser='chrome', preview=True, prints=False
    ):
        """
        :description: This method initializes the bot.

        :return: None
        :rtype: None
        """
        print('Starting bot...')
        # Initialize objects
        self.etrade = ETrade(
            consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie,
            sandbox_key, sandbox_secret, dev, headless, browser
        )
        self.strategy = Strategy(prints, strategy_name)
        self.execute = Execute(self.etrade)

        # Retrieve credentials
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.web_username = web_username
        self.web_password = web_password
        self.etrade_cookie = etrade_cookie
        self.account_id = account_id
        self.account_id_key = account_id_key

        # Run strategy
        self.strategy_name = strategy_name
        self.new_portfolio = self.strategy.run_strategy()

        # Preview or execute trades, print information
        self.preview = preview
        self.prints = prints

    def run(self):
        """
        :description: This method runs the strategy and previews or executes the trades.

        :return: The trade responses from E-Trade
        :rtype: pd.DataFrame
        """
        print('\nRunning strategy: {}'.format(self.strategy_name))

        # Get current portfolio
        current_portfolio = self.etrade.get_portfolio_data(self.account_id_key)[[
            'pctOfPortfolio', 'quantity', 'positionType'
        ]]

        # Get buying power
        buying_power = self.etrade.get_buying_power(self.account_id_key, prints=self.prints)

        # Calculate new portfolio shares
        new_portfolio_shares = self.execute.calculate_shares(self.new_portfolio, buying_power, prints=self.prints)

        # Execute trades
        print('')
        if self.preview:
            print('Previewing trades...')
        else:
            print('Executing trades...')
        place_order = self.execute.execute_trades(
            current_portfolio, new_portfolio_shares, self.account_id_key, self.preview, self.prints
        )

        return place_order
