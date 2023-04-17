.. _batch:

#####
Batch
#####

Configuring Batch File
======================

ETradeBot can be run from a batch file. This is useful for running the program on a schedule. Here are the steps to
configure a batch file:

1. Open a text editor and create a new file in the ``etradebot`` root directory named ``run_main.bat``.
2. Copy and paste the following commands into the file while modifying the user-defined variables (shown in bullet
   points) to match your setup:

    * ``CONDA_PATH``: The path to your conda installation.
    * ``ETRADEBOT_PATH``: The path to your ``etradebot`` root directory.
    * ``CONDA_ENV``: The name of your conda environment.
    * ``STRATEGY_NAME``: The name of your strategy which should match its Python file in the `strategies` directory.
    * ``PREVIEW``: Set to ``True`` to run in preview mode, or ``False`` to run in live trading mode.

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