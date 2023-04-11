@echo off
rem Run Python script in a given conda environment from a batch file.

rem User-defined variables:
rem ---------------------------------------------------------------
rem Define here the path to your conda installation.
set CONDA_PATH=C:\Users\25del\anaconda3

rem Define here the path to your etradebot root directory.
set ETRADEBOT_PATH=G:\My Drive\etradebot

rem Define here the name of your conda environment.
set CONDA_ENV=etradebot

rem Define the strategy name.
set STRATEGY_NAME=cape_strategy

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
