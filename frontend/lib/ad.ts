// Dynamic require to avoid bundler error on Expo Go / Web when native module isn't available
let AdsMod: any = null;
try { AdsMod = require('react-native-google-mobile-ads'); } catch (e) { AdsMod = null; }

const FallbackInterstitial = {
  createForAdRequest: (_unit: string) => ({
    load: () => {},
    addAdEventListener: () => () => {},
    show: () => {},
  }),
};

export const AdEventType = AdsMod?.AdEventType ?? { LOADED: 'LOADED' };
export const TestIds = AdsMod?.TestIds ?? {
  INTERSTITIAL: 'ca-app-pub-3940256099942544/1033173712',
  BANNER: 'ca-app-pub-3940256099942544/6300978111',
};
export const BannerAd = AdsMod?.BannerAd ?? ((() => null) as any);
export const BannerAdSize = AdsMod?.BannerAdSize ?? { ANCHORED_ADAPTIVE_BANNER: 'ANCHORED_ADAPTIVE_BANNER' };

import AsyncStorage from "@react-native-async-storage/async-storage";

const Interstitial = AdsMod?.InterstitialAd ?? FallbackInterstitial;
const interUnit = __DEV__ ? TestIds.INTERSTITIAL : "ca-app-pub-XXXX/INTER";
export const interstitial = Interstitial.createForAdRequest(interUnit);

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