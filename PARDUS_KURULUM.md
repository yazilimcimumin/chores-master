# ChoresMaster - Pardus Akıllı Tahta Kurulum Rehberi

## 📋 Gereksinimler

- Pardus 21 veya üzeri
- Python 3.8+
- Pygame kütüphanesi
- İnternet bağlantısı (ilk kurulum için)

## 🚀 Kurulum Yöntemleri

### Yöntem 1: DEB Paketi ile Kurulum (ÖNERİLEN)

En kolay ve hızlı yöntem. Pardus akıllı tahtalar için optimize edilmiştir.

```bash
# 1. Scripti çalıştırılabilir yapın
chmod +x create_deb_package.sh

# 2. DEB paketini oluşturun
./create_deb_package.sh

# 3. Paketi kurun
sudo dpkg -i choresmaster_1.0.0_all.deb

# 4. Bağımlılıkları düzeltin (gerekirse)
sudo apt-get install -f
```

Kurulum tamamlandıktan sonra:
- Uygulama menüsünden "Chores Master" arayin
- Veya terminalden `choresmaster` yazın

### Yöntem 2: Manuel Kurulum Scripti

```bash
# 1. Scripti çalıştırılabilir yapın
chmod +x install_pardus.sh

# 2. Root yetkisi ile çalıştırın
sudo ./install_pardus.sh
```

### Yöntem 3: Python ile Doğrudan Çalıştırma

Kurulum yapmadan test etmek için:

```bash
# 1. Bağımlılıkları yükleyin
sudo apt-get install python3-pygame
pip3 install -r requirements.txt

# 2. Oyunu çalıştırın
python3 chores_game.py
```

### Yöntem 4: Derlenmiş Binary (PyInstaller)

```bash
# 1. Build scriptini çalıştırılabilir yapın
chmod +x build_linux.sh

# 2. Derleyin
./build_linux.sh

# 3. Çalıştırın
cd dist
./ChoresMaster
```

## 🎮 Kullanım

### Uygulama Menüsünden
1. Pardus menüsünü açın
2. "Eğitim" veya "Oyunlar" kategorisine gidin
3. "Chores Master" uygulamasını bulun ve tıklayın

### Terminalden
```bash
choresmaster
```

### Masaüstü Kısayolu
Kurulum sonrası masaüstüne kısayol eklemek için:
```bash
cp /usr/share/applications/choresmaster.desktop ~/Desktop/
chmod +x ~/Desktop/choresmaster.desktop
```

## 🔧 Sorun Giderme

### Pygame Hatası
```bash
sudo apt-get install python3-pygame
pip3 install pygame --upgrade
```

### Ses Çalışmıyor
```bash
sudo apt-get install pulseaudio
pulseaudio --start
```

### İzin Hatası
```bash
sudo chmod +x /usr/local/bin/choresmaster
sudo chmod -R 755 /opt/choresmaster
```

### Logo Görünmüyor
```bash
sudo apt-get install python3-pil
```

## 📦 Kaldırma

### DEB Paketi ile Kurulmuşsa
```bash
sudo dpkg -r choresmaster
```

### Manuel Kurulum ile Kurulmuşsa
```bash
sudo rm -rf /opt/choresmaster
sudo rm /usr/local/bin/choresmaster
sudo rm /usr/share/applications/choresmaster.desktop
sudo rm /usr/share/pixmaps/choresmaster.png
```

## 🎯 Akıllı Tahta Optimizasyonları

### Tam Ekran Modu
Oyun otomatik olarak 1200x800 çözünürlükte açılır. Akıllı tahta için tam ekran yapmak isterseniz:

`chores_game.py` dosyasında şu satırı bulun:
```python
self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
```

Şu şekilde değiştirin:
```python
self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
```

### Dokunmatik Ekran Desteği
Oyun dokunmatik ekranlarla tam uyumludur. Fare tıklamaları dokunma olarak algılanır.

### Otomatik Başlatma
Akıllı tahta açılışında otomatik başlatmak için:

```bash
mkdir -p ~/.config/autostart
cp /usr/share/applications/choresmaster.desktop ~/.config/autostart/
```

## 📊 Sistem Gereksinimleri

- **İşlemci:** 1 GHz veya üzeri
- **RAM:** 512 MB minimum, 1 GB önerilen
- **Disk:** 100 MB boş alan
- **Ekran:** 1024x768 minimum çözünürlük
- **Ses:** Ses kartı (opsiyonel)

## 🆘 Destek

Sorun yaşarsanız:
1. Log dosyasını kontrol edin: `~/.choresmaster.log`
2. Terminalde çalıştırıp hata mesajlarını görün: `python3 /opt/choresmaster/chores_game.py`
3. Sistem loglarını kontrol edin: `journalctl -xe`

## 📝 Notlar

- Pardus 21 ve üzeri sürümlerde test edilmiştir
- Akıllı tahta dokunmatik ekranlarıyla tam uyumludur
- Tüm Türkçe karakterler düzgün görüntülenir
- Ses dosyaları otomatik olarak yüklenir

## 🎓 Eğitim Kurumları İçin

Toplu kurulum için:
```bash
# Tüm bilgisayarlara kurulum
for host in $(cat computers.txt); do
    scp choresmaster_1.0.0_all.deb $host:/tmp/
    ssh $host "sudo dpkg -i /tmp/choresmaster_1.0.0_all.deb"
done
```

## 📄 Lisans

Bu yazılım eğitim amaçlı geliştirilmiştir.
Geliştirici: CeZeC Dev
Programcı: Cesur
