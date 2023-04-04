.. _running:

#######
Running
#######

Running your strategy
=====================

Preview Mode
------------

In ``main.py``, the ``preview`` variable is set to ``True`` by default allowing the user to run ETradeBot without executing any trades. You can use preview mode to test the program before going live. The program will access your account, obtain market data, and submit preview trades through the E\-Trade API. The console output will either display the strategy with preview trades, or, return an error with traceback.

1. Run the bot:

    * In your terminal or command prompt, activate your ``etradebot`` virtual environment:

        * If you are using ``conda``:

        .. code-block:: bash

            conda activate etradebot

        * If you are using ``virtualenv``:

        .. code-block:: bash

            source etradebot/bin/activate

    * Navigate to the root directory of the ETradeBot project.

    .. code-block:: bash

        cd /path/to/etradebot

    * Run the following command to start the bot:

    .. code-block:: bash

        python main.py

    .. image:: _static/preview_trades.gif
       :alt: Preview Trades

2. Monitor the bot:

    * The bot will automatically execute trades based on your strategy.
    * You can monitor the bot's activity through the console output.
    * If you encounter any errors or issues, refer to the console output in the root directory for more information.

Live Trading Mode
-----------------

1. Set ``preview`` parameter in ``main.py`` to ``True``.
2. Repeat steps 1 and 2 from above.