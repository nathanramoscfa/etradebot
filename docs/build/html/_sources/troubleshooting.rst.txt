.. _troubleshooting:

###############
Troubleshooting
###############

Troubleshooting errors
======================

If you encounter an error, please check the following:

1. Are you in the right Python environment? If you followed the instructions in the :ref:`environment <environment>`
   section, you should be in the ``etrade`` environment.
2. Did you navigate to the correct directory? This should be the directory where you cloned the repository. If you
   followed the instructions in the :ref:`environment <environment>` section, you should be in the ``etrade`` directory.
3. Did you configure your :ref:`credentials <credentials>` correctly and do they match what you see on the E-Trade
   developer site?
4. Did you configure your strategy correctly? The ``strategy`` function within your ``custom_strategy.py`` file must
   return a ``pd.Series``. See :ref:`strategies <strategies>` for more information.

You may still encounter errors even if you configured ETradeBot correctly and previously successfully ran it usually
due to server errors from E-Trade. Here are some common errors encountered by the developer and their solutions:

1. Running ETradeBot to submit real trades outside of normal market trading hours (e.g. nights and weekends) may result
   in a server error. This is because E-Trade's servers may not be as responsive during these times for reasons unknown
   to the developer. It is best to only submit real trades during normal market trading hours.
2. E-Trade's servers may return a server error for reasons unknown to the developer. If this happens, try running
   ETradeBot again after a few minutes. Sometimes, simply rerunning ETradeBot resolved the error. You might also have
   to retry multiple times. When ETradeBot is configured correctly, E-Trade servers will usually respond as expected
   but this is not always the case. Here is an example of an actual Traceback of a server error returned by E-Trade
   where simply rerunning ETradeBot resolved the error:

.. code-block:: console

    Traceback (most recent call last):
      File "C:\Users\User\etradebot\main.py", line 84, in <module>
        main(
      File "C:\Users\User\etradebot\main.py", line 53, in main
        bot = Bot(
              ^^^^
      File "C:\Users\User\etradebot\bot.py", line 54, in __init__
        self.etrade = ETrade(
                      ^^^^^^^
      File "C:\Users\User\etradebot\etrade\etrade.py", line 46, in __init__
        self.accounts, self.orders, self.market = self.auth.etrade_login()
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\User\etradebot\authentication\authentication.py", line 160, in etrade_login
        accounts, orders, market = self.access_api()
                                   ^^^^^^^^^^^^^^^^^
      File "C:\Users\User\etradebot\authentication\authentication.py", line 143, in access_api
        tokens = self.get_access_tokens(oauth, verifier_code)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\User\etradebot\authentication\authentication.py", line 81, in get_access_tokens
        return oauth.get_access_token(verifier_code)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\User\anaconda3\envs\etradebot\Lib\site-packages\pyetrade\authorization.py", line 168, in get_access_token
        self.access_token = self.session.fetch_access_token(self.access_token_url)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\User\anaconda3\envs\etradebot\Lib\site-packages\requests_oauthlib\oauth1_session.py", line 323, in fetch_access_token
        token = self._fetch_token(url, **request_kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\User\anaconda3\envs\etradebot\Lib\site-packages\requests_oauthlib\oauth1_session.py", line 369, in _fetch_token
        raise TokenRequestDenied(error % (r.status_code, r.text), r)
    requests_oauthlib.oauth1_session.TokenRequestDenied: Token request failed with code 500, response was '<!doctype html>
    <html lang="en"><head><title>HTTP Status 500 – Internal Server Error</title><style type="text/css">
    h1 {font-family:Tahoma,Arial,sans-serif; color:white;background-color:#525D76;font-size:22px;}
    h2 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:16px;}
    h3 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:14px;}
    body {font-family:Tahoma,Arial, sans-serif;color:black;background-color:white;}
    b {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;}
    p {font-family:Tahoma,Arial,sans-serif;background:white;color:black;font-size:12px;}
    a {color:black;} a.name {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body>
    <h1>HTTP Status 500 – Internal Server Error</h1><hr class="line" /><p><b>Type</b> Status Report</p><p><b>Description</b>
    The server encountered an unexpected condition that prevented it from fulfilling the request.</p><hr class="line" />
    <h3></h3></body></html>'.

If you are still encountering errors, please `open an issue <https://github.com/nathanramoscfa/etradebot/issues>`_ and
provide as much information as possible.