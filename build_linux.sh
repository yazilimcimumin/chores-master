#!/bin/bash
# ChoresMaster Linux Build Script for Pardus Smart Boards

echo "================================"
echo "ChoresMaster Linux Build Script"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 bulunamadi! Lutfen Python3 yukleyin."
    exit 1
fi

echo "Python3 bulundu: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 bulunamadi! Lutfen pip3 yukleyin."
    exit 1
fi

echo "pip3 bulundu"
echo ""

# Install required packages
echo "Gerekli paketler yukleniyor..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Paket yukleme hatasi!"
    exit 1
fi

echo ""
echo "PyInstaller ile derleme yapiliyor..."

# Build for Linux
pyinstaller --onefile \
    --windowed \
    --add-data "sounds:sounds" \
    --add-data "logo.png:." \
    --name "ChoresMaster" \
    chores_game.py

if [ $? -ne 0 ]; then
    echo "Derleme hatasi!"
    exit 1
fi

echo ""
echo "================================"
echo "Derleme basarili!"
echo "Calistirabilir dosya: dist/ChoresMaster"
echo "================================"
echo ""
echo "Calistirmak icin:"
echo "  cd dist"
echo "  ./ChoresMaster"
echo ""
