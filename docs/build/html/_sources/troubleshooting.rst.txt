.. _troubleshooting:

###############
Troubleshooting
###############

Troubleshooting errors
======================

If you encounter an error, please check the following:

1. Are you in the right Python environment? If you followed the instructions in the :ref:`environment <environment>` section, you should be in the ``etrade`` environment.
2. Did you navigate to the correct directory? This should be the directory where you cloned the repository. If you followed the instructions in the :ref:`environment <environment>` section, you should be in the ``etrade`` directory.
3. Did you configure Selenium correctly? Your webdriver must be configured to work with the browser version you are using. See :ref:`selenium <selenium>` for more information.
4. Did you configure your :ref:`credentials <credentials>` correctly and do they match what you see on the E-Trade developer site?
5. Did you configure your strategy correctly? The ``strategy`` function within your ``custom_strategy.py`` file must return a ``pd.Series``. See :ref:`strategies <strategies>` for more information.

You may still encounter errors even if you configured ETradeBot correctly and previously successfully ran it usually due to server errors from E-Trade. Here are some common errors encountered by the developer and their solutions:

1. Running ETradeBot to submit real trades outside of normal market trading hours (e.g. nights and weekends) may result in a server error. This is because E-Trade's servers may not be as responsive during these times for reasons unknown to the developer. It is best to only submit real trades during normal market trading hours.
2. E-Trade's servers may return a server error for reasons unknown to the developer. If this happens, try running ETradeBot again after a few minutes. Sometimes, simply rerunning ETradeBot resolved the error.

If you are still encountering errors, please `open an issue <https://github.com/nathanramoscfa/etradebot/issues>`_ and provide as much information as possible.