# RevenueCat Setup Rehberi - Mystic Tarot

## ✅ Tamamlanan Adımlar

### 1. Paket Kurulumu
- [x] `expo-dev-client` yüklendi ✅
- [x] `react-native-purchases` zaten mevcut ✅

### 2. App.json Yapılandırması
- [x] `expo-dev-client` plugin eklendi ✅
- [x] Native development için hazırlandı ✅

### 3. Kod Yapılandırması
- [x] `_layout.tsx`'de RevenueCat initialization eklendi ✅
- [x] Dynamic require ile web-safe yapıldı ✅
- [x] Platform-specific API key seçimi eklendi ✅
- [x] Error handling ile graceful fallbacks ✅

## 🔑 Gerekli API Keys

### Production için RevenueCat Dashboard'dan alınacak:

**iOS API Key:**
```
appl_xxxxxxxxxxxxxxxxxxxxxxxx
```

**Android API Key:**
```
goog_xxxxxxxxxxxxxxxxxxxxxxxx
```

### API Key Alma Adımları:

1. **RevenueCat Dashboard'a git:** https://app.revenuecat.com
2. **Proje oluştur:** "Mystic Tarot" için yeni proje
3. **iOS App ekle:**
   - Bundle ID: `com.your.mystictarot`
   - API Key'i kopyala → `REVENUECAT_API_KEY_IOS`
4. **Android App ekle:**
   - Package Name: `com.your.mystictarot`
   - API Key'i kopyala → `REVENUECAT_API_KEY_ANDROID`

## 📱 Subscription Ürünleri Yapılandırması

### App Store Connect (iOS):
1. **In-App Purchases oluştur:**
   - `premium_monthly` - Aylık Premium (₺29.99)
   - `premium_annual` - Yıllık Premium (₺299.99)

### Google Play Console (Android):
1. **Subscriptions oluştur:**
   - `premium_monthly` - Aylık Premium (₺29.99)
   - `premium_annual` - Yıllık Premium (₺299.99)

### RevenueCat'te Ürünleri Bağla:
1. **Products sekmesi**
2. **iOS/Android ürünlerini import et**
3. **Offering oluştur:**
   - Name: "default"
   - Packages: `monthly`, `annual`

## 🔧 Mevcut Kod Yapısı

### Initialization (_layout.tsx):
```typescript
// RevenueCat otomatik olarak initialize edilir
// Platform bazlı API key seçimi
// Web environment için fallback
```

### Premium Hook (premium.ts):
```typescript
const { loading, isPremium, hasNoAds } = useEntitlements();
// loading: RevenueCat yükleniyor mu?
// isPremium: Premium abonelik aktif mi?
// hasNoAds: Reklamsız deneyim aktif mi?
```

### Paywall Component (Paywall.tsx):
```typescript
// Subscription packages gösterir
// Purchase flow handle eder
// Restore purchases destekler
```

## 🚀 Production Deployment Checklist

### 1. API Keys Update
```typescript
// app/_layout.tsx içinde güncelle:
const REVENUECAT_API_KEY_IOS = "appl_GERÇEK_iOS_KEY";
const REVENUECAT_API_KEY_ANDROID = "goog_GERÇEK_ANDROID_KEY";
```

### 2. Build Komutları
```bash
# Native development build (RevenueCat çalışır)
eas build -p ios --profile development
eas build -p android --profile development

# Production build
eas build -p ios --profile production
eas build -p android --profile production
```

### 3. Test Senaryoları
- [ ] Purchase flow testi (sandbox)
- [ ] Restore purchases testi
- [ ] Premium features unlock testi
- [ ] Subscription cancellation testi

## 🐛 Sorun Giderme

### Web Preview'da RevenueCat Hatası:
- **Normal:** Web environment'ta RevenueCat native modülü yok
- **Çözüm:** Dynamic require ile fallback eklendi
- **Test:** Native build'de test et

### "No Singleton Instance" Hatası:
- **Sebep:** RevenueCat.configure() çağrılmadan kullanım
- **Çözüm:** _layout.tsx'de initialization eklendi
- **Durum:** ✅ Çözüldü

### API Key Hatası:
- **Test Keys:** Development'ta test keys kullan
- **Production:** Gerçek keys ile replace et
- **Security:** Keys'leri environment variables'a taşı

## 📊 Entitlement Yapısı

### Premium Subscription:
- **ID:** `premium`
- **Features:** 
  - Reklamsız deneyim
  - Gelişmiş AI yorumlar
  - Özel kart açılımları
  - Kişiselleştirme seçenekleri

### No Ads Entitlement:
- **ID:** `no_ads` 
- **Features:**
  - Banner reklamları gizler
  - Interstitial reklamları atlar
  - Premium olmadan sadece reklamsızlık

## ✅ Mevcut Durum

- **✅ Initialization:** Düzgün yapılandırıldı
- **✅ Web Fallback:** Dynamic require ile çözüldü
- **✅ Error Handling:** Graceful fallbacks eklendi
- **⚠️ API Keys:** Test keys → Production keys gerekli
- **⚠️ Products:** RevenueCat Dashboard'da oluşturulacak

**🎉 RevenueCat entegrasyonu production-ready! Sadece API keys ve ürün yapılandırması kaldı.**