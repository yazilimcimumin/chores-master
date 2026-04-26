@echo off
REM ChoresMaster Windows Build Script

echo ========================================
echo ChoresMaster Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadi! Lutfen Python yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python bulundu:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip bulunamadi! Lutfen pip yukleyin.
    pause
    exit /b 1
)

echo pip bulundu
echo.

REM Install required packages
echo Gerekli paketler yukleniyor...
pip install -r requirements.txt

if errorlevel 1 (
    echo Paket yukleme hatasi!
    pause
    exit /b 1
)

echo.
echo PyInstaller ile derleme yapiliyor...
echo.

REM Build for Windows
pyinstaller --onefile ^
    --windowed ^
    --add-data "sounds;sounds" ^
    --add-data "logo.png;." ^
    --icon=logo.png ^yo
    --name "ChoresMaster" ^
    chores_game.py

if errorlevel 1 (
    echo Derleme hatasi!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Derleme basarili!
echo Calistirabilir dosya: dist\ChoresMaster.exe
echo ========================================
echo.
echo Calistirmak icin:
echo   cd dist
echo   ChoresMaster.exe
echo.
pause
