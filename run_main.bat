@echo off
rem Run Python script in a given conda environment from a batch file.

rem Define here the path to your conda installation.
set CONDA_PATH=C:\Users\25del\anaconda3

rem Define here the name of your conda environment.
set CONDA_ENV=etradebot

rem Activate the conda environment.
call %CONDA_PATH%\Scripts\activate.bat %CONDA_ENV%

rem Navigate to the directory where etradebot root directory is located.
G:
cd G:\My Drive\etradebot

rem Run your script.
python main.py

rem End the Python program.
taskkill /IM python.exe /F

rem Deactivate the conda environment.
call conda deactivate