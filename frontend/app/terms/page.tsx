import React from 'react';
import { ScrollView, Text } from 'react-native';

export default function TermsPage() {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#0a0a0a' }} contentContainerStyle={{ padding: 16 }}>
      <Text style={{ color: 'white', fontSize: 22, fontWeight: '700', marginBottom: 12 }}>Kullanım Koşulları</Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Amaç: </Text>
        Bu uygulama eğlence amaçlıdır; tıbbi, hukuki veya finansal tavsiye vermez. Kararlarınızdan siz sorumlusunuz.
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Hizmetler: </Text>
        Günün Kartı, çeşitli tarot açılımları, yapay zekâ destekli yorumlar, öğrenme içerikleri ve Premium özellikler (reklamsız deneyim, gelişmiş yorumlar, arşiv).
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Ücretlendirme: </Text>
        Satın alma ve abonelikler Apple App Store/Google Play kurallarına tabidir. Abonelikler dönem sonunda otomatik yenilenebilir; iptal ve iadeler ilgili mağaza politikalarına göre yapılır.
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Veri ve Gizlilik: </Text>
        Anonim tanısal kullanım verileri toplanabilir (ör. akış adımları, performans ölçümü). Soru/yorum içerikleri telemetriye gönderilmez. Detaylar için Gizlilik Politikası sayfamıza bakın (/privacy).
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Reklamlar: </Text>
        Kişiselleştirilmiş reklam gösterimi için yasal izin akışı sunulur. Premium veya “Reklamları kaldır” ürünü aktifleştirildiğinde reklamlar gösterilmez.
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>Sorumluluk Reddi: </Text>
        Hizmet “olduğu gibi” sunulur; kesinti/yanıt hatalarında kural tabanlı yedek yorumlar devreye alınabilir.
      </Text>

      <Text style={{ color: 'rgba(255,255,255,0.95)', lineHeight: 22, marginBottom: 12 }}>
        <Text style={{ fontWeight: '700' }}>İletişim: </Text>
        support@yourdomain.com
      </Text>
    </ScrollView>
  );
}