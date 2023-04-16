.. _running:

#######
Running
#######

Running your strategy
=====================

Ensure you have completed the following steps before running your strategy:

    1. :ref:`Install <data>` the Bloomberg SDK and C++ Build Tools.
    2. :ref:`Create <environment>` your Python environment and install ETradeBot.
    3. :ref:`Configure <selenium>` Selenium to work with your browser.
    4. :ref:`Obtain <credentials>` and securely store your E-Trade credentials.
    5. :ref:`Insert <strategies>` your strategy into the strategies directory as a .py file.
    6. :ref:`Configure <batch>` a batch file to run ETradeBot.

ETradeBot can run in one of two modes:

    - Preview Mode: displays the strategy with preview trades.
    - Live Trading Mode: executes trades based on your strategy.

Preview Mode
------------

You can use preview mode to test the program's responses before going live. The program will access your account,
obtain market data, and submit preview trades through the E\-Trade API. The console output will either display the
strategy with preview trades, or, return an error with traceback.

1. Verify the batch file:

    * Ensure the PREVIEW variable is set to ``True`` in ``run_main.bat``:

        .. code-block:: bat

            set PREVIEW=True

    * Ensure the name of your strategy in ``run_main.bat`` matches the name of your strategy file in the ``strategies``
      directory without the ``.py`` extension:

        .. code-block:: bat

            set STRATEGY_NAME=example_strategy

2. Run the bot:

    * In your terminal or command prompt, activate your ``etradebot`` virtual environment:

        * If you are using ``conda``:

        .. code-block:: bash

            conda activate etradebot

        * If you are using ``virtualenv``:

        .. code-block:: bash

            source etradebot/bin/activate

    * Navigate to the root directory of the ETradeBot project.

    .. code-block:: bash

        cd C:\Users\User\etradebot

    * Type the following command and press Enter to start the bot:

    .. code-block:: bash

        run_main.bat

3. Monitor the bot:

    * The bot will automatically generate preview trades based on your strategy.
    * You can monitor the bot's activity through the console output.
    * The bot will save the output and events of the bot to a log file within the ``logs`` directory.
    * If you encounter any errors or issues, refer to the console output and the
      :ref:`troubleshooting <troubleshooting>` section for more information.

.. image:: _static/preview_trades.gif
   :alt: Preview Trades

Live Trading Mode
-----------------

1. Verify the batch file:

    * Ensure the PREVIEW variable is set to ``True`` in ``run_main.bat``:

        .. code-block:: bat

            set PREVIEW=False

    * Ensure the name of your strategy in ``run_main.bat`` matches the name of your strategy file in the ``strategies``
      directory without the ``.py`` extension:

        .. code-block:: bat

            set STRATEGY_NAME=example_strategy

2. Repeat steps 2 and 3 from above:

    * The bot will automatically execute trades based on your strategy.
    * You can monitor the bot's activity through the console output.
    * The bot will save the output and events of the bot to a log file within the ``logs`` directory.
    * If you encounter any errors or issues, refer to the console output and the
      :ref:`troubleshooting <troubleshooting>` section for more information.

.. image:: _static/execute_trades.gif
   :alt: Execute Trades