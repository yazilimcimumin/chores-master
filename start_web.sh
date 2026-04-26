#!/bin/bash
# Start web server for ChoresMaster

echo "========================================"
echo "ChoresMaster Web Server"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 bulunamadi!"
    exit 1
fi

PORT=8000

echo "Web sunucusu baslatiliyor..."
echo "Adres: http://localhost:$PORT"
echo ""
echo "Tarayicinizda acmak icin:"
echo "  http://localhost:$PORT"
echo ""
echo "Durdurmak icin CTRL+C basin"
echo ""

# Start Python HTTP server
python3 -m http.server $PORT
