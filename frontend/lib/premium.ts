import Purchases from "react-native-purchases";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import 'react-native-get-random-values';
import { v4 as uuid } from "uuid";

const STORAGE_KEY = "appUserId";

export async function getOrCreateAppUserId() {
  let id = await AsyncStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = uuid();
    await AsyncStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}

export async function initRevenueCat(publicApiKey: string) {
  const appUserId = await getOrCreateAppUserId();
  await Purchases.configure({ apiKey: publicApiKey, appUserID: appUserId });
  if (__DEV__) {
    await Purchases.setLogLevel(Purchases.LOG_LEVEL.VERBOSE);
  }
  return appUserId;
}

export function useEntitlements() {
  const [loading, setLoading] = useState(true);
  const [isPremium, setIsPremium] = useState(false);
  const [hasNoAds, setHasNoAds] = useState(false);

  async function refresh() {
    const info = await Purchases.getCustomerInfo();
    setIsPremium(!!info.entitlements.active.premium);
    setHasNoAds(!!info.entitlements.active.no_ads);
  }

  useEffect(() => {
    (async () => { try { await refresh(); } finally { setLoading(false); } })();
    const listener = Purchases.addCustomerInfoUpdateListener(refresh);
    return () => listener.remove();
  }, []);

  return { loading, isPremium, hasNoAds, refresh };
}

export type OfferingPick = {
  monthly?: import("react-native-purchases").PurchasesPackage | null;
  annual?: import("react-native-purchases").PurchasesPackage | null;
};

export async function loadOfferings(): Promise<OfferingPick> {
  const offerings = await Purchases.getOfferings();
  return {
    monthly: offerings.current?.monthly ?? null,
    annual: offerings.current?.annual ?? null,
  };
}