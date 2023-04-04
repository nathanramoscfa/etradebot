.. _troubleshooting:

###############
Troubleshooting
###############

Troubleshooting errors
======================

If you encounter an error, please check the following:

1. Are you in the right Python environment? If you followed the instructions in the :ref:`environment <environment>` section, you should be in the ``etrade`` environment.
2. Did you navigate to the correct directory? This should be the directory where you cloned the repository. If you followed the instructions in the :ref:`environment <environment>` section, you should be in the ``etrade`` directory.
3. Did you configure your :ref:`credentials <credentials>` correctly and do they match what you see on the E-Trade developer site?
4. Did you configure your strategy correctly? See :ref:`strategies <strategies>` for more information.

You may still encounter errors even if you configured ETradeBot and/or previously successfully ran it. Here are some common errors encountered by the developer and their solutions:

1. Running ETradeBot to submit real trades outside of normal market trading hours (e.g. nights and weekends) may result in a server error. This is because E-Trade's servers may not be responsive during these times for reasons unknown to the developer. It is best to only submit real trades during normal market trading hours.
2. E-Trade's servers may return a server error for reasons unknown to the developer. If this happens, try running ETradeBot again. Sometimes, simply rerunning ETradeBot resolved the error.

If you are still encountering errors, please `open an issue <https://github.com/nathanramoscfa/etradebot/issues>`_ and provide as much information as possible.