import React, { useEffect, useState } from "react";
import { Platform, View, Text, Pressable, ActivityIndicator, Alert } from "react-native";
import { loadOfferings } from "@/lib/premium";
import { rcAvailable, rcPurchasePackage, rcRestorePurchases } from "@/lib/rc";
import { logEvent } from "@/utils/telemetry";

export default function Paywall({ onClose }: { onClose?: () => void }) {
  const [loading, setLoading] = useState(true);
  const [monthly, setMonthly] = useState<any | null>(null);
  const [annual, setAnnual] = useState<any | null>(null);

  const unsupported = Platform.OS === 'web' || !rcAvailable;

  useEffect(() => {
    (async () => {
      try {
        const pick = await loadOfferings();
        if (pick) {
          setMonthly(pick.monthly ?? null);
          setAnnual(pick.annual ?? null);
        } else {
          setMonthly(null);
          setAnnual(null);
        }
        logEvent({ event: "paywall_view" });
      } finally { 
        setLoading(false); 
      }
    })();
  }, []);

  async function buy(pkg: any | null) {
    if (!pkg || unsupported) return;
    try {
      logEvent({ event: "purchase_start", type: pkg.identifier });
      const { customerInfo } = await rcPurchasePackage(pkg);
      const active = !!customerInfo.entitlements.active.premium || !!customerInfo.entitlements.active.no_ads;
      if (active) {
        logEvent({ event: "purchase_success", type: pkg.identifier });
        onClose?.();
      }
    } catch (e: any) {
      logEvent({ event: "purchase_fail", type: pkg?.identifier });
      if (e?.userCancelled) return;
      Alert.alert("Satın alma başarısız", "Lütfen tekrar deneyin.");
    }
  }

  async function restore() {
    if (unsupported) return;
    try {
      await rcRestorePurchases();
      logEvent({ event: "restore_success" });
      onClose?.();
    } catch {
      Alert.alert("Geri yükleme başarısız", "Lütfen daha sonra deneyin.");
    }
  }

  if (unsupported) {
    return (
      <View style={{ padding: 16 }}>
        <Text style={{ fontSize: 16, textAlign: 'center', opacity: 0.7 }}>
          Purchases are not available in web preview. Please test on a device build.
        </Text>
      </View>
    );
  }

  if (loading) return <ActivityIndicator style={{ padding: 20 }} />;

  const packages = [annual, monthly].filter(Boolean);
  if (packages.length === 0) {
    return (
      <View style={{ padding: 16 }}>
        <Text style={{ textAlign: 'center', opacity: 0.7 }}>No packages available.</Text>
      </View>
    );
  }

  return (
    <View style={{ padding: 16, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "700" }}>Enerjini derinleştir</Text>
      <Text style={{ opacity: 0.7 }}>
        Reklamsız deneyim, AI ton/uzunluk özelleştirmesi ve arşiv.
      </Text>

      {annual && (
        <Pressable onPress={() => buy(annual)} style={btn} testID="buy-annual">
          <Text>Yıllık Premium – {annual.product?.priceString ?? 'Yükleniyor...'}</Text>
        </Pressable>
      )}
      {monthly && (
        <Pressable onPress={() => buy(monthly)} style={btn} testID="buy-monthly">
          <Text>Aylık Premium – {monthly.product?.priceString ?? 'Yükleniyor...'}</Text>
        </Pressable>
      )}
      <Pressable onPress={restore} style={btn} testID="restore">
        <Text>Zaten üyeyim (Geri Yükle)</Text>
      </Pressable>
    </View>
  );
}

const btn = { padding: 12, borderRadius: 12, borderWidth: 1 } as const;