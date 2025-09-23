# Android Deep Link Doğrulama Rehberi

## 1. Sunucu Doğrulaması

### assetlinks.json Dosyası Kontrolü
```bash
# Content-Type kontrolü
curl -I https://mystic-tarot-24.preview.emergentagent.com/.well-known/assetlinks.json

# Dosya içeriği kontrolü
curl https://mystic-tarot-24.preview.emergentagent.com/.well-known/assetlinks.json
```

**Beklenen Sonuçlar:**
- Content-Type: `application/json`
- Redirect olmamalı (200 OK)
- JSON formatında valid response

## 2. Cihaz Testi (ADB Komutları)

### App Links Doğrulama
```bash
# Uygulama linklerini doğrula
adb shell pm verify-app-links com.your.mystictarot

# Domain doğrulama durumu
adb shell pm get-app-links com.your.mystictarot
```

**Beklenen Sonuç:** 
- Status: `verified` veya `approved`

### Deep Link Test Komutları
```bash
# Ana sayfa test
adb shell am start -a android.intent.action.VIEW -d "https://mystic-tarot-24.preview.emergentagent.com/" com.your.mystictarot

# Kart detay test
adb shell am start -a android.intent.action.VIEW -d "https://mystic-tarot-24.preview.emergentagent.com/cards/gunes" com.your.mystictarot

# Custom scheme test
adb shell am start -a android.intent.action.VIEW -d "mystictarot://cards/gunes" com.your.mystictarot
```

**Beklenen Sonuç:**
- Uygulamanın doğrudan açılması
- Doğru sayfa/ekranın gösterilmesi
- Browser'da açılmamalı

## 3. Sorun Giderme

### Link Verification Sıfırlama
```bash
# Uygulama varsayılanlarını temizle
adb shell pm clear-package-data com.your.mystictarot

# Domain verification cache temizle
adb shell pm reset-preferred-activities

# Tekrar doğrulama
adb shell pm verify-app-links com.your.mystictarot
```

### Manuel Ayar Kontrolü
```
Ayarlar > Uygulamalar > Mystic Tarot > Varsayılan Olarak Aç > Desteklenen Web Adresleri
```

## 4. Build Öncesi Kontrol

### Expo Build Test
```bash
# Config doğrulama
npx expo config --json

# Prebuild test
npx expo prebuild -p android --clean

# EAS build (preview)
eas build -p android --profile preview --clear-cache
```

### Intent Filters Kontrolü (app.json)
```json
"android": {
  "package": "com.your.mystictarot",
  "versionCode": 2,
  "intentFilters": [
    {
      "action": "VIEW",
      "category": ["BROWSABLE", "DEFAULT"],
      "data": [{ "scheme": "mystictarot" }]
    },
    {
      "action": "VIEW",
      "category": ["BROWSABLE", "DEFAULT"],
      "data": [
        { 
          "scheme": "https", 
          "host": "mystic-tarot-24.preview.emergentagent.com", 
          "pathPrefix": "/cards" 
        }
      ]
    }
  ]
}
```

## 5. Production SHA-256 Fingerprint

**Mevcut Fingerprint:**
```
FF:7F:29:1F:16:BB:63:B7:AB:31:44:3B:99:26:E4:02:EC:F6:80:EC:BE:12:FE:0C:83:C0:D7:F1:75:20:43:62
```

**Play Console'dan Release SHA-256 alınması gerekirse:**
1. Play Console > Setup > App signing
2. SHA-256 certificate fingerprint kopyala
3. assetlinks.json güncelle
4. Domain tekrar doğrula

## 6. Başarı Kriterleri

✅ **Başarılı Doğrulama:**
- `curl` komutu 200 OK ve doğru JSON döner
- `adb verify-app-links` komutu `verified` döner
- Test URL'leri uygulamayı doğrudan açar
- Browser'a yönlendirme olmaz

❌ **Başarısızlık İşaretleri:**
- assetlinks.json 404 veya yanlış Content-Type
- `adb verify-app-links` komutu `ask` veya `denied` döner
- URL'ler browser'da açılır
- Uygulama açılmaz

## 7. Test Senaryoları

### Senaryo 1: Kart URL'i
```
https://mystic-tarot-24.preview.emergentagent.com/cards/gunes
→ Uygulamanın kart detay sayfası açılmalı
```

### Senaryo 2: Ana sayfa
```
https://mystic-tarot-24.preview.emergentagent.com/
→ Uygulamanın ana sayfası açılmalı
```

### Senaryo 3: Custom scheme
```
mystictarot://cards/gunes
→ Uygulamanın kart detay sayfası açılmalı
```

**Not:** Tüm testler production build ile yapılmalıdır. Development build'de deep link çalışmayabilir.