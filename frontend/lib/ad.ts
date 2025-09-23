import { InterstitialAd, AdEventType, TestIds } from "react-native-google-mobile-ads";
import AsyncStorage from "@react-native-async-storage/async-storage";

const interUnit = __DEV__ ? TestIds.INTERSTITIAL : "ca-app-pub-XXXX/INTER";
export const interstitial = InterstitialAd.createForAdRequest(interUnit);

export async function canShowInterstitial() {
  const now = Date.now();
  const dayKey = new Date().toISOString().slice(0, 10);
  const raw = await AsyncStorage.getItem("ad_meta");
  const meta = raw ? JSON.parse(raw) : { day: dayKey, count: 0, last: 0 };
  if (meta.day !== dayKey) { meta.day = dayKey; meta.count = 0; meta.last = 0; }
  if (meta.count >= 3) return false;
  if ((now - meta.last) / 1000 < 90) return false;
  meta.count += 1; meta.last = now;
  await AsyncStorage.setItem("ad_meta", JSON.stringify(meta));
  return true;
}

export function loadInterstitial() { interstitial.load(); }
export { AdEventType };