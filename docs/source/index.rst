.. ETradeBot documentation master file, created by
   sphinx-quickstart on Sat Apr  1 19:32:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#########
ETradeBot
#########

ETradeBot is an automated trading software written in Python for E-Trade accounts that allows users to execute trades based on custom trading strategies. ETradeBot is strategy-agnostic and will execute any strategy given to it. This project is not affiliated with E-Trade or any other financial institution.

Features
========

-   Fetches real-time market data from E-Trade API
-   Executes trades (buy/sell/sell short/short cover) based on user-defined strategies
-   Manages portfolio: tracks positions, balance, and performance
-   Trades common stocks, ETFs, and mutual funds

Options, futures, and Forex will be added in future releases.

Getting Started
===============

Refer to the `ETradeBot documentation <https://nr-capital-management.gitbook.io/etradebot/>`_ for instructions on installing, configuring, and using the software. Your E-Trade account must be approved and have the required forms signed and submitted for each trade type.

1. :ref:`Configure <environment>` your Python environment and install ETradeBot.
2. :ref:`Configure <selenium>` Selenium to work with your browser.
3. :ref:`Obtain <credentials>` and securely store your E-Trade credentials.
4. :ref:`Insert <strategies>` your strategy into the strategies directory as a .py file.
5. :ref:`Run <running>` main.py from the root directory.

Important Links
===============

-   ETradeBot GitHub: https://github.com/nathanramoscfa/etradebot
-   E-Trade Developer: https://developer.etrade.com/home
-   E-Trade API Documentation: https://apisb.etrade.com/docs/api/account/api-account-v1.html
-   Keyring documentation: https://keyring.readthedocs.io/en/latest/

Contributing
============

Contributions to ETradeBot are welcome! Please see the `contributing guidelines <https://github.com/nathanramoscfa/etradebot/blob/main/CONTRIBUTING.md>`_ for more information.

Disclaimer
==========

You must fully read, understand, and agree to the full disclaimer :ref:`here <disclaimer>` before using ETradeBot. Please note that while the developer has taken care to ensure the quality and functionality of ETradeBot, there is no guarantee that the software is free from errors or bugs. The developer does not assume responsibility or liability for any damages or losses incurred as a result of using ETradeBot. Users of ETradeBot should use the software at their own risk and verify the accuracy and correctness of its output before making any investment decisions. By using ETradeBot, users agree to release the developer from any and all liability related to their use of the software. Users should read and understand all documentation and instructions provided before using ETradeBot. If you do not agree with any part of this disclaimer, do not use ETradeBot.

License
=======

ETradeBot is licensed under the `MIT License <https://github.com/nathanramoscfa/etradebot/blob/main/LICENSE>`_.

Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Configuration

   environment
   selenium
   credentials
   strategies

.. toctree::
   :maxdepth: 2
   :caption: Usage

   running
   scheduling

.. toctree::
   :maxdepth: 2
   :caption: Core Modules

   authentication
   bot
   etrade
   execute
   strategy

.. toctree::
   :maxdepth: 2
   :caption: Utilities

   fake_data
   model
   portfolio

.. toctree::
   :maxdepth: 2
   :caption: Disclaimer

   disclaimer


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
