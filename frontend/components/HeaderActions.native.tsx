import React, { useState } from "react";
import { View, Pressable, Text } from "react-native";
import Paywall from "@/components/Paywall";
import { useEntitlements } from "@/lib/premium";

export default function HeaderActions() {
  const { isPremium, hasNoAds } = useEntitlements();
  const [open, setOpen] = useState(false);
  const gated = !(isPremium || hasNoAds);
  return (
    <View style={{ flexDirection: "row", gap: 8 }}>
      {gated && (
        <Pressable
          onPress={() => setOpen(true)}
          testID="open-paywall"
          style={{ paddingVertical: 8, paddingHorizontal: 12, borderRadius: 999, borderWidth: 1 }}
        >
          <Text>Premium’a geç</Text>
        </Pressable>
      )}
      {open && <Paywall onClose={() => setOpen(false)} />}
    </View>
  );
}