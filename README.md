# 🎮 CHORES MASTER - Ev İşleri Ustası

Profesyonel ve eğlenceli İngilizce-Türkçe kelime öğrenme oyunu! 4 farklı oyun modu ile kelime dağarcığınızı geliştirin.

**Geliştirici:** CeZeC Dev  
**Programcı:** Cesur

## 🎯 Oyun Modları

### 1. 🎯 Kim Milyoner Olmak İster (Süresiz)
- 15 soruluk çoktan seçmeli yarışma
- Her doğru cevap daha fazla para kazandırır
- ₺1.000.000'a ulaşmaya çalışın!
- 4 şık arasından doğru cevabı seçin

### 2. ⚡ Hızlı Yanıtla (30 Saniye - SÜRELİ)
- 30 saniye içinde mümkün olduğunca çok kelime
- Klavyeden cevabı yazıp ENTER'a basın
- Her doğru cevap +10 puan
- Hızlı düşünün, hızlı yazın!

### 3. 🎮 Kelime Eşleştirme (Süresiz)
- 8 İngilizce kelimeyi Türkçe karşılıklarıyla eşleştirin
- Sol taraftan İngilizce, sağ taraftan Türkçe seçin
- Rahat tempoda oynayın, süre yok
- Her doğru eşleştirme +10 puan

### 4. ⏱️ Zamana Karşı (60 Saniye - SÜRELİ)
- 60 saniyede 10 kelimeyi doğru cevaplayın
- 4 şıklı sorular
- Süre bitmeden tüm kelimeleri bulun
- Heyecan dolu yarış!

## 🚀 Kurulum

### Windows

1. Python'u yükleyin (Python 3.8 veya üzeri)
2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

### Linux / Pardus

Detaylı kurulum için [PARDUS_KURULUM.md](PARDUS_KURULUM.md) dosyasına bakın.

**Hızlı Kurulum:**
```bash
# DEB paketi oluştur ve kur
chmod +x create_deb_package.sh
./create_deb_package.sh
sudo dpkg -i choresmaster_1.0.0_all.deb
```

## 🎮 Oyunu Çalıştırma

### Web Tarayıcıda (ÖNERİLEN - Kurulum Gerektirmez!)

**Linux/Mac:**
```bash
chmod +x start_web.sh
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

Tarayıcınızda otomatik olarak açılacak veya şu adresi ziyaret edin:
```
http://localhost:8000
```

### Python ile (Masaüstü Uygulaması)
```bash
python chores_game.py
```

### Linux'ta Kuruluysa
```bash
choresmaster
```

## 🌐 Online Yayınlama (GitHub + Vercel)

### Hızlı Deployment

```bash
# Otomatik deployment scripti
chmod +x deploy.sh
./deploy.sh
```

### Manuel Deployment

1. **GitHub'a Yükle:**
```bash
git init
git add .
git commit -m "Initial commit: ChoresMaster"
git remote add origin https://github.com/KULLANICI_ADINIZ/chores-master.git
git branch -M main
git push -u origin main
```

2. **Vercel'de Yayınla:**
   - https://vercel.com adresine git
   - GitHub ile giriş yap
   - "New Project" → GitHub repo'sunu seç
   - "Deploy" butonuna tıkla
   - Otomatik deploy edilecek!

3. **URL'niz Hazır:**
   - https://chores-master.vercel.app
   - Özel domain ekleyebilirsiniz

Detaylı bilgi için: [DEPLOYMENT.md](DEPLOYMENT.md)

## 📦 Derleme

### Windows EXE Oluşturma

```bash
pyinstaller --onefile --windowed --add-data "sounds;sounds" --add-data "logo.png;." --name "ChoresMaster" chores_game.py
```

### Linux Binary Oluşturma

```bash
chmod +x build_linux.sh
./build_linux.sh
```

### Pardus DEB Paketi Oluşturma

```bash
chmod +x create_deb_package.sh
./create_deb_package.sh
```

## 🎨 Özellikler

- ✨ 4 farklı oyun modu
- � Web tarayıcıda çalışır (kurulum gerektirmez!)
- 🖥️ Masaüstü uygulaması (Python/PyGame)
- �🎵 Profesyonel ses efektleri
- 🎨 Modern gradient tasarım
- 🏆 Puan sistemi
- ⏱️ 2 süreli, 2 süresiz mod
- 📚 23 farklı ev işi kelimesi
- 🎯 Kim Milyoner Olmak İster tarzı quiz
- 🌈 Renkli ve kullanıcı dostu arayüz
- 🔊 Doğru/yanlış ses geri bildirimleri
- 🖥️ Pardus akıllı tahta desteği
- 👆 Dokunmatik ekran uyumlu
- 📱 Mobil uyumlu (responsive)
- 🎓 Eğitim kurumları için optimize
- 🌍 Tüm modern tarayıcılarda çalışır

## 🎯 Kelime Listesi

Oyunda 23 farklı ev işi kelimesi bulunmaktadır:
- clean the garage, cook, do the laundry
- make the bed, wash the dishes, walk the dog
- ve daha fazlası...

## 🎮 Kontroller

- **Fare/Dokunmatik**: Menü ve butonlar için
- **Klavye**: Hızlı Yanıtla modunda yazma
- **ENTER**: Cevabı onaylama
- **Ana Menüye Dön**: Her oyunda buton mevcut

## 💡 İpuçları

1. **Kim Milyoner**: Acele etmeyin, düşünerek cevaplayın
2. **Hızlı Yanıtla**: Küçük harfle yazın, hızlı olun
3. **Eşleştirme**: Önce bildiğiniz kelimeleri eşleştirin
4. **Zamana Karşı**: Hızlı karar verin, süre çok önemli!

## 🏆 Başarılar

- 🥉 Bronz: 100+ puan
- 🥈 Gümüş: 500+ puan  
- 🥇 Altın: 1000+ puan
- 💎 Milyoner: Kim Milyoner'i tamamlayın!

## 🖥️ Pardus Akıllı Tahta

Bu oyun Pardus akıllı tahtalar için özel olarak optimize edilmiştir:
- Dokunmatik ekran tam desteği
- Kolay kurulum (DEB paketi)
- Uygulama menüsü entegrasyonu
- Otomatik başlatma seçeneği
- Tam ekran modu

Detaylı kurulum ve kullanım için: [PARDUS_KURULUM.md](PARDUS_KURULUM.md)

## 📋 Sistem Gereksinimleri

### Minimum
- **İşlemci:** 1 GHz
- **RAM:** 512 MB
- **Disk:** 100 MB
- **Ekran:** 1024x768

### Önerilen
- **İşlemci:** 2 GHz
- **RAM:** 1 GB
- **Disk:** 200 MB
- **Ekran:** 1200x800 veya üzeri

## 🔧 Sorun Giderme

### Ses Çalışmıyor
- Ses dosyalarının `sounds/` klasöründe olduğundan emin olun
- Ses kartı sürücülerini kontrol edin

### Logo Görünmüyor
- `logo.png` dosyasının ana dizinde olduğundan emin olun
- PNG formatında olmalı

### Oyun Açılmıyor
```bash
# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt --upgrade
```

## 👨‍💻 Geliştirici

**CeZeC Dev**  
Programcı: Cesur

## 📄 Dosya Yapısı

```
choresmaster/
├── chores_game.py          # Ana oyun dosyası
├── logo.png                # CeZeC Dev logosu
├── requirements.txt        # Python bağımlılıkları
├── sounds/                 # Ses dosyaları
│   ├── correct.mp3
│   ├── wrong.mp3
│   └── thinking.mp3
├── build_linux.sh          # Linux derleme scripti
├── install_pardus.sh       # Pardus kurulum scripti
├── create_deb_package.sh   # DEB paketi oluşturma
├── PARDUS_KURULUM.md       # Pardus kurulum rehberi
└── README.md               # Bu dosya
```

## 🎓 Eğitim Amaçlı Kullanım

Bu oyun eğitim kurumlarında ücretsiz kullanılabilir:
- İlkokul ve ortaokul İngilizce dersleri
- Akıllı tahta uygulamaları
- Dil öğrenme merkezleri
- Özel eğitim kurumları

Eğlenceli oyunlar! 🎉
