import React from 'react';
import { View, Text, ScrollView } from 'react-native';

export default function PrivacyPage() {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#0a0a0a' }} contentContainerStyle={{ padding: 16 }}>
      <Text style={{ color: 'white', fontSize: 22, fontWeight: '700', marginBottom: 12 }}>Gizlilik Politikası (Kısa)</Text>
      <Text style={{ color: 'rgba(255,255,255,0.9)', lineHeight: 22 }}>
        • Uygulama eğlence amaçlıdır.{"\n"}
        • Tanısal kullanım verileri (anonim) toplanabilir: uygulama sürümü, cihaz türü, akış adımları (örn. reading_begin/result, abonelik denemesi). Soru/yorum içerikleri telemetriye gönderilmez.{"\n"}
        • Üçüncü taraf sağlayıcılar (örn. RevenueCat, ödeme; Google AdMob/AdSense, reklam) kendi politikalarına tabidir.{"\n"}
        • Satın almalar App Store/Google Play kuralları kapsamında gerçekleştirilir.{"\n"}
        • Sorularınız için: support@example.com
      </Text>
      <Text style={{ color: 'rgba(255,255,255,0.9)', lineHeight: 22, marginTop: 16 }}>
        Uyarı: Bu uygulama tıbbi, hukuki veya finansal tavsiye vermez; kararlarınızdan siz sorumlusunuz.
      </Text>
    </ScrollView>
  );
}