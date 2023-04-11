.. _running:

#######
Running
#######

Running your strategy
=====================

ETradeBot can run in one of two modes:

    - Preview Mode.
    - Live Trading Mode.

Preview Mode allows you to test your strategy without executing any real trades. Live Trading Mode allows you to execute trades based on your strategy.

Configure Batch File
--------------------

1. Open a text editor and create a new file named ``run_main.bat``.
2. Copy and paste the following code into the file while modifying the user-defined variables to match your setup:

    .. code-block:: bat

        @echo off
        rem Run Python script in a given conda environment from a batch file.

        rem User-defined variables:
        rem ---------------------------------------------------------------
        rem Define here the path to your conda installation.
        set CONDA_PATH=C:\Users\User\anaconda3

        rem Define here the path to your etradebot root directory.
        set ETRADEBOT_PATH=C:\Users\User\etradebot

        rem Define here the name of your conda environment.
        set CONDA_ENV=etradebot

        rem Define the strategy name.
        set STRATEGY_NAME=example_strategy

        rem Set ETradeBot to either preview or live trading mode.
        rem SETTING THIS TO FALSE WILL PLACE LIVE TRADES! PROCEED WITH CAUTION!
        set PREVIEW=True

        rem End of user-defined variables.
        rem ---------------------------------------------------------------

        rem Do not modify these commands unless you know what you are doing:
        rem ---------------------------------------------------------------
        rem Activate the conda environment.
        call %CONDA_PATH%\Scripts\activate.bat %CONDA_ENV%

        rem Navigate to the directory where etradebot root directory is located.
        pushd %ETRADEBOT_PATH%

        rem Run your script.
        python main.py %PREVIEW% %STRATEGY_NAME%

        rem End the Python program.
        taskkill /IM python.exe /F

        rem Deactivate the conda environment.
        call conda deactivate
        rem ---------------------------------------------------------------
        rem End of commands.

Preview Mode
------------

In ``run_main.bat``, the ``PREVIEW`` parameter is set to ``True`` by default allowing the user to run ETradeBot without executing any real trades. You can use preview mode to test the program's responses before going live. The program will access your account, obtain market data, and submit preview trades through the E\-Trade API. The console output will either display the strategy with preview trades, or, return an error with traceback.

1. Configure the batch file:

    * Set the PREVIEW variable to ``True`` in ``run_main.bat``:

        .. code-block:: bat

            set PREVIEW=True

    * Set the name of your strategy in ``run_main.bat`` which should match the name of your strategy file in the ``strategies`` directory without the ``.py`` extension:

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

        cd /path/to/etradebot

    * Type the following command and press Enter to start the bot:

    .. code-block:: bash

        run_main.bat

3. Monitor the bot:

    * The bot will automatically generate preview trades based on your strategy.
    * You can monitor the bot's activity through the console output.
    * The bot will save the output and events of the bot to a log file within the ``logs`` directory.
    * If you encounter any errors or issues, refer to the console output and the :ref:`troubleshooting <troubleshooting>` section for more information.

.. image:: _static/preview_trades.gif
   :alt: Preview Trades

Live Trading Mode
-----------------

1. Configure the batch file:

    * Set the PREVIEW variable to ``False`` in ``run_main.bat``:

        .. code-block:: bat

            set PREVIEW=False

    * Set the name of your strategy in ``run_main.bat`` which should match the name of your strategy file in the ``strategies`` directory without the ``.py`` extension:

        .. code-block:: bat

            set STRATEGY_NAME=example_strategy

2. Repeat steps 2 and 3 from above:

    * The bot will automatically execute trades based on your strategy.
    * You can monitor the bot's activity through the console output.
    * The bot will save the output and events of the bot to a log file within the ``logs`` directory.
    * If you encounter any errors or issues, refer to the console output and the :ref:`troubleshooting <troubleshooting>` section for more information.

.. image:: _static/execute_trades.gif
   :alt: Execute Trades