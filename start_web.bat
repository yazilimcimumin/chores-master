@echo off
REM Start web server for ChoresMaster

echo ========================================
echo ChoresMaster Web Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadi!
    pause
    exit /b 1
)

set PORT=8000

echo Web sunucusu baslatiliyor...
echo Adres: http://localhost:%PORT%
echo.
echo Tarayicinizda acmak icin:
echo   http://localhost:%PORT%
echo.
echo Durdurmak icin CTRL+C basin
echo.

REM Start Python HTTP server
python -m http.server %PORT%
