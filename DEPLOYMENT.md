# 🚀 ChoresMaster Deployment Rehberi

## GitHub'a Yükleme

### 1. Git Repository Oluşturma

```bash
# Git başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: ChoresMaster - Ev İşleri Kelime Oyunu"

# GitHub'da yeni repo oluştur (chores-master)
# Sonra bağla:
git remote add origin https://github.com/KULLANICI_ADINIZ/chores-master.git
git branch -M main
git push -u origin main
```

### 2. GitHub Repository Ayarları

Repository'yi public yapın ki Vercel erişebilsin.

## 🌐 Vercel'de Yayınlama

### Yöntem 1: Vercel CLI (Hızlı)

```bash
# Vercel CLI kur
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Production deploy
vercel --prod
```

### Yöntem 2: Vercel Dashboard (Kolay)

1. **Vercel'e Git:** https://vercel.com
2. **Sign Up/Login** (GitHub ile giriş yapın)
3. **New Project** butonuna tıklayın
4. **Import Git Repository** seçin
5. GitHub'daki `chores-master` repo'sunu seçin
6. **Deploy** butonuna tıklayın

Vercel otomatik olarak:
- Projeyi build edecek
- Domain verecek (örn: chores-master.vercel.app)
- SSL sertifikası ekleyecek
- Her commit'te otomatik deploy yapacak

### 3. Özel Domain (Opsiyonel)

Vercel Dashboard'da:
1. Project Settings → Domains
2. Kendi domain'inizi ekleyin
3. DNS ayarlarını yapın

## 📱 Netlify'da Yayınlama (Alternatif)

### Netlify CLI

```bash
# Netlify CLI kur
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy

# Production deploy
netlify deploy --prod
```

### Netlify Dashboard

1. **Netlify'e Git:** https://netlify.com
2. **Sign Up/Login**
3. **New site from Git**
4. GitHub repo'sunu seçin
5. Deploy

## 🔧 Deployment Ayarları

### Vercel için `vercel.json` (Zaten Hazır)

```json
{
  "version": 2,
  "name": "chores-master"
}
```

### Netlify için `netlify.toml` (Opsiyonel)

```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🌍 Deployment Sonrası

### URL'ler

- **Vercel:** https://chores-master.vercel.app
- **Netlify:** https://chores-master.netlify.app
- **GitHub Pages:** https://KULLANICI_ADINIZ.github.io/chores-master

### Test Etme

1. Tüm oyun modlarını test edin
2. Mobil cihazlarda test edin
3. Farklı tarayıcılarda test edin
4. Ses dosyalarının çalıştığını kontrol edin

### Güncelleme

```bash
# Değişiklikleri yap
git add .
git commit -m "Update: açıklama"
git push

# Vercel/Netlify otomatik deploy yapacak
```

## 📊 Analytics (Opsiyonel)

### Vercel Analytics

```bash
# Vercel dashboard'dan Analytics'i aktif et
```

### Google Analytics

`index.html` dosyasına ekle:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🔒 Güvenlik

- HTTPS otomatik aktif (Vercel/Netlify)
- CORS ayarları yapıldı
- Cache headers optimize edildi

## 🎯 SEO Optimizasyonu

`index.html` dosyasına eklenebilir:

```html
<meta name="description" content="ChoresMaster - İngilizce-Türkçe ev işleri kelime öğrenme oyunu. 4 farklı oyun modu ile eğlenceli öğrenin!">
<meta name="keywords" content="kelime oyunu, ingilizce, türkçe, eğitim, ev işleri, chores">
<meta property="og:title" content="ChoresMaster - Ev İşleri Kelime Oyunu">
<meta property="og:description" content="4 farklı oyun modu ile İngilizce-Türkçe kelime öğrenin!">
<meta property="og:image" content="/logo.png">
```

## 📱 PWA (Progressive Web App) - Opsiyonel

Offline çalışma için `manifest.json` ve service worker eklenebilir.

## 🎓 Eğitim Kurumları İçin

Kendi sunucunuzda host etmek için:

```bash
# Nginx
sudo cp -r * /var/www/html/choresmaster/

# Apache
sudo cp -r * /var/www/html/choresmaster/
```

## 🆘 Sorun Giderme

### Ses Dosyaları Çalışmıyor

- Ses dosyalarının `sounds/` klasöründe olduğundan emin olun
- HTTPS kullanıldığından emin olun
- Tarayıcı console'da hata kontrol edin

### Logo Görünmüyor

- `logo.png` dosyasının root dizinde olduğundan emin olun
- Dosya yollarını kontrol edin

### Deploy Hatası

```bash
# Vercel logs
vercel logs

# Netlify logs
netlify logs
```

## 📞 Destek

- **GitHub Issues:** Sorunları bildirin
- **Email:** info@cezec.dev
- **Geliştirici:** CeZeC Dev
- **Programcı:** Cesur

---

**Not:** Bu proje eğitim amaçlıdır ve ücretsiz kullanılabilir.
