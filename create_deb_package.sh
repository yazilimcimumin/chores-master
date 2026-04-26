#!/bin/bash
# Create DEB package for Pardus

PACKAGE_NAME="choresmaster"
VERSION="1.0.0"
ARCH="all"

echo "========================================"
echo "ChoresMaster DEB Paketi Olusturuluyor"
echo "========================================"
echo ""

# Create package directory structure
PKG_DIR="${PACKAGE_NAME}_${VERSION}_${ARCH}"
echo "Paket dizini olusturuluyor: $PKG_DIR"

mkdir -p $PKG_DIR/DEBIAN
mkdir -p $PKG_DIR/opt/choresmaster
mkdir -p $PKG_DIR/usr/share/applications
mkdir -p $PKG_DIR/usr/share/pixmaps
mkdir -p $PKG_DIR/usr/local/bin

# Create control file
cat > $PKG_DIR/DEBIAN/control << EOF
Package: choresmaster
Version: $VERSION
Section: education
Priority: optional
Architecture: $ARCH
Depends: python3, python3-pygame
Maintainer: CeZeC Dev <info@cezec.dev>
Description: Chores Master - Ev Isleri Kelime Oyunu
 Ingilizce-Turkce kelime ogrenmek icin 4 farkli oyun modu sunan
 egitici bir oyun. Pardus akilli tahtalar icin optimize edilmistir.
 .
 Oyun Modlari:
  - Kim Milyoner Olmak Ister
  - Hizli Yanitla (30 saniye)
  - Kelime Eslestirme
  - Zamana Karsi (60 saniye)
 .
 Programmer: Cesur
EOF

# Create postinst script
cat > $PKG_DIR/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

# Install Python dependencies
pip3 install pygame 2>/dev/null || true

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q
fi

echo "ChoresMaster basariyla kuruldu!"
echo "Uygulamayi baslatmak icin 'choresmaster' yazin veya uygulama menusunden acin."

exit 0
EOF

chmod 755 $PKG_DIR/DEBIAN/postinst

# Create prerm script
cat > $PKG_DIR/DEBIAN/prerm << 'EOF'
#!/bin/bash
set -e
exit 0
EOF

chmod 755 $PKG_DIR/DEBIAN/prerm

# Copy application files
echo "Uygulama dosyalari kopyalaniyor..."
cp chores_game.py $PKG_DIR/opt/choresmaster/
cp -r sounds $PKG_DIR/opt/choresmaster/
cp logo.png $PKG_DIR/opt/choresmaster/
cp requirements.txt $PKG_DIR/opt/choresmaster/

# Copy icon
cp logo.png $PKG_DIR/usr/share/pixmaps/choresmaster.png

# Create desktop entry
cat > $PKG_DIR/usr/share/applications/choresmaster.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Chores Master
Name[tr]=Chores Master
Comment=English-Turkish Word Learning Game
Comment[tr]=Ingilizce-Turkce Kelime Ogrenim Oyunu
Exec=choresmaster
Icon=choresmaster
Terminal=false
Categories=Education;Game;Languages;
Keywords=word;game;english;turkish;education;kelime;oyun;ingilizce;turkce;egitim;
StartupNotify=true
EOF

# Create launcher script
cat > $PKG_DIR/usr/local/bin/choresmaster << 'EOF'
#!/bin/bash
cd /opt/choresmaster
python3 chores_game.py "$@"
EOF

chmod 755 $PKG_DIR/usr/local/bin/choresmaster

# Set permissions
echo "Izinler ayarlaniyor..."
find $PKG_DIR -type d -exec chmod 755 {} \;
find $PKG_DIR/opt/choresmaster -type f -exec chmod 644 {} \;
chmod 755 $PKG_DIR/opt/choresmaster/chores_game.py

# Build package
echo ""
echo "DEB paketi olusturuluyor..."
dpkg-deb --build $PKG_DIR

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "DEB paketi basariyla olusturuldu!"
    echo "Paket: ${PKG_DIR}.deb"
    echo "========================================"
    echo ""
    echo "Kurmak icin:"
    echo "  sudo dpkg -i ${PKG_DIR}.deb"
    echo ""
    echo "Kaldirmak icin:"
    echo "  sudo dpkg -r choresmaster"
    echo ""
else
    echo "Paket olusturma hatasi!"
    exit 1
fi
