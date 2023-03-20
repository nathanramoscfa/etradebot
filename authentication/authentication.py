import time
import pyetrade
from selenium.common.exceptions import NoSuchElementException


class Authentication(object):
    """
    :description: Etrade OAuth authentication

    :param consumer_key: Consumer key provided by Etrade
    :type consumer_key: str, required
    :param consumer_secret: Consumer secret provided by Etrade
    :type consumer_secret: str, required
    :param web_username: Etrade web username
    :type web_username: str, required
    :param web_password: Etrade web password
    :type web_password: str, required
    :param account_id: Etrade account ID
    :type account_id: str, required
    :param etrade_cookie: Etrade cookie
    :type etrade_cookie: dict, required
    :param sandbox_key: Etrade sandbox consumer key
    :type sandbox_key: str, required
    :param sandbox_secret: Etrade sandbox consumer secret
    :type sandbox_secret: str, required
    :param dev: Run in sandbox mode, defaults to False
    :type dev: bool, optional
    :param headless: Run browser in headless mode, defaults to True
    :type headless: bool, optional
    :param browser: Browser to use, defaults to 'chrome'
    :type browser: str, optional
    :param retries: Number of retries for failed requests, defaults to 3
    :type retries: int, optional
    :EtradeRef: https://apisb.etrade.com/docs/api/authorization/request_token.html
    """
    def __init__(
            self, consumer_key, consumer_secret, web_username, web_password, account_id, etrade_cookie,
            sandbox_key=None, sandbox_secret=None, dev=True, headless=True, browser='chrome', retries=3, sleep=30
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.web_username = web_username
        self.web_password = web_password
        self.account_id = account_id
        self.etrade_cookie = etrade_cookie
        self.sandbox_key = sandbox_key
        self.sandbox_secret = sandbox_secret
        self.dev = dev
        self.headless = headless
        self.browser = browser
        self.retries = retries
        self.sleep = sleep

    def get_oauth(self):
        return pyetrade.ETradeOAuth(
            self.sandbox_key if self.dev else self.consumer_key,
            self.sandbox_secret if self.dev else self.consumer_secret,
            self.web_username,
            self.web_password,
            self.etrade_cookie
        )

    @staticmethod
    def get_access_tokens(oauth, verifier_code):
        return oauth.get_access_token(verifier_code)

    def get_accounts_api(self, tokens):
        return pyetrade.ETradeAccounts(
            self.sandbox_key if self.dev else self.consumer_key,
            self.sandbox_secret if self.dev else self.consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )

    def get_orders_api(self, tokens):
        return pyetrade.ETradeOrder(
            self.sandbox_key if self.dev else self.consumer_key,
            self.sandbox_secret if self.dev else self.consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )

    def get_market_api(self, tokens):
        return pyetrade.ETradeMarket(
            self.sandbox_key if self.dev else self.consumer_key,
            self.sandbox_secret if self.dev else self.consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            self.dev
        )

    def access_api(self):
        oauth = self.get_oauth()
        verifier_code = oauth.get_verification_code(self.dev, self.headless, self.browser)
        tokens = self.get_access_tokens(oauth, verifier_code)

        return (
            self.get_accounts_api(tokens),
            self.get_orders_api(tokens),
            self.get_market_api(tokens)
        )

    def etrade_login(self):
        """
        :description: Login to Etrade

        :return: Etrade API objects
        :rtype: tuple
        """
        for i in range(self.retries):
            try:
                accounts, orders, market = self.access_api()
                return accounts, orders, market
            except NoSuchElementException:
                if self.browser != 'edge':
                    print('ConnectionError: Trying again with edge.')
                    self.browser = 'edge'
                else:
                    print('ConnectionError: Trying again with chrome.')
                    time.sleep(self.sleep)
        raise Exception("Failed to connect to Etrade API after multiple retries")
