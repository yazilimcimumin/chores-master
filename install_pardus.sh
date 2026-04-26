#!/bin/bash
# ChoresMaster Installation Script for Pardus Smart Boards

echo "========================================"
echo "ChoresMaster Pardus Kurulum Scripti"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Bu script root yetkisi ile calistirilmalidir."
    echo "Lutfen 'sudo ./install_pardus.sh' komutunu kullanin."
    exit 1
fi

# Install system dependencies
echo "Sistem bagimliliklari yukleniyor..."
apt-get update
apt-get install -y python3 python3-pip python3-pygame

# Install Python packages
echo ""
echo "Python paketleri yukleniyor..."
pip3 install pygame pyinstaller

# Create application directory
APP_DIR="/opt/choresmaster"
echo ""
echo "Uygulama dizini olusturuluyor: $APP_DIR"
mkdir -p $APP_DIR

# Copy files
echo "Dosyalar kopyalaniyor..."
cp chores_game.py $APP_DIR/
cp -r sounds $APP_DIR/
cp logo.png $APP_DIR/
cp requirements.txt $APP_DIR/

# Create desktop entry
echo ""
echo "Masaustu kisayolu olusturuluyor..."
cat > /usr/share/applications/choresmaster.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Chores Master
Comment=Ev Isleri Kelime Oyunu
Exec=python3 /opt/choresmaster/chores_game.py
Icon=/opt/choresmaster/logo.png
Terminal=false
Categories=Education;Game;
Keywords=kelime;oyun;ingilizce;turkce;egitim;
EOF

# Make executable
chmod +x /usr/share/applications/choresmaster.desktop

# Create launcher script
cat > /usr/local/bin/choresmaster << EOF
#!/bin/bash
cd /opt/choresmaster
python3 chores_game.py
EOF

chmod +x /usr/local/bin/choresmaster

echo ""
echo "========================================"
echo "Kurulum tamamlandi!"
echo "========================================"
echo ""
echo "Oyunu baslatmak icin:"
echo "  1. Uygulama menusunden 'Chores Master' arayin"
echo "  2. Veya terminalden 'choresmaster' yazin"
echo ""
