# Mağaza Yayına Hazırlık Metinleri

## Google Play Store - Türkçe

### Uygulama Adı
Mystic Tarot – Günün Kartı

### Kısa Açıklama (≤80 karakter)
Günün Kartı, hızlı açılımlar ve AI yorumlarla eğlenceli tarot rehberi.

### Uzun Açıklama
Günün enerjisini tek kartla keşfet ya da 3–4 kart açılımlarıyla derine in. AI destekli yorumlar, kart anlamları, quiz ve öğrenme modlarıyla tarot dünyasını keyifle deneyimle. 

**Özellikler:**
🔮 5 Farklı Açılım Türü:
• Günün Kartı - Günlük rehberlik
• Klasik Tarot - Geçmiş, şimdi, gelecek
• Günün Yolu - İş, para, aşk, genel tavsiye
• Çift Tarot - İlişki analizi
• Evet/Hayır - Hızlı kararlar

🎴 22 Major Arcana Kartı:
• Detaylı kart anlamları
• Türkçe ve İngilizce destek
• Güzel kart animasyonları
• Haptic feedback ve ses efektleri

🤖 AI Destekli Yorumlar:
• Kişiselleştirilebilir ton ve uzunluk
• Akıllı yorumlama algoritması
• Çevrimdışı yedek sistem

🎯 Eğlenceli Quiz:
• 198 tarot sorusu
• 3 zorluk seviyesi
• Öğrenirken eğlenin

✨ Premium Özellikler:
• Reklamsız deneyim
• Gelişmiş AI yorumları
• Özelleştirilebilir deneyim

Uygulama eğlence amaçlıdır; kararlar sana aittir. Premium ile reklamsız deneyim, daha detaylı yorumlar ve özelleştirme seni bekliyor.

### Anahtar Kelimeler
tarot, fal, kart, günün kartı, açılım, aşk, gelecek, oracle, astroloji

---

## App Store - İngilizce

### Uygulama Adı
Mystic Tarot - Card of the Day

### Subtitle
Quick spreads, AI insights, learning

### Promotional Text
Go Premium for ad-free, deeper AI readings!

### Description
Discover your Card of the Day or dive deeper with quick 3–4 card spreads. Enjoy AI-powered insights, rich card meanings, a tarot quiz, haptics, sounds, and stunning card flips.

**Features:**
🔮 5 Reading Types:
• Card of the Day - Daily guidance
• Classic Tarot - Past, present, future
• Path of the Day - Work, money, love, advice
• Couples Tarot - Relationship insights
• Yes/No - Quick decisions

🎴 22 Major Arcana Cards:
• Detailed card meanings
• Turkish & English support
• Beautiful card animations
• Haptic feedback & sound effects

🤖 AI-Powered Insights:
• Customizable tone & length
• Smart interpretation algorithms
• Offline fallback system

🎯 Fun Quiz Game:
• 198 tarot questions
• 3 difficulty levels
• Learn while you play

✨ Premium Features:
• Ad-free experience
• Advanced AI readings
• Customizable experience

For entertainment only. Premium unlocks ad-free mode and deeper, customizable readings.

### Keywords
tarot, card of the day, fortune, spread, love, oracle, astrology, mystical

---

## Ekran Görüntüsü Planı

1. **Ana Ekran** - 5 açılım türü ve "Bugünün Falına Başla" CTA
2. **Günün Kartı Sonucu** - AI yorum ile kart detayı
3. **Klasik Açılım** - 3 kart grid + flip animasyonu
4. **Kart Anlamları** - Major Arcana detay sayfası
5. **Quiz Ekranı** - Soru ve seçenekler
6. **Paywall** - Premium planlar
7. **Ayarlar** - Dil, sesler, haptik ayarları

**Not:** Tüm ekran görüntüleri koyu tema, tutarlı tasarım ve yararlı başlıklarla hazırlanmalı.

---

## Build Komutları

### Android (Google Play)
```bash
# Production build
eas build -p android --profile production --clear-cache

# Submit to Play Console
eas submit -p android --latest --track internal
```

### iOS (App Store)
```bash
# Production build
eas build -p ios --profile production

# Submit to App Store Connect
eas submit -p ios --latest
```

## Zorunlu Formlar

### Google Play Console
- **App Content > Data Safety**: Ads kullanımı, veri toplama izinleri
- **Target Audience**: 13+ yaş sınırı
- **Privacy Policy URL**: https://mystic-tarot-24.preview.emergentagent.com/privacy
- **Store Listing**: İkon, açıklamalar, ekran görüntüleri

### App Store Connect
- **App Privacy**: Identifiers, Usage Data, Diagnostics
- **Age Rating**: 12+ (Simulated Gambling için)
- **Export Compliance**: Şifreleme kullanımı
- **Privacy URL**: https://mystic-tarot-24.preview.emergentagent.com/privacy