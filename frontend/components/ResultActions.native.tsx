import React, { useCallback, useEffect } from "react";
import { View, Pressable, Text, Share, Linking } from "react-native";
import { appSchemeUrl, webCardUrl } from "../utils/cards";
import { logEvent } from "../utils/telemetry";
import { useEntitlements } from "@/lib/premium";
import { loadInterstitial, interstitial, canShowInterstitial, AdEventType } from "@/lib/ad";

export default function ResultActionsNative({
  cardId, readingType, shareUrl
}: { cardId: string; readingType: string; shareUrl?: string }) {
  const urlApp = appSchemeUrl(cardId as any);
  const urlWeb = webCardUrl(cardId as any);
  const deep = shareUrl || urlWeb;
  const { isPremium, hasNoAds } = useEntitlements();
  const gated = !(isPremium || hasNoAds);

  useEffect(() => { loadInterstitial(); }, []);

  const onNew = useCallback(async () => {
    try {
      if (gated && await canShowInterstitial()) {
        const unsubscribe = interstitial.addAdEventListener(AdEventType.LOADED, () => {
          unsubscribe?.();
          interstitial.show();
          loadInterstitial();
        });
        loadInterstitial();
      }
    } catch {}
    logEvent({ event: "reading_begin", type: "home" as any });
    Linking.openURL("mystictarot://home");
  }, [gated]);

  const onMeaning = useCallback(() => {
    Linking.openURL(urlApp);
  }, [urlApp]);

  const onShare = useCallback(async () => {
    try {
      await Share.share({ message: `Kart yorumum: ${deep}` });
      logEvent({ event: "share_click", type: readingType });
    } catch {}
  }, [deep, readingType]);

  const btn = (label: string, onPress: () => void, testID: string) => (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      testID={testID}
      style={{ paddingVertical:10, paddingHorizontal:16, borderRadius:12, borderWidth:1 }}
    >
      <Text>{label}</Text>
    </Pressable>
  );

  return (
    <View style={{ flexDirection:"row", flexWrap:"wrap", gap:8, marginTop:12 }}>
      {btn("Yeni kart çek", onNew, "cta-new-reading")}
      {btn("Kart anlamını detaylı oku", onMeaning, "cta-meaning")}
      {btn("Paylaş", onShare, "cta-share")}
    </View>
  );
}