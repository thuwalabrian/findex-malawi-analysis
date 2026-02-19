@echo off
REM Financial Inclusion Dashboard Launcher
REM This script launches the interactive dashboard

echo.
echo ============================================================
echo  Financial Inclusion in Malawi - Interactive Dashboard
echo ============================================================
echo.
echo Starting dashboard server...
echo Dashboard will be available at: http://127.0.0.1:8050/
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0dashboard"
python app.py

pause
