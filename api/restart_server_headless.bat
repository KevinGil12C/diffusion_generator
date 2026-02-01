@echo off
:: Headless Restart Script for Web Interface
echo Stopping Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /PID 11488 2>nul

echo Starting Server...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: Start in background
start /B python main.py > server_log.txt 2>&1
exit
