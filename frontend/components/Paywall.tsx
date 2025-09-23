import React, { useEffect, useState } from "react";
import { View, Text, Pressable, ActivityIndicator, Alert } from "react-native";
import Purchases, { PurchasesPackage } from "react-native-purchases";
import { loadOfferings } from "@/lib/premium";
import { logEvent } from "@/utils/telemetry";

export default function Paywall({ onClose }: { onClose?: () => void }) {
  const [loading, setLoading] = useState(true);
  const [monthly, setMonthly] = useState<PurchasesPackage | null>(null);
  const [annual, setAnnual] = useState<PurchasesPackage | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const o = await loadOfferings();
        setMonthly(o.monthly ?? null);
        setAnnual(o.annual ?? null);
        logEvent({ event: "paywall_view" as any });
      } finally { setLoading(false); }
    })();
  }, []);

  async function buy(pkg: PurchasesPackage | null) {
    if (!pkg) return;
    try {
      logEvent({ event: "purchase_attempt" as any, type: pkg.identifier });
      const { customerInfo } = await Purchases.purchasePackage(pkg);
      const active = !!customerInfo.entitlements.active.premium || !!customerInfo.entitlements.active.no_ads;
      if (active) {
        logEvent({ event: "purchase_success" as any, type: pkg.identifier });
        onClose?.();
      }
    } catch (e: any) {
      logEvent({ event: "purchase_error" as any, type: pkg?.identifier });
      if (e?.userCancelled) return;
      Alert.alert("Satın alma başarısız", "Lütfen tekrar deneyin.");
    }
  }

  async function restore() {
    try {
      await Purchases.restorePurchases();
      logEvent({ event: "restore_success" as any });
      onClose?.();
    } catch {
      Alert.alert("Geri yükleme başarısız", "Lütfen daha sonra deneyin.");
    }
  }

  if (loading) return <ActivityIndicator />;

  return (
    <View style={{ padding:16, gap:12 }}>
      <Text style={{ fontSize:20, fontWeight:"700" }}>Enerjini derinleştir</Text>
      <Text style={{ opacity:0.7 }}>
        Reklamsız deneyim, AI ton/uzunluk özelleştirmesi ve arşiv.
      </Text>

      {annual && (
        <Pressable onPress={() => buy(annual)} style={btn} testID="buy-annual">
          <Text>Yıllık Premium – {annual.product.priceString}</Text>
        </Pressable>
      )}
      {monthly && (
        <Pressable onPress={() => buy(monthly)} style={btn} testID="buy-monthly">
          <Text>Aylık Premium – {monthly.product.priceString}</Text>
        </Pressable>
      )}
      <Pressable onPress={restore} style={btn} testID="restore">
        <Text>Zaten üyeyim (Geri Yükle)</Text>
      </Pressable>
    </View>
  );
}
const btn = { padding:12, borderRadius:12, borderWidth:1 } as const;